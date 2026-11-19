"""Onde mora cada coisa: o código e os fluxos vêm do plugin; estado, logs e escolhas vêm do vault.

  CODE     <plugin>/harness         motor, hooks, flows/*.json, skills.json (padrão)
  PROJECT  o vault aberto            CLAUDE_PROJECT_DIR, ou a pasta atual
  DATA     <vault>/.claude/harness   modes.json, state/, observe.log, hook-errors.log, OFF,
                                     flows/*.json e skills.json locais (vencem os do plugin)

O vault liga os bloqueios criando DATA/modes.json (mesmo que seja só `{}`). Sem ele, tudo só observa.
"""
import os
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
PROJECT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()
DATA = PROJECT / ".claude" / "harness"


def is_vault() -> bool:
    return (PROJECT / "_meta" / "vault-state.json").is_file()


def opted_in() -> bool:
    return (DATA / "modes.json").is_file()


def off() -> bool:
    """Desligado: não é vault do gm-apprentice, ou o mestre criou DATA/OFF."""
    return not is_vault() or (DATA / "OFF").exists()


def config(name: str) -> Path:
    local = DATA / name
    return local if local.is_file() else CODE / name


def flow_dirs() -> list:
    return [d for d in (DATA / "flows", CODE / "flows") if d.is_dir()]
