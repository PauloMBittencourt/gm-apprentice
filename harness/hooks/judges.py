"""Detecção de adulteração dos "juízes" (só biblioteca padrão, de propósito: precisa funcionar mesmo
quando o resto do harness foi corrompido).

Juízes: o harness do plugin (código e fluxos), .claude/harness do vault (sem estado/logs), .claude/skills,
settings(.local).json e CLAUDE.md.
A linha de base (hash de cada arquivo) é gravada na primeira vez que a auditoria é vista na sessão;
depois, qualquer diferença é adulteração, por qualquer meio (Bash, python, git, PowerShell...).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "engine"))
import paths  # noqa: E402

HARNESS = paths.DATA
PROJECT = paths.PROJECT
SKIP_DIRS = {"state", "__pycache__", "testes", "pesquisa", "tests"}
SKIP_FILES = {"hook-errors.log", "observe.log", ".planted.json"}


def hashes() -> dict:
    files = [PROJECT / ".claude" / "settings.json", PROJECT / ".claude" / "settings.local.json", PROJECT / "CLAUDE.md"]
    for r in (paths.CODE, HARNESS, PROJECT / ".claude" / "skills"):
        if r.is_dir():
            files += [f for f in r.rglob("*") if f.is_file() and not (set(f.relative_to(r).parts) & SKIP_DIRS)
                      and f.name not in SKIP_FILES]
    out = {}
    for f in files:
        try:
            out[_key(f)] = hashlib.sha1(f.read_bytes()).hexdigest()
        except OSError:
            pass
    return out


def _key(f: Path) -> str:
    try:
        return f.relative_to(PROJECT).as_posix()
    except ValueError:                       # código do plugin, fora do vault
        return "plugin/" + f.relative_to(paths.CODE.parent).as_posix()


def _path(sid) -> Path:
    return HARNESS / "state" / f"judges-plugin-{re.sub(r'[^A-Za-z0-9_-]', '_', str(sid))}.json"


def ensure(sid):
    p = _path(sid)
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(hashes()), encoding="utf-8")


def changed(sid) -> list:
    """Arquivos que mudaram desde a linha de base; [] se não há linha de base."""
    p = _path(sid)
    if not p.exists():
        return []
    try:
        base = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return ["(linha de base ilegível)"]
    now = hashes()
    return sorted(k for k in set(base) | set(now) if base.get(k) != now.get(k))


def message(files) -> str:
    return ("[flow] Os juízes (harness, skills, configuração) foram ALTERADOS durante o fluxo: " + ", ".join(files)
            + ". Reverta o conteúdo (ex.: git checkout -- <arquivo>) e avise o mestre; sem isso a auditoria não vale.")
