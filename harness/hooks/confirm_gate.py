"""Gate de escrita confirmada: só grava no vault o texto que o mestre VIU e RESPONDEU.

Origem: incidente de 2026-11-18 (Worldbuilding do ttrpg-expert gravou a "malha do livro" inteira em
_World/politica.md sem passar ponto a ponto). Ver PLANO-CORRECAO-WORLDBUILDING.md, passo 1.

Um único script, registrado em três eventos (despacha por hook_event_name):
  Stop             -> grava a PROPOSTA: o texto final da resposta (last_assistant_message, não o transcript,
                      que a doc diz poder chegar atrasado).
  UserPromptSubmit -> grava o TURNO DO MESTRE (texto e ordem).
  PreToolUse       -> antes de Write/Edit/MultiEdit em pasta protegida, exige:
                      (1) um turno do mestre depois de uma proposta;
                      (2) que esse turno não seja uma negação ("não", "calma", "espera"...);
                      (3) que cada linha NOVA de conteúdo esteja contida na proposta que o mestre viu.
                      Shell gravando em pasta protegida: sempre barrado (o caminho é Write/Edit).

Por que o modelo não engana: o estado (state/confirm-<sessão>.jsonl) é escrito SÓ por este hook,
em modo acréscimo, a partir do que o Claude Code entrega no stdin. O modelo não tem caneta nele.

Modo por pasta, em <vault>/.claude/harness/modes.json (sem o arquivo: observe): `confirmacao@_World`, `confirmacao@_midwife` (off|observe|enforce).
Só biblioteca padrão, de propósito. Falha aberta: erro do próprio gate vai para hook-errors.log, exit 0.
"""
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "engine"))
import paths  # noqa: E402

try:                       # Windows: stdout em cp1252 derruba o "⚠" da mensagem
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HARNESS = paths.DATA
PROJECT = paths.PROJECT
STATE = HARNESS / "state"
PROTECTED = {"_World": "enforce", "_midwife": "observe"}   # padrão quando o modes.json não diz nada
WRITE_TOOLS = {"Write", "Edit", "MultiEdit"}
SHELL_TOOLS = {"Bash", "PowerShell", "mcp__terminal__run_in_terminal"}
# "Não toque no nome, pode gravar o resto" é aceite: a negação vale só sem um "pode gravar/seguir..." depois.
ACCEPT = re.compile(r"[,.;:!]\s*(?:e\s+|mas\s+)?pode\s+(?:gravar|seguir|salvar|botar|colocar|escrever)\b", re.I)
REFUSE = re.compile(r"\bn[ãa]o\s+pode\s+(?:gravar|seguir|salvar|botar|colocar|escrever)\b", re.I)
NEGATION = re.compile(r"^\W*(n[ãa]o\b|calma|espera|pera\b|errado|errou|pare\b|para\s+(?:a[ií]|tudo)|nada disso|cancela)",
                      re.I)
SHELL_VERBS = (r"\b(tee|mv|cp|rm|rmdir|mkdir|touch|rename|ren|del|erase|ln|truncate|dd|Set-Content|Out-File|"
               r"Add-Content|Move-Item|Copy-Item|Remove-Item|New-Item|Rename-Item|Clear-Content)\b|\bsed\s+-\S*i")
PY_WRITE = r"open\(|write_text|write_bytes|shutil\.|os\.(remove|rename|makedirs|unlink)|\.unlink|--write|--apply"


# ------------------------------------------------------------------ infra

def read_stdin() -> dict:
    # Windows: o Python lê o stdin com a code page ANSI; o Claude Code manda UTF-8 (acentos do vault quebrariam).
    return json.loads(sys.stdin.buffer.read().decode("utf-8", errors="replace") or "{}")


def log_error(exc):
    try:
        with open(HARNESS / "hook-errors.log", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} confirm_gate: {type(exc).__name__}: {exc}\n")
    except Exception:
        pass


def ledger_path(sid) -> Path:
    return STATE / f"confirm-{re.sub(r'[^A-Za-z0-9_-]', '_', str(sid or 'sem-sessao'))}.jsonl"


