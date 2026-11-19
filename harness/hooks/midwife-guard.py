"""PreToolUse guard: blocks any write into _midwife/ outside the-midwife's file structure.
Exit 2 = blocked (stderr goes back to Claude)."""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "engine"))
import paths  # noqa: E402

if paths.off() or not paths.opted_in():   # só bloqueia; vale no vault que ligou o harness
    sys.exit(0)

TOPIC = r"(index|discoveries|chapter-shape|weather-atmosphere|cover-stories|social-events|romance-threads)\.md"
FOLDERS = r"(adventures|npcs|entity-sketches|image-prompts|session-0)/[^/]+\.md"
SEEDS = r"seeds/(premises|npcs|locations|hooks|tone|mechanics)/[^/]+\.md"
ALLOWED = re.compile(rf"^(index\.md|{SEEDS}|[^/]+/{TOPIC}|[^/]+/{FOLDERS})$")
STRUCTURE = ("_midwife/index.md; _midwife/seeds/{premises,npcs,locations,hooks,tone,mechanics}/*.md; "
             "_midwife/{aventura}/{index,discoveries,chapter-shape,weather-atmosphere,cover-stories,"
             "social-events,romance-threads}.md; _midwife/{aventura}/{adventures,npcs,entity-sketches,"
             "image-prompts,session-0}/*.md")

def block(msg):
    print(f"BLOQUEADO pelo mestre: {msg}\nEstrutura permitida da the-midwife: {STRUCTURE}", file=sys.stderr)
    sys.exit(2)

def single_note_delete(seg):
    """`rm`, `git rm` ou `Remove-Item` de UM caminho .md dentro de _midwife/, sem -r, curinga nem metacaractere."""
    s = seg.strip()
    if re.search(r"[<>&$`|*?;]", s):
        return False
    m = re.fullmatch(r"(?:git\s+rm|rm|Remove-Item)(?:\s+-(?:f|LiteralPath))?\s+(\"[^\"]+\"|'[^']+'|\S+)", s, re.I)
    if not m:
        return False
    path = m.group(1).strip("\"'")
    return bool(re.search(r"(?:^|[/\\])_midwife[/\\]", path)) and path.lower().endswith(".md")


data = json.load(sys.stdin)
tool, inp = data.get("tool_name", ""), data.get("tool_input", {})

if tool in ("Write", "Edit", "NotebookEdit", "MultiEdit"):
    path = (inp.get("file_path") or inp.get("notebook_path") or "").replace("\\", "/")
    m = re.search(r"(?:^|/)_midwife/(.*)$", path)
    if m and not ALLOWED.match(m.group(1)):
        block(f"'{m.group(1)}' nao faz parte da estrutura da the-midwife.")
elif tool in ("Bash", "PowerShell"):
    # harmless redirections (2>/dev/null, 2>&1, >$null) are not writes
    cmd = re.sub(r"\d*>\s*(/dev/null|&\d|\$null)", "", inp.get("command", ""))
    # Gravar em _midwife pelo shell é proibido; as ferramentas Write/Edit são o único caminho.
    # A checagem é por SEGMENTO do comando (separado por ; && || | e quebra de linha): só bloqueia
    # quando o próprio segmento que cita _midwife (ou o prefixo _mid, contra abreviações) grava nele.
    # Citar a pasta numa busca (grep -v _midwife) ou mandar a saída para outro lugar não é gravação.
    verbs = (r"\b(tee|mv|cp|rm|rmdir|mkdir|touch|rename|ren|del|erase|ln|truncate|dd|"
             r"Set-Content|Out-File|Add-Content|Move-Item|Copy-Item|Remove-Item|New-Item|"
             r"Rename-Item|Clear-Content)\b|\bsed\s+-\S*i")
    pywrite = (r"open\(|write_text|write_bytes|shutil\.|os\.(remove|rename|makedirs|unlink)|\.unlink|"
               r"--write|--apply|--execute|--fix")
    for seg in re.split(r";|&&|\|\||\||\n", cmd):
        if not re.search(r"_mid", seg, re.I):
            continue
        # A skill manda tirar o que foi superado: apagar UMA nota (sem -r, sem curinga) é permitido; o git guarda.
        if single_note_delete(seg):
            continue
        if (re.search(r">>?\s*[\"']?[^\s\"'|;&]*_mid", seg, re.I)
                or re.search(verbs, seg, re.I)
                or (re.search(r"python|\.py\b|\bpy\b", seg, re.I) and re.search(pywrite, seg))):
            block("gravar em _midwife pelo shell e proibido; use Write/Edit dentro da estrutura da skill.")
sys.exit(0)
