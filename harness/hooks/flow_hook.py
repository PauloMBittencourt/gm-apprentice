"""Hook único do motor de fluxos: UserPromptSubmit, PreToolUse, PostToolUse e Stop.

Serve a TODAS as skills que têm arquivo em ../flows/<skill>.json. A skill ativa (a ativada por último), o
modo e as regras próprias vêm do JSON do fluxo (chave "hook"), não do código. Falha aberta (ver harness.run).

Guardas (cada uma com modo off | observe | enforce):
  flow.artifact  artefato de passo reprovado pelo validador
  flow.report    gravar o arquivo final antes de todos os passos (só se o fluxo declara `hook.report_write`)
  flow.stop      encerrar com passo pendente
  flow.protect   editar os "juízes" (harness, skills, settings, CLAUDE.md) durante o fluxo ou adulterá-los
Precedência do modo: <vault>/.claude/harness/modes.json `guarda@skill` > `guarda` > padrão da skill
(enforce se o fluxo está `mvp`/`validado` e o modo é um dos `enforce_modes`; senão observe).
Vault sem modes.json: tudo em observe.
Em observe NÃO bloqueia: registra em ../observe.log o que bloquearia (e continua orientando o modelo).
"""
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "engine"))

import paths  # noqa: E402
import judges  # noqa: E402  (só stdlib: funciona mesmo com o resto do harness corrompido)

try:
    import flow  # noqa: E402
    from harness import HARNESS, PROJECT, block, load_input, load_state, rel_to_project, run, save_state  # noqa: E402
    HARNESS_OK = True
except Exception:  # um juiz corrompido (ex.: skills.json) derrubaria tudo em silêncio: o modo degradado acusa
    HARNESS_OK = False

RUN_DIR = "_QA/.run/"
MAX_STOP_BLOCKS = 2

# O que o fluxo não pode alterar: o próprio harness, as skills do vault, a configuração e as regras do vault.
PROTECTED_REL = [r"^\.claude/harness/", r"^\.claude/skills/", r"^\.claude/settings(\.local)?\.json$", r"^CLAUDE\.md$"]
PROTECTED_IN_CMD = r"(\.claude[/\\]harness|plugins[/\\]cache[/\\]gm-apprentice|\.claude[/\\]skills|settings(\.local)?\.json|CLAUDE\.md)"
WRITE_VERBS = (r"\b(tee|mv|cp|rm|rmdir|mkdir|touch|rename|ren|del|erase|ln|truncate|dd|Set-Content|Out-File|"
               r"Add-Content|Move-Item|Copy-Item|Remove-Item|New-Item|Rename-Item|Clear-Content)\b|\bsed\s+-\S*i")
PY_WRITE = (r"open\(|write_text|write_bytes|shutil\.|os\.(remove|rename|makedirs|unlink)|\.unlink|"
            r"--write|--apply|--execute|--fix")

CUR = {"skill": "?", "default": "enforce"}


def emit_context(event: str, text: str):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}},
                     ensure_ascii=False))


def mode(guard: str) -> str:
    """modes.json `guarda@skill` > `guarda` > padrão da skill."""
    if not paths.opted_in():
        return "observe"
    try:
        cfg = json.loads((HARNESS / "modes.json").read_text(encoding="utf-8"))
    except Exception:
        return "enforce"
    return cfg.get(f"{guard}@{CUR['skill']}") or cfg.get(guard) or CUR["default"]


def decide(guard: str, msg: str):
    """enforce: bloqueia. observe: só registra. off: ignora."""
    m = mode(guard)
    if m == "off":
        return
    if m == "observe":
        try:
            with open(HARNESS / "observe.log", "a", encoding="utf-8") as f:
                f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "skill": CUR["skill"], "guard": guard,
                                    "would_block": msg[:400]}, ensure_ascii=False) + "\n")
        except Exception:
            pass
        return
    block(msg)


def protected_write_path(rel: str) -> bool:
    return any(re.search(p, rel) for p in PROTECTED_REL)


def plugin_code(path_str: str) -> bool:
    """O código do harness agora mora no plugin, fora do vault."""
    if not path_str:
        return False
    try:
        Path(path_str).resolve().relative_to(paths.CODE)
        return True
    except (ValueError, OSError):
        return False


def protected_command(cmd: str) -> bool:
    for seg in re.split(r";|&&|\|\||\||\n", cmd):
        if not re.search(PROTECTED_IN_CMD, seg, re.I):
            continue
        if re.search(r">>?\s*[\"']?[^\s\"'|;&]*" + PROTECTED_IN_CMD, seg, re.I) \
                or re.search(WRITE_VERBS, seg, re.I) \
                or (re.search(r"python|\.py\b|\bpy\b", seg, re.I) and re.search(PY_WRITE, seg)):
            return True
    return False


def writes_final(cmd: str, final_rx: str) -> bool:
    """O comando grava um arquivo que casa com o padrão do arquivo final? (heurística: nome base + verbo de escrita)"""
    base = final_rx.strip("^$").split("/")[-1]
    stem = re.sub(r"\\\.\w+$", "", base).replace(".*", "")      # "QA_full_audit_.*\.md" -> "QA_full_audit_"
    if not stem or stem not in cmd:
        return False
    return bool(re.search(r">>?", cmd) or re.search(WRITE_VERBS, cmd, re.I) or re.search(PY_WRITE, cmd))


