import json, subprocess, sys
from pathlib import Path

import _vault

G = str(Path(__file__).resolve().parents[1] / "hooks" / "midwife-guard.py")
P = str(_vault.make())
res = []


def run(tool, inp):
    r = subprocess.run([sys.executable, G], input=json.dumps({"tool_name": tool, "tool_input": inp}).encode(),
                       capture_output=True)
    return r.returncode


def case(label, tool, inp, expect):
    rc = run(tool, inp)
    ok = (rc == expect)
    res.append(ok)
    print(("PASS " if ok else "FAIL ") + f"{label} (rc={rc}, esperado {expect})")


B = "Bash"
# devem PASSAR (leitura, ou citar a pasta só para excluir)
case("grep -v _midwife com saida em TMP (o caso real do relatorio)", B,
     {"command": 'find . -name "*.md" | grep -v "^./_midwife" > "$TMP/stale.txt"; python3 gma.py vault-check . names'}, 0)
case("gma vault-check sem citar a pasta", B, {"command": 'python3 "x/gma.py" vault-check . names'}, 0)
case("ls _midwife", B, {"command": "ls _midwife"}, 0)
case("cat de arquivo do _midwife com saida em /tmp", B, {"command": "cat _midwife/index.md > /tmp/out.txt"}, 0)
case("grep dentro de _midwife", B, {"command": 'grep -rn "Bell" _midwife/'}, 0)
case("redirecionamento inofensivo", B, {"command": "ls _midwife 2>/dev/null"}, 0)
# devem BLOQUEAR
case("redirecionamento para _midwife", B, {"command": "echo oi > _midwife/x.md"}, 2)
case("append em _midwife", B, {"command": "echo oi >> _midwife/index.md"}, 2)
case("cp para _midwife", B, {"command": "cp a.md _midwife/b.md"}, 2)
case("rm em _midwife", B, {"command": "rm -rf _midwife/seeds"}, 2)
case("sed -i em _midwife", B, {"command": "sed -i s/a/b/ _midwife/index.md"}, 2)
case("tee em _midwife", B, {"command": "echo oi | tee _midwife/z.md"}, 2)
case("python escrevendo em _midwife", B, {"command": "python3 -c \"open('_midwife/a','w').write('x')\""}, 2)
case("gma --write citando _midwife", B, {"command": 'python3 gma.py vault-write . note-new "_midwife/x.md" --write'}, 2)
case("abreviacao _mid* (o contorno do relatorio)", B, {"command": "echo oi > _mid*/x.md"}, 2)
case("PowerShell Set-Content", "PowerShell", {"command": "Set-Content _midwife/a.md 'x'"}, 2)
# ferramentas de arquivo (comportamento original)
case("Write fora da estrutura", "Write", {"file_path": P + r"\_midwife\teste.txt", "content": "x"}, 2)
case("Write dentro da estrutura", "Write", {"file_path": P + r"\_midwife\seeds\hooks\novo.md", "content": "x"}, 0)
case("Write fora do _midwife", "Write", {"file_path": P + r"\Characters\NPCs\Teste.md", "content": "x"}, 0)

print(f"\n{sum(res)}/{len(res)} ok")
sys.exit(0 if all(res) else 1)
