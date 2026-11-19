import json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path

# Teste dourado: roda numa CÓPIA de um vault real.  GMA_VAULT="<caminho do vault>" py -3 test_harness.py
if not os.environ.get("GMA_VAULT"):
    print("SKIP test_harness: defina GMA_VAULT com o caminho de um vault real (é copiado, nunca alterado)")
    sys.exit(0)
SRC = Path(os.environ["GMA_VAULT"])
SCR = Path(tempfile.mkdtemp(prefix="harness_gold_"))
V = SCR / "vaultcopy"
SK = Path(__file__).resolve().parents[2] / "skills"

if V.exists():
    shutil.rmtree(V)
shutil.copytree(SRC, V, ignore=shutil.ignore_patterns(".git", "_inbox", "state", "__pycache__"))
(V / ".claude" / "harness" / "state").mkdir(exist_ok=True)

HOOKS = Path(__file__).resolve().parents[1] / "hooks"
os.environ["CLAUDE_PROJECT_DIR"] = str(V)
results = []


def tl(tools=(), texts=(), skill=None, cmds=()):
    """transcript sintético -> caminho"""
    lines = []
    ts = "2026-11-17T10:00:00.000Z"
    for t in texts:
        lines.append({"type": "user", "timestamp": ts, "message": {"content": t}})
    items = []
    if skill:
        items.append({"type": "tool_use", "name": "Skill", "input": {"skill": "gm-apprentice:" + skill}})
    for p in tools:
        items.append({"type": "tool_use", "name": "Read", "input": {"file_path": str(p)}})
    for c in cmds:
        items.append({"type": "tool_use", "name": "Bash", "input": {"command": c}})
    lines.append({"type": "assistant", "timestamp": ts, "message": {"content": items}})
    p = SCR / f"tx_{len(results)}_{int(time.time()*1000)}.jsonl"
    p.write_text("\n".join(json.dumps(l) for l in lines), encoding="utf-8")
    return str(p)


def hook(name, payload):
    t0 = time.time()
    r = subprocess.run([sys.executable, str(HOOKS / name)], input=json.dumps(payload).encode("utf-8"),
                       capture_output=True, env=dict(os.environ, PYTHONUTF8="1"))
    return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace"), time.time() - t0


def check(label, cond, extra=""):
    results.append((label, cond))
    print(("PASS " if cond else "FAIL ") + label + (("  | " + extra) if (extra and not cond) else ""))


def pre(tool, inp, transcript):
    return hook("pretool.py", {"tool_name": tool, "tool_input": inp, "transcript_path": transcript, "session_id": "t"})


note = str(V / "Characters" / "NPCs" / "Teste Novo.md")

# T1: sem skill -> bloqueia
rc, o, e, _ = pre("Write", {"file_path": note, "content": "x"}, tl())
check("T1 gravar sem skill é bloqueado", rc == 2 and "nenhuma skill" in e, e)

# T2: isenções
rc, *_ = pre("Write", {"file_path": str(V / ".claude" / "x.md"), "content": "x"}, tl())
check("T2a .claude isento", rc == 0)
rc, *_ = pre("Write", {"file_path": str(SCR / "fora.md"), "content": "x"}, tl())
check("T2b fora do projeto isento", rc == 0)

# T3: organizer progressivo
rc, o, e, _ = pre("Write", {"file_path": note, "content": "x"}, tl(skill="campaign-organizer"))
check("T3a organizer sem template/esquema bloqueia", rc == 2 and "_Template_" in e, e)
tools = [V / "_Templates" / "_Template_NPC.md", V / "_meta" / "entity-types.md",
         V / "_meta" / "relationship-types.md", V / "_meta" / "index.md"]
rc, o, e, _ = pre("Write", {"file_path": note, "content": "x"}, tl(tools=tools, skill="campaign-organizer"))
check("T3b ainda falta version gate", rc == 2 and "version" in e, e)
rc, o, e, _ = pre("Write", {"file_path": note, "content": "x"},
                  tl(tools=tools, skill="campaign-organizer", cmds=['py gma.py vault-check "V" version']))
check("T3c organizer completo passa", rc == 0, e)

# T4: o relatório da auditoria completa saiu dos gates antigos (ablação 2026-11-19): o fluxo campaign-qa cuida
rep = str(V / "_QA" / "QA_full_audit_2026-11-17.md")
rc, o, e, _ = pre("Write", {"file_path": rep, "content": "x"}, tl(skill="campaign-qa"))
check("T4 gate antigo não barra mais o relatório", rc == 0, e)

# T5: comandos
rc, o, e, _ = pre("Bash", {"command": 'py "C:\\x\\gma.py" stamp-entities "V" "a.md" --set a=1 --write'}, tl())
check("T5a comando de gravação gma sem skill bloqueia", rc == 2, e)
rc, o, e, _ = pre("Bash", {"command": 'py "C:\\x\\gma.py" vault-check "V" all'}, tl())
check("T5b leitura (vault-check all) livre", rc == 0, e)
rc, o, e, _ = pre("Bash", {"command": 'py gma.py publish deploy --verify'},
                  tl(skill="publish-site", cmds=['gma vault-check V version']))
check("T5c deploy sem publish-played bloqueia", rc == 2 and "publish-played" in e, e)

# T6: gate de conteúdo (PostToolUse)
broken = V / "Characters" / "NPCs" / "Quebrada.md"
broken.write_text("---\ntype: npc\nname: [aberto\nrelationships: tudo errado\n---\n# x\n", encoding="utf-8")
rc, o, e, dt = hook("posttool.py", {"tool_name": "Write", "tool_input": {"file_path": str(broken)},
                                    "transcript_path": tl(), "session_id": "t6"})
check("T6a nota quebrada é apontada", rc == 2 and "GATE DE CONTEÚDO" in e, e + o)
print("   tempo:", round(dt, 1), "s | stderr:", e[:400].replace("\n", " / "))
good = V / "Characters" / "PCs" / "Chris.md"
rc, o, e, dt = hook("posttool.py", {"tool_name": "Edit", "tool_input": {"file_path": str(good)},
                                    "transcript_path": tl(), "session_id": "t6"})
check("T6b nota limpa passa em silêncio", rc == 0 and not e.strip(), e)
print("   tempo:", round(dt, 1), "s")
for i in range(4):
    rc, *_ = hook("posttool.py", {"tool_name": "Write", "tool_input": {"file_path": str(broken)},
                                  "transcript_path": tl(), "session_id": "t6"})
check("T6c depois de 3 tentativas para de insistir", rc == 0)

# T7/T8 (Stop e checklist) saíram na ablação de 2026-11-19; o flow_hook faz os dois (test_flow.py).

# T9: robustez
r = subprocess.run([sys.executable, str(HOOKS / "pretool.py")], input=b"isso nao e json", capture_output=True)
check("T9a entrada inválida falha aberta", r.returncode == 0)
(V / ".claude" / "harness" / "OFF").write_text("x")
rc, *_ = pre("Write", {"file_path": note, "content": "x"}, tl())
check("T9b arquivo OFF desliga", rc == 0)
(V / ".claude" / "harness" / "OFF").unlink()

bad = [l for l, c in results if not c]
print(f"\n{len(results) - len(bad)}/{len(results)} ok")
print("falhas:", bad)
log = V / ".claude" / "harness" / "hook-errors.log"
print("hook-errors.log:", log.read_text(encoding="utf-8") if log.exists() else "(vazio)")
shutil.rmtree(SCR, ignore_errors=True)
sys.exit(1 if bad else 0)