class Lock:
    """Lock por arquivo (O_CREAT|O_EXCL): hooks rodam em paralelo; sem isso o log sai fora de ordem."""

    def __init__(self, path: Path):
        self.p = path.with_suffix(".lock")

    def __enter__(self):
        for _ in range(200):                      # até ~4 s
            try:
                os.close(os.open(self.p, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
                return self
            except FileExistsError:
                try:                              # lock órfão (processo morreu): libera depois de 10 s
                    if time.time() - self.p.stat().st_mtime > 10:
                        self.p.unlink()
                except OSError:
                    pass
                time.sleep(0.02)
        return self                               # falha aberta: segue sem lock

    def __exit__(self, *a):
        try:
            self.p.unlink()
        except OSError:
            pass


def append(sid, ev: str, **fields):
    p = ledger_path(sid)
    p.parent.mkdir(parents=True, exist_ok=True)
    with Lock(p):
        seq = sum(1 for _ in open(p, encoding="utf-8")) if p.exists() else 0
        line = json.dumps({"seq": seq, "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "ev": ev, **fields},
                          ensure_ascii=False)
        with open(p, "a", encoding="utf-8", newline="\n") as f:
            f.write(line + "\n")
            f.flush()


def events(sid) -> list:
    p = ledger_path(sid)
    if not p.exists():
        return []
    out = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(ln))
        except ValueError:
            pass                                  # linha truncada não derruba o gate
    return out


def mode_for(folder: str) -> str:
    if not paths.opted_in():
        return "observe"
    try:
        cfg = json.loads((HARNESS / "modes.json").read_text(encoding="utf-8"))
    except Exception:
        cfg = {}
    return cfg.get(f"confirmacao@{folder}") or PROTECTED[folder]


# ------------------------------------------------------------------ texto

def norm(s: str) -> str:
    """Tira o que muda entre chat e arquivo sem mudar o sentido: markdown, links, espaços, caixa."""
    s = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", s)       # [[Nota|apelido]] -> apelido
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)              # [texto](url) -> texto
    s = re.sub(r"[\[\]*_`~]", "", s)                            # ênfase some sem deixar espaço ("**1997**.")
    s = re.sub(r"[#>|]", " ", s)                                # citação, título e tabela viram espaço
    s = re.sub(r"^\s*(?:[-+•]|\d+[.)])\s+", "", s)            # marcador de lista
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("—", "-").replace("–", "-")
    return re.sub(r"\s+", " ", s).strip().lower()


def content_lines(text: str) -> list:
    """Linhas que carregam conteúdo. Ficam de fora: frontmatter, títulos, separadores de tabela, vazias."""
    lines, in_fm = [], False
    for i, raw in enumerate(text.splitlines()):
        st = raw.strip()
        if st == "---" and (i == 0 or in_fm):
            in_fm = not in_fm
            continue
        if in_fm or not st or st.startswith("#") or re.fullmatch(r"[|:\-\s]+", st):
            continue
        n = norm(st)
        if n:
            lines.append((st, n))
    return lines


def new_text(tool: str, inp: dict, path: Path) -> str:
    """O que a escrita ACRESCENTA (linhas que já estavam no arquivo não precisam de nova confirmação)."""
    if tool == "Edit":
        pairs = [(inp.get("old_string", ""), inp.get("new_string", ""))]
    elif tool == "MultiEdit":
        pairs = [(e.get("old_string", ""), e.get("new_string", "")) for e in inp.get("edits", [])]
    else:
        try:
            old = path.read_text(encoding="utf-8")
        except OSError:
            old = ""
        pairs = [(old, inp.get("content", ""))]
    out = []
    for old, new in pairs:
        before = {n for _, n in content_lines(old)}
        out += [raw for raw, n in content_lines(new) if n not in before]
    return "\n".join(out)


def protected_folder(path_str: str):
    rel = path_str.replace("\\", "/")
    try:
        rel = Path(path_str).resolve().relative_to(PROJECT.resolve()).as_posix()
    except Exception:
        pass
    if re.search(r"(?:^|/)(?:world-)?index\.md$", rel):     # índice só lista e liga notas: não é texto de mundo
        return None
    for folder in PROTECTED:
        if re.search(rf"(?:^|/){folder}/", rel):
            return folder
    return None


# ------------------------------------------------------------------ decisão

def check(evs: list, added: str):
    """Devolve None (pode gravar) ou o motivo da recusa. Função pura: é ela que os testes exercitam."""
    if not added.strip():
        return None
    last_user = next((e for e in reversed(evs) if e["ev"] == "user"), None)
    if last_user is None:
        return "Não houve nenhum turno do mestre nesta sessão. Mostre o texto e pergunte antes de gravar."
    proposal = next((e for e in reversed(evs) if e["ev"] == "proposal" and e["seq"] < last_user["seq"]), None)
    if proposal is None:
        return "O mestre ainda não viu nenhuma proposta. Mostre o texto exato que vai gravar e espere a resposta."
    said = last_user.get("text", "")
    if REFUSE.search(said) or (NEGATION.search(said) and not ACCEPT.search(said)):
        return (f"A última resposta do mestre não é um aceite (\"{last_user['text'][:60]}\"). "
                "Ajuste a proposta e pergunte de novo.")
    seen = norm(proposal.get("text", ""))
    missing = [raw for raw, n in content_lines(added) if n not in seen]
    if missing:
        amostra = "; ".join(f"\"{m[:70]}\"" for m in missing[:3])
        return (f"{len(missing)} linha(s) não estavam na proposta que o mestre viu: {amostra}. "
                "Grave só o que foi mostrado; o resto, mostre e pergunte antes.")
    return None


def emit(decision_msg: str, folder: str, tool: str):
    m = mode_for(folder)
    if m == "off":
        return
    if m == "observe":
        try:
            with open(HARNESS / "observe.log", "a", encoding="utf-8") as f:
                f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "guard": f"confirmacao@{folder}",
                                    "tool": tool, "would_block": decision_msg[:400]}, ensure_ascii=False) + "\n")
        except Exception:
            pass
        return
    print(json.dumps({
        "systemMessage": f"⚠ harness: escrita em {folder}/ barrada (sem confirmação do mestre).",
        "hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                               "permissionDecisionReason": f"[confirmacao] {decision_msg}"},
    }, ensure_ascii=False))