def main():
    d = load_input()
    ev_name = d.get("hook_event_name") or ""
    tool = d.get("tool_name") or ""
    inp = d.get("tool_input") or {}
    sid = d.get("session_id")
    prompt = str(d.get("prompt", ""))

    events, results = flow.load_events(d.get("transcript_path"))
    if ev_name in ("PreToolUse", "PostToolUse") and tool:
        events.append(flow.make_event(len(events), tool, inp, d.get("tool_use_id")))
    act = flow.find_activation(events, prompt)
    if not act:
        return
    skill, act_text, _ = act
    CUR["skill"] = skill
    try:
        spec = flow.load_spec(skill)
        flow_mode = flow.select_mode(spec, act_text)
        CUR["default"] = "enforce" if flow.enforcing(spec, flow_mode) else "observe"
    except Exception:          # fluxo corrompido: a adulteração é acusada antes de qualquer outra coisa
        spec, flow_mode = None, None
        CUR["default"] = "enforce"

    judges.ensure(sid)
    changed = judges.changed(sid)
    if changed and ev_name in ("PostToolUse", "Stop"):
        decide("flow.protect", judges.message(changed))
    if spec is None:
        return

    hk = spec.get("hook") or {}
    report_rx = hk.get("report_write")
    final_step = hk.get("final_step", "relatorio")
    if flow_mode not in (hk.get("report_modes") or [flow_mode]):
        report_rx = None

    steps = spec["modes"][flow_mode]
    out, current = flow.evaluate(steps, events, results, PROJECT)
    status = flow.status_text(f"{skill}:{flow_mode}", out, current)
    st = load_state(sid)
    fs = st.setdefault("flow", {"last": None, "stop": 0})
    tag = f"flow {skill}"

    if ev_name == "UserPromptSubmit":
        emit_context("UserPromptSubmit", status)
        fs["last"] = current["id"] if current else "fim"
        save_state(sid, st)
        return

    if ev_name == "PreToolUse":
        if tool in flow.WRITE_TOOLS:
            fp = inp.get("file_path") or inp.get("notebook_path") or ""
            r = rel_to_project(fp) or ""
            if protected_write_path(r) or plugin_code(fp):
                decide("flow.protect",
                       f"BLOQUEADO pelo harness ({tag}): {r} faz parte dos juízes (harness, skills, configuração) "
                       "e não pode ser editado enquanto o fluxo roda. Só o mestre altera isso, fora do fluxo.")
            if report_rx and re.match(report_rx, r):
                pend = [s for s in out if s["state"] == "open" and s["id"] != final_step]
                if pend:
                    decide("flow.report",
                           f"BLOQUEADO pelo harness ({tag}): o arquivo final só é gravado depois de todos os "
                           "passos anteriores terem evidência. Pendentes: "
                           + ", ".join(s["id"] for s in pend) + ".\n" + status)
        elif tool in flow.CMD_TOOLS:
            cmd = str(inp.get("command", ""))
            if report_rx and writes_final(cmd, report_rx):
                pend = [s for s in out if s["state"] == "open" and s["id"] != final_step]
                if pend:
                    decide("flow.report", f"BLOQUEADO pelo harness ({tag}): o arquivo final só é gravado depois de "
                           "todos os passos anteriores terem evidência. Pendentes: "
                           + ", ".join(s["id"] for s in pend))
            if protected_command(cmd):
                decide("flow.protect",
                       f"BLOQUEADO pelo harness ({tag}): este comando grava em arquivos dos juízes "
                       "(harness, skills, configuração, CLAUDE.md). Isso não é permitido durante o fluxo.")
        return

    if ev_name == "PostToolUse":
        if tool in flow.WRITE_TOOLS:
            r = rel_to_project(inp.get("file_path") or inp.get("notebook_path")) or ""
            if r.startswith(RUN_DIR) and r.endswith(".md"):
                opts = next((a for s in steps for a in s["evidence"]
                             if "artifact" in a and flow.fnmatch(r.lower(), a["artifact"].lower())), None)
                if opts is not None and opts.get("validate", True):
                    errs = flow.validate_artifact(PROJECT / r, events, PROJECT, opts)
                    if errs:
                        decide("flow.artifact",
                               f"[{tag}] {r} não passou na validação:\n" + "\n".join(f"- {e}" for e in errs)
                               + "\nCorrija o arquivo; a validação roda de novo ao salvar.")
        marker = current["id"] if current else "fim"
        if marker != fs.get("last"):
            fs["last"] = marker
            save_state(sid, st)
            emit_context("PostToolUse", status)
        return

    if ev_name == "Stop":
        if not current or flow.human_only(current):
            return
        if fs.get("stop", 0) >= MAX_STOP_BLOCKS:
            return
        if mode("flow.stop") == "enforce":
            fs["stop"] = fs.get("stop", 0) + 1
            save_state(sid, st)
        decide("flow.stop", f"[GATE DE FECHAMENTO {tag}] O fluxo ainda não terminou. Não encerre.\n" + status)


def degraded():
    """Harness quebrado: só confere a adulteração (linha de base já existente) e deixa o resto passar."""
    try:
        d = json.load(sys.stdin)
        ch = judges.changed(d.get("session_id"))
        if ch and d.get("hook_event_name") in ("PostToolUse", "Stop") and paths.opted_in():
            sys.stderr.write(judges.message(ch) + " (o harness em si está quebrado: " + ", ".join(ch) + ")")
            sys.exit(2)
    except SystemExit:
        raise
    except Exception:
        pass


if paths.off():
    sys.exit(0)
elif HARNESS_OK:
    run(main)
else:
    degraded()
