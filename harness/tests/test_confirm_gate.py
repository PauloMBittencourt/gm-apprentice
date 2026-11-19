"""Testes do gate de escrita confirmada (hooks/confirm_gate.py).

Cada cenário reproduz um pedaço do incidente de 2026-11-18. Roda com `py -3 tests/test_confirm_gate.py`
(ou pytest). Os testes de ponta a ponta chamam o script de verdade pelo stdin, como o Claude Code faz.
"""
import json
import subprocess
import sys
import uuid
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[1]
GATE = HARNESS / "hooks" / "confirm_gate.py"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _vault  # noqa: E402
PROJECT = _vault.make()
sys.path.insert(0, str(HARNESS / "hooks"))
import confirm_gate as cg  # noqa: E402

PROPOSTA = """Proponho gravar isto no politica.md:

> Gloria Martinez e os outros agentes do Petrodon estão parados desde 1997.
> Ninguém falou com eles. LaCroix veio justamente para amarrar essas pontas.

Posso gravar?"""
ARQUIVO = "## Agentes do Petrodon\n\n- Gloria Martinez e os outros agentes do Petrodon estão parados desde 1997.\n"


def ev(*items):
    return [dict(seq=i, ev=k, text=t) for i, (k, t) in enumerate(items)]


# ------------------------------------------------------------- função pura

def test_sem_turno_do_mestre_nega():
    assert cg.check(ev(("proposal", PROPOSTA)), ARQUIVO)


def test_sem_proposta_antes_nega():
    assert cg.check(ev(("user", "faz a política")), ARQUIVO)


def test_texto_proposto_e_aceito_passa():
    assert cg.check(ev(("proposal", PROPOSTA), ("user", "pode gravar")), ARQUIVO) is None


def test_linha_a_mais_nega():
    extra = ARQUIVO + "- Mariel espiona o Fortier a mando do Geduld.\n"
    msg = cg.check(ev(("proposal", PROPOSTA), ("user", "pode")), extra)
    assert msg and "Mariel" in msg


def test_negacao_do_mestre_nega():
    for resp in ("calma, não é isso", "Não grava ainda", "espera", "errado, o Petrodon morreu"):
        assert cg.check(ev(("proposal", PROPOSTA), ("user", resp)), ARQUIVO), resp


def test_proposta_depois_do_turno_nao_vale():
    # o modelo escreveu a proposta e já foi gravar no mesmo turno, sem o mestre ver
    evs = ev(("user", "pode seguir"), ("proposal", PROPOSTA))
    assert cg.check(evs, ARQUIVO)


def test_so_titulo_e_frontmatter_passam():
    assert cg.check(ev(("proposal", PROPOSTA), ("user", "ok")), "---\nstatus: DRAFT\n---\n## Seção nova\n") is None


def test_wikilink_e_lista_normalizam():
    arq = "1. [[Gloria Martinez|Gloria Martinez]] e os outros agentes do Petrodon estão parados desde **1997**.\n"
    assert cg.check(ev(("proposal", PROPOSTA), ("user", "ok")), arq) is None


def test_edit_conta_so_o_que_foi_acrescentado(tmp_path=None):
    inp = {"old_string": "- Linha antiga que ninguém confirmou hoje.",
           "new_string": "- Linha antiga que ninguém confirmou hoje.\n- LaCroix veio justamente para amarrar essas pontas."}
    added = cg.new_text("Edit", inp, Path("x"))
    assert "antiga" not in added and "LaCroix" in added


# ------------------------------------------------------------- ponta a ponta

def hook(payload):
    r = subprocess.run([sys.executable, str(GATE)], input=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                       capture_output=True)
    out = r.stdout.decode("utf-8").strip()
    return r.returncode, (json.loads(out) if out else None)


def write_payload(sid, content):
    return {"hook_event_name": "PreToolUse", "session_id": sid, "tool_name": "Write",
            "tool_input": {"file_path": str(PROJECT / "_World" / "__teste_gate__.md"), "content": content}}


def test_ponta_a_ponta():
    sid = "teste-" + uuid.uuid4().hex[:8]
    try:
        rc, out = hook(write_payload(sid, ARQUIVO))                     # nada visto ainda
        assert rc == 0 and out["hookSpecificOutput"]["permissionDecision"] == "deny"
        hook({"hook_event_name": "Stop", "session_id": sid, "last_assistant_message": PROPOSTA})
        hook({"hook_event_name": "UserPromptSubmit", "session_id": sid, "prompt": "pode gravar"})
        rc, out = hook(write_payload(sid, ARQUIVO))                     # visto e aceito
        assert rc == 0 and out is None
        rc, out = hook(write_payload(sid, ARQUIVO + "- Texto inventado agora.\n"))
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
        rc, out = hook({"hook_event_name": "PreToolUse", "session_id": sid, "tool_name": "Bash",
                        "tool_input": {"command": "echo x >> _World/politica.md"}})
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
        rc, out = hook({"hook_event_name": "PreToolUse", "session_id": sid, "tool_name": "Bash",
                        "tool_input": {"command": "grep -rn Gloria _World/"}})
        assert out is None                                              # ler não é gravar
        rc, out = hook({"hook_event_name": "PreToolUse", "session_id": sid, "tool_name": "Write",
                        "tool_input": {"file_path": str(PROJECT / "Characters" / "x.md"), "content": "livre"}})
        assert out is None                                              # fora das pastas protegidas
    finally:
        for p in (cg.ledger_path(sid), cg.ledger_path(sid).with_suffix(".lock")):
            p.unlink(missing_ok=True)


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("PASS", name)
            except Exception as e:
                fails += 1
                print("FAIL", name, type(e).__name__, e)
    sys.exit(1 if fails else 0)
