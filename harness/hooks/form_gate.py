"""Gate de forma: nas conversas guiadas, uma pergunta por mensagem e mensagem curta.

Origem: incidente de 2026-11-18 (Worldbuilding com mensagens longas, em forma de relatório).
Ver PLANO-CORRECAO-WORLDBUILDING.md, passo 2.

Por que código e não juiz LLM: contar "?" e caracteres é determinístico, barato e não erra por
cansaço em trace longo (TRAIL: 11% de acerto de juízes LLM). Então pode bloquear.

Eventos:
  PostToolUse(Skill) -> registra a skill carregada pelo modelo (e o texto de ativação, para saber o modo).
  UserPromptSubmit   -> registra skill chamada por slash (/the-midwife ...), que NÃO dispara a ferramenta Skill.
  Stop               -> mede a última resposta (last_assistant_message). Se viola: block UMA vez.
                        Com stop_hook_active=true (já está corrigindo por causa de um block), libera e só
                        registra: bloquear de novo não força nada e o Claude Code corta após 8 blocks.

A skill ativa vem do ledger do confirm_gate (state/confirm-<sessão>.jsonl), que só os hooks escrevem;
não do transcript, que a doc avisa poder chegar atrasado.

Modo por skill em <vault>/.claude/harness/modes.json (sem o arquivo: observe): `forma@the-midwife`, `forma@ttrpg-expert` (off|observe|enforce).
Limites em ../modes.json: `forma.max_chars` (padrão 900). Linhas citadas (> ...) e blocos de código
não contam: é ali que vai o texto exato proposto para gravar, que pode ser longo.
"""
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import confirm_gate as cg  # noqa: E402  (ledger, lock, leitura UTF-8)

HARNESS = cg.HARNESS
# skill -> regex do modo conversacional sobre o texto de ativação (None = a skill inteira é conversa)
CONVERSA = {
    "the-midwife": None,
    "ttrpg-expert": r"worldbuild|mundo|pol[ií]tica|fac[cç][aã]o|_World",
}
PADRAO = {"the-midwife": "enforce", "ttrpg-expert": "enforce"}
SLASH = re.compile(r"^\s*/(?:gm-apprentice:)?([a-z][\w-]*)\s*(.*)", re.S | re.I)


def cfg() -> dict:
    try:
        return json.loads((HARNESS / "modes.json").read_text(encoding="utf-8"))
    except Exception:
        return {}


def active(evs: list):
    """(skill, texto de ativação + turnos do mestre desde então) da última skill registrada, ou None.
    Os turnos entram porque o modelo costuma carregar a skill sem argumentos: o modo vem da conversa."""
    i = next((i for i in range(len(evs) - 1, -1, -1) if evs[i]["ev"] == "skill"), None)
    if i is None:
        return None
    falas = [e.get("text", "") for e in evs[i:] if e["ev"] == "user"]
    return evs[i]["skill"], "\n".join([evs[i].get("text", "")] + falas)


def in_conversation(evs: list):
    a = active(evs)
    if not a or a[0] not in CONVERSA:
        return None
    rx = CONVERSA[a[0]]
    if rx and not re.search(rx, a[1] or "", re.I):
        return None
    return a[0]


def body(text: str) -> str:
    """Texto que conta para a forma: sem blocos de código e sem linhas citadas (a proposta para gravar)."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith(">"))


def violations(text: str, max_chars: int) -> list:
    b = body(text)
    out = []
    perguntas = len(re.findall(r"\?+", b))
    if perguntas > 1:
        out.append(f"{perguntas} perguntas na mesma mensagem; deixe só UMA")
    n = len(b.strip())
    if n > max_chars:
        out.append(f"mensagem com {n} caracteres (limite {max_chars}); encurte, sem relatório")
    return out


def on_stop(data: dict):
    sid = data.get("session_id")
    evs = cg.events(sid)
    skill = in_conversation(evs)
    if not skill:
        return
    c = cfg()
    mode = c.get(f"forma@{skill}") or (PADRAO[skill] if cg.paths.opted_in() else "observe")
    if mode == "off":
        return
    v = violations(data.get("last_assistant_message") or "", int(c.get("forma.max_chars") or 900))
    if not v:
        return
    msg = f"[forma {skill}] " + "; ".join(v) + "."
    if mode == "observe":
        with open(HARNESS / "observe.log", "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "guard": f"forma@{skill}",
                                "would_block": msg}, ensure_ascii=False) + "\n")
        return
    if data.get("stop_hook_active"):
        cg.append(sid, "form_unresolved", skill=skill, why=msg)   # já bloqueou uma vez: libera e registra
        print(json.dumps({"systemMessage": f"⚠ harness: resposta ainda fora da forma ({'; '.join(v)})."},
                         ensure_ascii=False))
        return
    cg.append(sid, "form_blocked", skill=skill, why=msg)
    print(json.dumps({
        "decision": "block",
        "reason": msg + " Reescreva a resposta inteira já na forma da skill: curta, uma pergunta só. "
                        "Texto para gravar vai citado (linhas começando com >).",
        "systemMessage": f"⚠ harness: resposta refeita — {'; '.join(v)}.",
    }, ensure_ascii=False))


def main():
    data = cg.read_stdin()
    ev, sid = data.get("hook_event_name", ""), data.get("session_id")
    if ev == "PostToolUse" and data.get("tool_name") == "Skill":
        inp = data.get("tool_input") or {}
        name = str(inp.get("skill") or inp.get("command") or "").split(":")[-1]
        if name:
            cg.append(sid, "skill", skill=name, text=str(inp.get("args") or ""), via="tool")
    elif ev == "UserPromptSubmit":
        m = SLASH.match(data.get("prompt") or "")
        if m:
            cg.append(sid, "skill", skill=m.group(1).lower(), text=m.group(2), via="slash")
    elif ev == "Stop":
        on_stop(data)


if __name__ == "__main__":
    try:
        if not cg.paths.off():
            main()
    except Exception as exc:          # falha aberta
        cg.log_error(exc)
    sys.exit(0)