def on_pretool(data: dict):
    tool, inp = data.get("tool_name", ""), data.get("tool_input") or {}
    if tool in WRITE_TOOLS:
        path = inp.get("file_path") or ""
        folder = protected_folder(path)
        if folder:
            msg = check(events(data.get("session_id")), new_text(tool, inp, Path(path)))
            if msg:
                emit(msg, folder, tool)
    elif tool in SHELL_TOOLS:
        cmd = re.sub(r"\d*>\s*(/dev/null|&\d|\$null)", "", inp.get("command", ""))
        for seg in re.split(r";|&&|\|\||\||\n", cmd):
            for folder in PROTECTED:
                if folder == "_midwife" or not re.search(folder[:4], seg, re.I):
                    continue          # _midwife pelo shell já é barrado pelo midwife-guard.py
                if (re.search(rf">>?\s*[\"']?[^\s\"'|;&]*{folder[:4]}", seg, re.I) or re.search(SHELL_VERBS, seg, re.I)
                        or (re.search(r"python|\.py\b|\bpy\b", seg, re.I) and re.search(PY_WRITE, seg))):
                    emit(f"gravar em {folder}/ pelo shell é proibido; use Write/Edit, que passam pela confirmação.",
                         folder, tool)
                    return


def main():
    data = read_stdin()
    ev, sid = data.get("hook_event_name", ""), data.get("session_id")
    if ev == "Stop":
        txt = data.get("last_assistant_message") or ""
        if txt.strip():
            append(sid, "proposal", text=txt)
    elif ev == "UserPromptSubmit":
        append(sid, "user", text=data.get("prompt") or "")
    elif ev == "PreToolUse":
        on_pretool(data)


if __name__ == "__main__":
    try:
        if not paths.off():
            main()
    except Exception as exc:          # falha aberta: bug do gate nunca trava o projeto
        log_error(exc)
    sys.exit(0)
