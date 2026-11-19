"""Testes do gate de forma (hooks/form_gate.py). Roda com `py -3 tests/test_form_gate.py`.

Os cenários vêm do incidente de 2026-11-18: resposta longa em forma de relatório e mais de uma pergunta
no Worldbuilding do ttrpg-expert.
"""
import json
import subprocess
import sys
import uuid
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[1]
GATE = HARNESS / "hooks" / "form_gate.py"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _vault  # noqa: E402
_vault.make()
sys.path.insert(0, str(HARNESS / "hooks"))
import confirm_gate as cg  # noqa: E402
import form_gate as fg  # noqa: E402

CURTA = "Gravei. O LaCroix já sabe quem são os agentes do Petrodon?"
DUAS = "A Gloria responde ao LaCroix? E o Victor Girard, ainda controla a imprensa?"
LONGA = "Relatório da malha política. " * 60 + "Seguimos?"
PROPOSTA_CITADA = "Proponho gravar:\n\n" + "\n".join(["> Linha longa do texto exato a gravar no politica.md."] * 40) + \
                  "\n\nPosso gravar?"


def ev(*items):
    out = []
    for i, it in enumerate(items):
        k, rest = it[0], it[1:]
        if k == "skill":
            out.append(dict(seq=i, ev="skill", skill=rest[0], text=rest[1] if len(rest) > 1 else ""))
        else:
            out.append(dict(seq=i, ev=k, text=rest[0]))
    return out


# ------------------------------------------------------------- função pura

def test_curta_uma_pergunta_ok():
    assert fg.violations(CURTA, 900) == []


def test_duas_perguntas_viola():
    assert any("perguntas" in v for v in fg.violations(DUAS, 900))


def test_longa_viola():
    assert any("caracteres" in v for v in fg.violations(LONGA, 900))


def test_proposta_citada_nao_conta():
    assert fg.violations(PROPOSTA_CITADA, 900) == []


def test_interrogacao_dentro_de_codigo_nao_conta():
    assert fg.violations("Rodei:\n```\nls ?? x?\n```\nPosso seguir?", 900) == []


def test_midwife_sempre_conversa():
    assert fg.in_conversation(ev(("skill", "the-midwife"))) == "the-midwife"


def test_ttrpg_expert_consulta_de_regra_nao_e_conversa():
    assert fg.in_conversation(ev(("skill", "ttrpg-expert"), ("user", "quanto custa Rapidez no V20?"))) is None


def test_ttrpg_expert_worldbuilding_pela_fala_do_mestre():
    evs = ev(("skill", "ttrpg-expert"), ("user", "vamos montar a política de LA"))
    assert fg.in_conversation(evs) == "ttrpg-expert"


def test_skill_fora_da_lista_nao_e_conversa():
    assert fg.in_conversation(ev(("skill", "campaign-qa"), ("user", "política"))) is None


def test_ultima_skill_vence():
    assert fg.in_conversation(ev(("skill", "the-midwife"), ("skill", "campaign-qa"))) is None


# ------------------------------------------------------------- ponta a ponta

def hook(payload):
    r = subprocess.run([sys.executable, str(GATE)], input=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                       capture_output=True)
    out = r.stdout.decode("utf-8").strip()
    return r.returncode, (json.loads(out) if out else None)


def test_ponta_a_ponta():
    sid = "teste-" + uuid.uuid4().hex[:8]
    try:
        stop = {"hook_event_name": "Stop", "session_id": sid, "stop_hook_active": False}
        assert hook({**stop, "last_assistant_message": DUAS})[1] is None       # sem skill ativa: não mexe
        hook({"hook_event_name": "UserPromptSubmit", "session_id": sid, "prompt": "/the-midwife nova crônica"})
        rc, out = hook({**stop, "last_assistant_message": DUAS})
        assert rc == 0 and out["decision"] == "block" and "perguntas" in out["reason"]
        rc, out = hook({**stop, "stop_hook_active": True, "last_assistant_message": DUAS})
        assert out.get("decision") is None and "systemMessage" in out          # não bloqueia duas vezes
        assert hook({**stop, "last_assistant_message": CURTA})[1] is None
        hook({"hook_event_name": "PostToolUse", "session_id": sid, "tool_name": "Skill",
              "tool_input": {"skill": "gm-apprentice:campaign-qa"}})
        assert hook({**stop, "last_assistant_message": LONGA})[1] is None      # QA não é conversa guiada
        kinds = [e["ev"] for e in cg.events(sid)]
        assert kinds.count("form_blocked") == 1 and kinds.count("form_unresolved") == 1
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
