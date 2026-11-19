"""Testes da generalização do motor para as 10 skills. Roda numa cópia descartável.

    py -3 .claude/harness/tests/test_general.py
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
TMP = Path(tempfile.mkdtemp(prefix="general_"))
import atexit  # noqa: E402
atexit.register(shutil.rmtree, TMP, ignore_errors=True)
PROJ = TMP / "vault"
H = PROJ / ".claude" / "harness"
shutil.copytree(SRC, H, ignore=shutil.ignore_patterns("state", "__pycache__", "tests", "pesquisa", "testes", "evals",
                                                      "hook-errors.log", "observe.log", "OFF"))
(H / "state").mkdir(exist_ok=True)
import _vault  # noqa: E402
_vault.mark(PROJ)
for d in ("Characters/NPCs", "_Campaign", "_QA/.run", "Chapters"):
    (PROJ / d).mkdir(parents=True, exist_ok=True)
(PROJ / "Characters/NPCs/A.md").write_text("# A\nlinha\n", encoding="utf-8")

spec = importlib.util.spec_from_file_location("flow", H / "engine" / "flow.py")
flow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(flow)
flow.PROJECT = PROJ

HOOK = H / "hooks" / "flow_hook.py"
log = []
ctr = [0]


def check(label, cond, extra=""):
    log.append(cond)
    print(("PASS " if cond else "FAIL ") + label + (f"  | {extra}" if (extra and not cond) else ""))


def tx(lines):
    ctr[0] += 1
    p = TMP / f"t{ctr[0]}.jsonl"
    p.write_text("\n".join(json.dumps(x) for x in lines), encoding="utf-8")
    return str(p)


def user(t):
    return {"type": "user", "message": {"content": t}}


def tool(n, name, inp, err=False):
    return [{"type": "assistant", "message": {"content": [{"type": "tool_use", "id": f"t{n}", "name": name, "input": inp}]}},
            {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": f"t{n}", "is_error": err}]}}]


def hook(event, transcript, sid, **kw):
    p = {"hook_event_name": event, "session_id": sid, "transcript_path": transcript}
    p.update(kw)
    r = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(p).encode(), capture_output=True,
                       env=dict(os.environ, PYTHONUTF8="1"), cwd=str(PROJ))
    return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")


SKILLS = ["campaign-organizer", "campaign-qa", "publish-site", "qa-passo", "session-play", "session-prep",
          "session-wrapup", "the-midwife", "ttrpg-expert", "vault-ingest"]

# ---- G1: as 10 carregam, avaliam transcript vazio e têm passos com id único
check("G1a existem fluxos para as 10 skills", flow.all_skills() == sorted(SKILLS), str(flow.all_skills()))
for sk in SKILLS:
    sp = flow.load_spec(sk)
    for m, steps in sp["modes"].items():
        ids = [s["id"] for s in steps]
        out, cur = flow.evaluate(steps, [], {}, PROJ)
        ok = len(ids) == len(set(ids)) and len(out) == len(steps)
        check(f"G1b {sk}:{m} avalia sem erro e ids únicos ({len(steps)} passos)", ok)

# ---- G2: ativação pelo nome original do plugin, por três caminhos
for sk in SKILLS:
    ev = [{"i": 0, "kind": "user", "text": f"<command-name>/gm-apprentice:{sk}</command-name>"}]
    a = flow.find_activation(ev, "")
    b = flow.find_activation([], f"/gm-apprentice:{sk} faça algo")
    c = flow.find_activation([flow.make_event(0, "Skill", {"skill": f"gm-apprentice:{sk}", "args": "x"})], "")
    check(f"G2 {sk} ativa por comando, prompt e ferramenta Skill",
          all(x and x[0] == sk for x in (a, b, c)), f"{a} {b} {c}")
check("G2z skill desconhecida não ativa", flow.find_activation([], "/commit") is None and
      flow.find_activation([flow.make_event(0, "Skill", {"skill": "outra"})], "") is None)
ev = [flow.make_event(0, "Skill", {"skill": "gm-apprentice:campaign-qa"}),
      flow.make_event(1, "Skill", {"skill": "gm-apprentice:session-wrapup"})]
check("G2y a ativada por último vale", flow.find_activation(ev, "")[0] == "session-wrapup")

# ---- G3: modo e enforce
cq, wu = flow.load_spec("campaign-qa"), flow.load_spec("session-wrapup")
check("G3a campaign-qa: auditoria completa e padrão -> full_audit",
      flow.select_mode(cq, "/campaign-qa auditoria completa") == "full_audit" and flow.select_mode(cq, "") == "full_audit")
check("G3b campaign-qa: 'só a timeline' -> modo_unico", flow.select_mode(cq, "só a timeline") == "modo_unico")
check("G3c campaign-qa full_audit bloqueia; modo_unico só observa",
      flow.enforcing(cq, "full_audit") and not flow.enforcing(cq, "modo_unico"))
check("G3d rascunhos só observam", not flow.enforcing(wu, "padrao") and not flow.enforcing(flow.load_spec("the-midwife"), "aventura"))
check("G3e publish-site: 'site quebrado' -> diagnosticar",
      flow.select_mode(flow.load_spec("publish-site"), "meu site está quebrado") == "diagnosticar")

# ---- G4: átomos novos
steps = [{"id": "x", "evidence": [{"lint": "tocados"}]}]
check("G4a lint sem gravação: ok", flow.evaluate(steps, [], {}, PROJ)[1] is None)
w = flow.make_event(0, "Write", {"file_path": str(PROJ / "Characters/NPCs/A.md")})
check("G4b lint com gravação e sem vault-check: pendente", flow.evaluate(steps, [w], {}, PROJ)[1] is not None)
vc = flow.make_event(1, "Bash", {"command": "bash gma vault-check . frontmatter"}, "c1")
check("G4c lint com vault-check depois: ok", flow.evaluate(steps, [w, vc], {"c1": False}, PROJ)[1] is None)
check("G4d lint com vault-check que falhou: pendente", flow.evaluate(steps, [w, vc], {"c1": True}, PROJ)[1] is not None)
st2 = [{"id": "y", "evidence": [{"read": ["_midwife/index.md"], "if_exists": True}]}]
check("G4e read if_exists: arquivo inexistente não é exigido", flow.evaluate(st2, [], {}, PROJ)[1] is None)
(PROJ / "_midwife").mkdir()
(PROJ / "_midwife/index.md").write_text("x", encoding="utf-8")
check("G4f read if_exists: existente é exigido", flow.evaluate(st2, [], {}, PROJ)[1] is not None)
st3 = [{"id": "z", "evidence": [{"artifact": "wrapup-S*-*.txt", "validate": False}]}]
ev = [flow.make_event(0, "Write", {"file_path": str(TMP / "scratch" / "wrapup-S07-batch.txt")})]
check("G4g artefato fora do vault casa pelo nome", flow.evaluate(st3, ev, {}, PROJ)[1] is None)

# ---- G5: hook com outra skill (rascunho): orienta, não bloqueia, registra
T = tx([user("<command-name>/gm-apprentice:session-wrapup</command-name>")])
rc, o, e = hook("UserPromptSubmit", T, "w1", prompt="/gm-apprentice:session-wrapup")
check("G5a UserPromptSubmit injeta o status da session-wrapup", rc == 0 and "session-wrapup:padrao" in o, f"rc={rc} {o[:200]} {e[:200]}")
rc, o, e = hook("Stop", T, "w1")
obs = H / "observe.log"
check("G5b Stop em rascunho não bloqueia e registra WOULD-BLOCK",
      rc == 0 and obs.exists() and "session-wrapup" in obs.read_text(encoding="utf-8"), f"rc={rc} {e[:150]}")
rc, o, e = hook("PreToolUse", T, "w1", tool_name="Write", tool_input={"file_path": str(PROJ / "CLAUDE.md")})
check("G5c escrever em juiz durante rascunho: não bloqueia", rc == 0, f"rc={rc}")
(H / "modes.json").write_text(json.dumps({"flow.stop@session-wrapup": "enforce"}), encoding="utf-8")
rc, o, e = hook("Stop", T, "w2")
check("G5d modes.json `guarda@skill` força enforce numa skill em rascunho", rc == 2, f"rc={rc} {e[:150]}")
(H / "modes.json").write_text("{}", encoding="utf-8")

# ---- G6: campaign-qa original (nome do plugin) é conduzida e bloqueia
T = tx([user("<command-name>/gm-apprentice:campaign-qa</command-name>")])
rc, o, e = hook("Stop", T, "q1")
check("G6a Stop na campaign-qa original bloqueia", rc == 2 and "campaign-qa" in e, f"rc={rc} {e[:150]}")
rc, o, e = hook("PreToolUse", T, "q2", tool_name="Write", tool_input={"file_path": str(PROJ / "_QA/QA_full_audit_2026-11-17.md")})
check("G6b relatório direto na campaign-qa é barrado", rc == 2, f"rc={rc} {e[:150]}")
rc, o, e = hook("PreToolUse", T, "q3", tool_name="Bash", tool_input={"command": "echo x > _QA/QA_full_audit_2026-11-17.md"})
check("G6c relatório por redirect na campaign-qa é barrado", rc == 2, f"rc={rc}")
rc, o, e = hook("PreToolUse", T, "q4", tool_name="Write", tool_input={"file_path": str(PROJ / ".claude/harness/modes.json")})
check("G6d editar juiz na campaign-qa é barrado", rc == 2, f"rc={rc}")
T2 = tx([user("<command-name>/gm-apprentice:campaign-qa</command-name> só a timeline")])
rc, o, e = hook("Stop", T2, "q5")
check("G6e campaign-qa em modo_unico só observa", rc == 0, f"rc={rc} {e[:150]}")

# ---- G7: sem skill de fluxo ativa, nada acontece
T = tx([user("oi, tudo bem?")])
check("G7 sem skill ativa: nenhum hook age", all(hook(ev, T, "n1")[0] == 0 and not hook(ev, T, "n1")[1].strip()
                                                  for ev in ("Stop", "UserPromptSubmit")))

bad = [i for i, c in enumerate(log) if not c]
print(f"\n{sum(log)}/{len(log)} ok")
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if bad else 0)
