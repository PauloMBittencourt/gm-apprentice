"""Marca uma pasta como vault do gm-apprentice com o harness ligado, e aponta os hooks para ela.

O harness só age num vault (tem _meta/vault-state.json) e só bloqueia quando o vault tem
.claude/harness/modes.json. Os testes rodam num vault descartável, nunca no vault real.
"""
import atexit
import os
import shutil
import tempfile
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[1] / "modes.example.json"


def mark(root: Path) -> Path:
    (root / "_meta").mkdir(parents=True, exist_ok=True)
    (root / "_meta" / "vault-state.json").write_text("{}", encoding="utf-8")
    data = root / ".claude" / "harness"
    data.mkdir(parents=True, exist_ok=True)
    if not (data / "modes.json").exists():
        shutil.copy(EXAMPLE, data / "modes.json")
    os.environ["CLAUDE_PROJECT_DIR"] = str(root)
    return root


def make() -> Path:
    tmp = tempfile.mkdtemp(prefix="gmavault_")
    atexit.register(shutil.rmtree, tmp, ignore_errors=True)
    return mark(Path(tmp) / "vault")
