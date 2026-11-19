"""Testes do motor mínimo de fluxos. Roda numa cópia descartável do harness (não toca no vault real).

    py -3 .claude/harness/tests/test_flow.py
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]          # .claude/harness
TMP = Path(tempfile.mkdtemp(prefix="flowtest_"))
import atexit  # noqa: E402
atexit.register(shutil.rmtree, TMP, ignore_errors=True)
PROJ = TMP / "vault"
H = PROJ / ".claude" / "harness"
shutil.copytree(SRC, H, ignore=shutil.ignore_patterns("state", "__pycache__", "tests", "pesquisa", "hook-errors.log", "OFF", "observe.log"))
(H / "state").mkdir(exist_ok=True)
import _vault  # noqa: E402
_vault.mark(PROJ)

spec = importlib.util.spec_from_file_location("flow", H / "engine" / "flow.py")
flow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(flow)

# vault sintético: 45 NPCs, cada um com uma linha reconhecível; _World e Timeline
for d in ("Characters/NPCs", "_Campaign", "_World", "_QA/.run", "Chapters"):
    (PROJ / d).mkdir(parents=True, exist_ok=True)
NOTES = []
for i in range(45):
    p = PROJ / "Characters" / "NPCs" / f"N{i:02d}.md"
    p.write_text(f"---\ntype: npc\n---\n# N{i:02d}\n\nlinha um\nBell foi visto na sessão {i}.\nlinha três\n", encoding="utf-8")
    NOTES.append(f"Characters/NPCs/N{i:02d}.md")

results_log = []
SK = "C:/Users/x/.claude/plugins/cache/gm-apprentice/gm-apprentice/1.12.33/skills/"
G = "bash .claude/harness/bin/gma "


class T:
    def __init__(self):
        self.lines, self.n = [], 0

    def tool(self, name, inp, err=False):
        tid = f"t{self.n}"
        self.n += 1
        self.lines.append({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": tid, "name": name, "input": inp}]}})
        self.lines.append({"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": tid, "is_error": err}]}})
        return tid

    def user(self, text):
        self.lines.append({"type": "user", "message": {"content": text}})

    def save(self):
        p = TMP / f"tx_{len(results_log)}_{self.n}_{len(self.lines)}.jsonl"
        p.write_text("\n".join(json.dumps(x) for x in self.lines), encoding="utf-8")
        return str(p)


def check(label, cond, extra=""):
    results_log.append(cond)
    print(("PASS " if cond else "FAIL ") + label + (f"  | {extra}" if (extra and not cond) else ""))


def evalute(t, project=PROJ):
    ev, res = flow.load_events(t.save())
    steps = flow.load_steps("qa-passo", "full_audit")
    return flow.evaluate(steps, ev, res, project) + (ev, res)


def write_artifact(passo, name, notes, findings="", status="COMPLETO", motivo=None):
    rel = f"_QA/.run/{name}"
    exam = "[" + ", ".join(notes) + "]"
    mot = f"motivo: {motivo}\n" if motivo else ""
    (PROJ / rel).write_text(f"---\npasso: {passo}\nstatus: {status}\n{mot}examinados: {exam}\n---\n{findings}",
                            encoding="utf-8")
    return str(PROJ / rel)


CMDS = {
    "versao": ["vault-check . version"], "canon": ["vault-check . pc-body"],
    "timeline": ["vault-check . timeline --order"], "nomes": ["vault-check . names"],
    "grafo": ["graph-check . all", "links .", "vault-check . index", "vault-check . gm-leak",
              "vault-check . frontmatter", "vault-check . stories", "vault-check . sessions",
              "vault-check . relationships"],
    "tons": ["tones ."], "rascunhos": ["vault-check . stale-drafts"], "wrapup": ["vault-check . wrapup"],
    "capitulos": ["vault-check . chapters"], "pares": ["vault-check . npc-pairs"], "config": ["vault-check . settings"],
    "spoilers": ['grep -rn "spoiler" --include=*.md .'],
}
CHECK_FILES = {"canon": "canon-audit", "timeline": "timeline-validation", "nomes": "name-similarity",
               "pistas": "clue-redundancy", "grafo": "graph-health", "tons": "tone-words",
               "legado": "legacy-canon-field-repair", "rascunhos": "stale-draft-detection",
               "wrapup": "wrapup-conformance", "capitulos": "chapter-notes", "pares": "npc-pairs",
               "config": "settings", "spoilers": "open-spoilers"}


def do_step(t, sid, read_notes=True):
    """Simula o cumprimento honesto de um passo."""
    if sid in CHECK_FILES:
        t.tool("Read", {"file_path": SK + f"campaign-qa/references/checks/{CHECK_FILES[sid]}.md"})
    if sid == "mundo":
        t.tool("Read", {"file_path": SK + "campaign-qa/references/world-audit-criteria.md"})
    for c in CMDS.get(sid, []):
        t.tool("Bash", {"command": G + c})
    if sid == "canon" and read_notes:
        for n in NOTES[:40]:
            t.tool("Read", {"file_path": str(PROJ / n)})
    if sid in ("canon", "timeline", "nomes", "pistas", "grafo"):
        name = {"canon": "02-canon.md", "timeline": "03-timeline.md", "nomes": "04-nomes.md",
                "pistas": "05-pistas.md", "grafo": "06-grafo.md"}[sid]
        if sid == "canon":
            p = write_artifact(sid, name, NOTES[:3], status="PARCIAL", motivo="amostra de teste: 3 de 45 notas")
        else:
            p = write_artifact(sid, name, NOTES[:3])
        t.tool("Write", {"file_path": p, "content": "x"})
    if sid == "relatorio":
        t.tool("Bash", {"command": G + "vault-check . report-new --mode full_audit --scope full_vault"})
        rp = PROJ / "_QA" / "QA_full_audit_2026-11-17.md"
        rp.write_text("relatório", encoding="utf-8")
        t.tool("Write", {"file_path": str(rp), "content": "x"})
        t.tool("Bash", {"command": G + "vault-check . report-stats"})


ORDER = [s["id"] for s in flow.load_steps("qa-passo", "full_audit")]


def done_until(t, last_id, with_human=True):
    for sid in ORDER:
        if sid == last_id:
            break
        if sid == "achados":
            if with_human:
                t.user("pode seguir, decidi tudo")
            continue
        do_step(t, sid)


# ---- T1: começo
t = T()
out, cur, *_ = evalute(t)
check("T1 sem nada feito, o passo atual é versao", cur and cur["id"] == "versao")

# ---- T2/T3: version gate
t = T(); t.tool("Bash", {"command": G + "vault-check . version"})
out, cur, *_ = evalute(t)
check("T2 version rodado e ok avança para canon", cur["id"] == "canon", str(cur["id"]))
t = T(); t.tool("Bash", {"command": G + "vault-check . version"}, err=True)
out, cur, *_ = evalute(t)
check("T3 version com erro NÃO conta", cur["id"] == "versao")

# ---- T4: canon exige leitura, comando, 40 notas e artefato
t = T(); do_step(t, "versao")
t.tool("Read", {"file_path": SK + "campaign-qa/references/checks/canon-audit.md"})
t.tool("Bash", {"command": G + "vault-check . pc-body"})
out, cur, *_ = evalute(t)
msgs = " | ".join(m["msg"] for m in cur["missing"])
check("T4 canon pede 40 notas e artefato", cur["id"] == "canon" and "40" in msgs and "artefato" not in msgs and "_QA/.run" in msgs, msgs)

# ---- T5: read_min conta Read e Bash com caminho explícito, não curinga/cd
t = T(); do_step(t, "versao")
for n in NOTES[:20]:
    t.tool("Read", {"file_path": str(PROJ / n)})
for n in NOTES[20:40]:
    t.tool("Bash", {"command": f'cat "{PROJ / n}"'})
ev, _ = flow.load_events(t.save())
check("T5a Read + cat com caminho explícito contam (40)", len(flow.notes_read(ev, PROJ)) == 40, str(len(flow.notes_read(ev, PROJ))))
t = T()
t.tool("Bash", {"command": "cd Characters/NPCs && for f in *.md; do cat $f; done"})
ev, _ = flow.load_events(t.save())
check("T5b loop com cd e curinga NÃO conta", len(flow.notes_read(ev, PROJ)) == 0)

# ---- T6: validação de artefato
t = T(); do_step(t, "versao"); do_step(t, "canon")
ev, res = flow.load_events(t.save())
good = write_artifact("canon", "02-canon.md", NOTES[:3],
                      f'### A1 [WARNING] Bell aparece\narquivo: {NOTES[0]}\nlinha: 7\ntrecho: "Bell foi visto na sessão 0."\nproposta: x\n')
check("T6a artefato válido passa", flow.validate_artifact(Path(good), ev, PROJ) == [],
      str(flow.validate_artifact(Path(good), ev, PROJ)))
bad = write_artifact("canon", "02-canon.md", NOTES[:3],
                     f'### A1 [WARNING] inventado\narquivo: {NOTES[0]}\nlinha: 7\ntrecho: "O Matador sumiu do hospital."\nproposta: x\n')
e = flow.validate_artifact(Path(bad), ev, PROJ)
check("T6b trecho que não existe é reprovado", any("trecho não está" in x for x in e), str(e))
nr = write_artifact("canon", "02-canon.md", ["Characters/NPCs/N44.md"])
e = flow.validate_artifact(Path(nr), ev, PROJ)
check("T6c examinado sem leitura é reprovado", any("não aparece em nenhuma leitura" in x for x in e), str(e))
(PROJ / "_QA/.run/02-canon.md").write_text("---\npasso: canon\nstatus: PARCIAL\nexaminados: []\n---\n", encoding="utf-8")
e = flow.validate_artifact(PROJ / "_QA/.run/02-canon.md", ev, PROJ)
check("T6d PARCIAL sem motivo é reprovado", any("exige `motivo" in x for x in e), str(e))
(PROJ / "_QA/.run/02-canon.md").write_text("---\npasso: canon\nstatus: NAO_AVALIADO\nmotivo: sem acesso\nexaminados: []\n---\n", encoding="utf-8")
e = flow.validate_artifact(PROJ / "_QA/.run/02-canon.md", ev, PROJ)
check("T6e NAO_AVALIADO com motivo é aceito", e == [], str(e))
fab = write_artifact("canon", "02-canon.md", NOTES[:3],
                     f'### A1 [WARNING] x\narquivo: Characters/NPCs/N44.md\nlinha: 7\ntrecho: "Bell foi visto na sessão 44."\nproposta: x\n')
e = flow.validate_artifact(Path(fab), ev, PROJ)
check("T6f achado em nota não lida é reprovado", any("não foi lido" in x for x in e), str(e))

# ---- T6g..T6j: honestidade de cobertura e cabeçalho flexível (achados do teste ao vivo)
t = T(); do_step(t, "versao")
for n in NOTES[:45]:
    t.tool("Read", {"file_path": str(PROJ / n)})
ev45, res45 = flow.load_events(t.save())
opts = {"artifact": "_QA/.run/*canon*.md", "complete_needs_pct": 90}
low = write_artifact("canon", "02-canon.md", NOTES[:10])
e = flow.validate_artifact(Path(low), ev45, PROJ, opts)
check("T6g COMPLETO com 10 de 45 notas é reprovado (cobertura)", any("exige 90%" in x for x in e), str(e))
par = write_artifact("canon", "02-canon.md", NOTES[:10], status="PARCIAL", motivo="10 de 45 notas")
check("T6h PARCIAL com motivo é aceito com cobertura baixa", flow.validate_artifact(Path(par), ev45, PROJ, opts) == [])
full = write_artifact("canon", "02-canon.md", NOTES[:45])
check("T6i COMPLETO com 45 de 45 notas é aceito", flow.validate_artifact(Path(full), ev45, PROJ, opts) == [],
      str(flow.validate_artifact(Path(full), ev45, PROJ, opts)))
tid = write_artifact("canon", "02-canon.md", NOTES[:3],
                     f'### T1 [INFO] id com letra T\narquivo: {NOTES[0]}\nlinha: 7\ntrecho: "Bell foi visto na sessão 0."\nproposta: x\n',
                     status="PARCIAL", motivo="teste")
check("T6j cabeçalho com letra T no lugar de A é aceito", flow.validate_artifact(Path(tid), ev45, PROJ) == [],
      str(flow.validate_artifact(Path(tid), ev45, PROJ)))

# ---- T7: passo humano e conclusão
t = T(); done_until(t, "achados", with_human=False)
out, cur, *_ = evalute(t)
check("T7a sem mensagem do mestre, o passo atual é achados (humano)", cur["id"] == "achados" and flow.human_only(cur), str(cur and cur["id"]))
t.user("beleza, decida você mesmo")
out, cur, *_ = evalute(t)
check("T7b com mensagem do mestre avança para relatorio", cur and cur["id"] == "relatorio", str(cur and cur["id"]))
do_step(t, "relatorio")
out, cur, *_ = evalute(t)
check("T7c tudo cumprido: nenhum passo pendente", cur is None, str(cur and cur["id"]))

# ---- T8: passo condicional (_World)
shutil.rmtree(PROJ / "_World")
t = T(); done_until(t, "achados", with_human=False)
out, cur, *_ = evalute(t)
check("T8 sem _World o passo mundo é pulado por condição", [s["state"] for s in out if s["id"] == "mundo"] == ["skip"])
(PROJ / "_World").mkdir()

# ---- T9: hook (integração por stdin)
HOOK = H / "hooks" / "flow_hook.py"


def hook(event, transcript, **kw):
    payload = {"hook_event_name": event, "session_id": f"s{len(results_log)}", "transcript_path": transcript}
    payload.update(kw)
    r = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload).encode(), capture_output=True,
                       env=dict(os.environ, PYTHONUTF8="1"), cwd=str(PROJ))
    return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")


# skill ativa só por comando do usuário
t = T(); t.user("<command-name>/qa-passo</command-name>")
tx = t.save()
rc, o, e = hook("Stop", tx)
check("T9a Stop com passo pendente bloqueia", rc == 2 and "versao" in e, f"rc={rc} {e[:200]}")
SID = "teto1"
codes = [hook("Stop", tx, session_id=SID)[0] for _ in range(4)]
dbg = {p.name: p.read_text(encoding="utf-8") for p in (H / "state").glob("*.json")}
check("T9b respeita o teto de 2 bloqueios (2 bloqueios e depois libera)", codes == [2, 2, 0, 0], f"codes={codes} state={dbg}")
t = T()
rc, o, e = hook("Stop", t.save())
check("T9c skill inativa: não faz nada", rc == 0 and not e.strip() and not o.strip())
t = T(); t.user("<command-name>/qa-passo</command-name>"); done_until(t, "achados", with_human=False)
rc, o, e = hook("Stop", t.save(), session_id="h1")
check("T9d passo humano à espera: Stop deixa parar", rc == 0, f"rc={rc} {e[:200]}")

# relatório antes do fim é barrado
t = T(); t.user("<command-name>/qa-passo</command-name>"); do_step(t, "versao")
rc, o, e = hook("PreToolUse", t.save(), tool_name="Write",
                tool_input={"file_path": str(PROJ / "_QA/QA_full_audit_2026-11-17.md")})
check("T9e gravar o relatório com passos pendentes é barrado", rc == 2 and "canon" in e, f"rc={rc} {e[:200]}")
rc, o, e = hook("PreToolUse", t.save(), tool_name="Write", tool_input={"file_path": str(PROJ / "Characters/NPCs/N00.md")})
check("T9f gravar outra nota não é barrado por este hook", rc == 0)

# PostToolUse: artefato inválido barra, passo novo anuncia uma vez
t = T(); t.user("<command-name>/qa-passo</command-name>"); do_step(t, "versao"); do_step(t, "canon")
bad = write_artifact("canon", "02-canon.md", NOTES[:3],
                     f'### A1 [WARNING] x\narquivo: {NOTES[0]}\nlinha: 7\ntrecho: "texto inventado"\nproposta: x\n',
                     status="PARCIAL", motivo="teste")
rc, o, e = hook("PostToolUse", t.save(), tool_name="Write", tool_input={"file_path": bad}, session_id="p1")
check("T9g PostToolUse reprova artefato com trecho inventado", rc == 2 and "trecho" in e, f"rc={rc} {e[:200]}")
good = write_artifact("canon", "02-canon.md", NOTES[:3], status="PARCIAL", motivo="3 de 45 notas")
rc, o, e = hook("PostToolUse", t.save(), tool_name="Write", tool_input={"file_path": good}, session_id="p2")
check("T9h artefato válido avança e anuncia o passo seguinte", rc == 0 and "additionalContext" in o and "timeline" in o, f"rc={rc} {o[:200]}")
rc, o, e = hook("PostToolUse", t.save(), tool_name="Write", tool_input={"file_path": good}, session_id="p2")
check("T9i o mesmo passo não é anunciado duas vezes", rc == 0 and not o.strip(), o[:200])

# robustez
r = subprocess.run([sys.executable, str(HOOK)], input=b"nao e json", capture_output=True)
check("T9j entrada inválida: falha aberta", r.returncode == 0)
(H / "OFF").write_text("x")
t = T(); t.user("<command-name>/qa-passo</command-name>")
rc, o, e = hook("Stop", t.save(), session_id="off1")
check("T9k OFF desliga", rc == 0)
(H / "OFF").unlink()

# ---- T10: proteção dos juízes
t = T(); t.user("<command-name>/qa-passo</command-name>"); do_step(t, "versao")
tx = t.save()
PROT = [
    ("Write", {"file_path": str(PROJ / ".claude/harness/flows/qa-passo.json")}, True, "Write em flows"),
    ("Edit", {"file_path": str(PROJ / ".claude/harness/hooks/flow_hook.py")}, True, "Edit no hook"),
    ("Write", {"file_path": str(PROJ / ".claude/skills/qa-passo/SKILL.md")}, True, "Write na skill"),
    ("Write", {"file_path": str(PROJ / ".claude/settings.json")}, True, "Write no settings"),
    ("Write", {"file_path": str(PROJ / "CLAUDE.md")}, True, "Write no CLAUDE.md"),
    ("Write", {"file_path": str(PROJ / "_QA/.run/02-canon.md")}, False, "Write em _QA/.run liberado"),
    ("Write", {"file_path": str(PROJ / "Characters/NPCs/N00.md")}, False, "Write em nota liberado"),
    ("Bash", {"command": "echo x > .claude/harness/modes.json"}, True, "redirect para o harness"),
    ("Bash", {"command": "sed -i 's/a/b/' .claude/settings.json"}, True, "sed -i no settings"),
    ("Bash", {"command": "python3 -c \"open('CLAUDE.md','w').write('x')\""}, True, "python escreve no CLAUDE.md"),
    ("Bash", {"command": "rm .claude/harness/state/x.json"}, True, "rm no harness"),
    ("Bash", {"command": "cat .claude/harness/modes.json"}, False, "cat no harness liberado"),
    ("Bash", {"command": "bash .claude/harness/bin/gma vault-check . version"}, False, "executar gma liberado"),
    ("Bash", {"command": "grep -n x CLAUDE.md | head"}, False, "grep no CLAUDE.md liberado"),
]
for i, (tool, inp, blocked, label) in enumerate(PROT):
    rc, o, e = hook("PreToolUse", tx, tool_name=tool, tool_input=inp, session_id=f"pr{i}")
    check(f"T10.{i} {label}", (rc == 2) == blocked, f"rc={rc} {e[:150]}")

# ---- T11: modos
modes = H / "modes.json"
modes.write_text(json.dumps({"flow.protect": "observe", "flow.stop": "off"}), encoding="utf-8")
rc, o, e = hook("PreToolUse", tx, tool_name="Write", tool_input={"file_path": str(PROJ / "CLAUDE.md")}, session_id="m1")
obs = H / "observe.log"
check("T11a observe não bloqueia e registra", rc == 0 and obs.exists() and "flow.protect" in obs.read_text(encoding="utf-8"),
      f"rc={rc} {e[:150]}")
t2 = T(); t2.user("<command-name>/qa-passo</command-name>")
rc, o, e = hook("Stop", t2.save(), session_id="m2")
check("T11b off ignora a guarda de Stop", rc == 0, f"rc={rc} {e[:150]}")
modes.write_text("{ quebrado", encoding="utf-8")
rc, o, e = hook("PreToolUse", tx, tool_name="Write", tool_input={"file_path": str(PROJ / "CLAUDE.md")}, session_id="m3")
check("T11c modes.json ilegível: padrão enforce", rc == 2, f"rc={rc}")
modes.write_text(json.dumps({"flow.protect": "enforce"}), encoding="utf-8")

bad_n = [i for i, c in enumerate(results_log) if not c]
print(f"\n{sum(results_log)}/{len(results_log)} ok")
log = H / "hook-errors.log"
print("hook-errors.log:", log.read_text(encoding="utf-8") if log.exists() else "(vazio)")
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if bad_n else 0)
