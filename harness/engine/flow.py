"""Motor mínimo de fluxos (MVP; ver ../MVP.md).

O estado NÃO é lido de um arquivo: é recalculado a cada chamada a partir do transcript
da sessão (evidência medida por fora) e do disco (artefatos). Átomos de evidência:
read, run, read_min, artifact, human.
"""
from __future__ import annotations

import json
import re
from fnmatch import fnmatch
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

PROJECT = paths.PROJECT

CMD_TOOLS = {"Bash", "PowerShell", "mcp__terminal__run_in_terminal"}
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
READ_VERBS = re.compile(r"\b(cat|head|tail|sed|awk|type|more|less|bat|xargs|Get-Content|gc)\b", re.I)
_NOTE_DIRS = (r"(?:Chapters|Characters|Locations|Factions & Organizations|Items|Creatures|"
              r"Organizations|Events|_Campaign|_World|_meta)")
NOTE_REL = re.compile(r"^" + _NOTE_DIRS + r"/.+\.md$", re.I)
NOTE_PATH = re.compile(r"(?:^|[\s\"'=/])(" + _NOTE_DIRS + r"/[^\"'\n;|&<>*?]*?\.md)", re.I)
STATUS_OK = {"COMPLETO", "PARCIAL", "NAO_AVALIADO"}
SEVERITIES = {"CRITICAL", "ERROR", "WARNING", "INFO"}


# ------------------------------------------------------------------ utilidades

def norm(s) -> str:
    return str(s).replace("\\", "/").lower()


def rel(project, p):
    if not p:
        return None
    try:
        return Path(p).resolve().relative_to(Path(project).resolve()).as_posix()
    except Exception:
        return None


def _strings(o, out):
    if isinstance(o, str):
        out.append(o)
    elif isinstance(o, dict):
        for v in o.values():
            _strings(v, out)
    elif isinstance(o, list):
        for v in o:
            _strings(v, out)


def blob(inp) -> str:
    parts: list = []
    _strings(inp, parts)
    return norm("\n".join(parts))


def make_event(i, name, inp, tool_id=None) -> dict:
    return {"i": i, "kind": "tool", "id": tool_id, "name": name, "input": inp or {}, "blob": blob(inp)}


def load_events(transcript_path):
    """Lê o JSONL da sessão. Devolve (eventos em ordem, {tool_use_id: is_error})."""
    events: list = []
    results: dict = {}
    if not transcript_path or not Path(transcript_path).exists():
        return events, results
    with open(transcript_path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            content = (obj.get("message") or {}).get("content")
            kind = obj.get("type")
            if kind == "assistant" and isinstance(content, list):
                for it in content:
                    if it.get("type") == "tool_use":
                        events.append(make_event(len(events), it.get("name", ""), it.get("input"), it.get("id")))
            elif kind == "user" and not obj.get("isMeta"):
                if isinstance(content, str):
                    events.append({"i": len(events), "kind": "user", "text": content})
                elif isinstance(content, list):
                    for it in content:
                        if it.get("type") == "text":
                            events.append({"i": len(events), "kind": "user", "text": it.get("text", "")})
                        elif it.get("type") == "tool_result":
                            results[it.get("tool_use_id")] = bool(it.get("is_error"))
    return events, results


def _is_human_text(text: str) -> bool:
    t = (text or "").strip()
    return bool(t) and not t.startswith("<command-") and not t.startswith("<system-reminder>") \
        and not t.startswith("Caveat:") and not t.startswith("[Request interrupted")


def flow_active(events, prompt: str = "", skill: str = "qa-passo") -> bool:
    if prompt.strip().lstrip("/").split(":")[-1].startswith(skill) and prompt.strip().startswith("/"):
        return True
    for e in events:
        if e["kind"] == "tool" and e["name"] == "Skill" and \
                str(e["input"].get("skill", "")).split(":")[-1] == skill:
            return True
        if e["kind"] == "user" and re.search(r"<command-name>/?(?:[\w-]+:)?" + re.escape(skill) + r"</command-name>",
                                             e.get("text", "")):
            return True
    return False


def flow_file(skill: str):
    """O fluxo local do vault vence o do plugin."""
    return next((d / f"{skill}.json" for d in paths.flow_dirs() if (d / f"{skill}.json").is_file()), None)


def all_skills() -> list:
    return sorted({p.stem for d in paths.flow_dirs() for p in d.glob("*.json")})


def load_spec(skill: str) -> dict:
    return json.loads(flow_file(skill).read_text(encoding="utf-8"))


def _skill_of(name: str):
    n = str(name or "").strip().lstrip("/").split(":")[-1].split()[0] if str(name or "").strip() else ""
    return n if n and flow_file(n) else None


def find_activation(events, prompt: str = ""):
    """Skill de fluxo ativada mais recentemente: (skill, texto_da_ativação, índice) ou None.
    Ativa por: comando do usuário (/skill ... ou <command-name>), ferramenta Skill, ou o prompt atual."""
    best = None
    for e in events:
        if e["kind"] == "tool" and e["name"] == "Skill":
            sk = _skill_of(e["input"].get("skill"))
            if sk:
                best = (sk, str(e["input"].get("args", "")), e["i"])
        elif e["kind"] == "user":
            m = re.search(r"<command-name>/?([\w:.-]+)</command-name>", e.get("text", ""))
            if m and _skill_of(m.group(1)):
                best = (_skill_of(m.group(1)), e.get("text", ""), e["i"])
    p = (prompt or "").strip()
    if p.startswith("/") and _skill_of(p[1:]):
        best = (_skill_of(p[1:]), p, len(events))
    return best


def select_mode(spec: dict, text: str) -> str:
    for mode, rx in (spec.get("mode_triggers") or {}).items():
        if mode in spec["modes"] and re.search(rx, text or "", re.I):
            return mode
    d = spec.get("mode_default")
    return d if d in spec["modes"] else next(iter(spec["modes"]))


def enforcing(spec: dict, mode: str) -> bool:
    """Rascunho = só observa (registra e orienta, não bloqueia). Validado/mvp = bloqueia nos modos listados."""
    if spec.get("status") not in ("mvp", "validado"):
        return False
    return mode in (spec.get("enforce_modes") or list(spec["modes"]))


def notes_read(events, project) -> list:
    """Notas do vault lidas: [(índice, caminho_relativo_minúsculo)], sem repetição, em ordem.
    Conta a ferramenta Read e comandos de leitura com caminho explícito. Curingas e `cd` + `*.md` NÃO contam."""
    seen: dict = {}
    for e in events:
        if e["kind"] != "tool":
            continue
        if e["name"] == "Read":
            r = rel(project, e["input"].get("file_path"))
            if r and NOTE_REL.match(r):
                seen.setdefault(r.lower(), e["i"])
        elif e["name"] in CMD_TOOLS:
            cmd = str(e["input"].get("command", ""))
            if READ_VERBS.search(cmd):
                for m in NOTE_PATH.finditer(cmd.replace("\\", "/")):
                    seen.setdefault(m.group(1).lower(), e["i"])
    return sorted(((i, p) for p, i in seen.items()))


# ------------------------------------------------------------------ átomos

def _first(events, pred):
    for e in events:
        if pred(e):
            return e["i"]
    return None


def _is_readish(e) -> bool:
    return e["kind"] == "tool" and e["name"] not in WRITE_TOOLS and e["name"] not in ("Skill", "ToolSearch")


def atom_read(atom, events):
    paths = atom["read"]
    if atom.get("if_exists") or atom.get("if_existing_vault"):
        # só exigido se o alvo existir no vault; caminho curto de skill ("x/y.md") nunca é checado no disco
        if atom.get("if_existing_vault") and not scope_notes(PROJECT):
            return True, None, {"type": "read", "msg": ""}
        if atom.get("if_exists") and not any((PROJECT / p).exists() for p in paths):
            return True, None, {"type": "read", "msg": ""}
    idxs = [_first(events, lambda e, p=norm(p): _is_readish(e) and p in e["blob"]) for p in paths]
    if atom.get("any"):
        found = [i for i in idxs if i is not None]
        return (bool(found), min(found) if found else None,
                {"type": "read", "msg": "ler um destes: " + ", ".join(paths)})
    missing = [p for p, i in zip(paths, idxs) if i is None]
    ok = not missing
    return (ok, max(idxs) if ok else None, {"type": "read", "msg": "ler " + ", ".join(missing)})


def atom_run(atom, events, results):
    rx = atom["run"]
    idx = _first(events, lambda e: e["kind"] == "tool" and e["name"] in CMD_TOOLS
                 and re.search(rx, str(e["input"].get("command", "")), re.I)
                 and not results.get(e.get("id"), False))
    return (idx is not None, idx, {"type": "run", "msg": f"rodar um comando que case com /{rx}/"})


def atom_read_min(atom, events, project):
    n = atom["read_min"]
    nr = notes_read(events, project)
    ok = len(nr) >= n
    return (ok, nr[n - 1][0] if ok else None,
            {"type": "read_min", "msg": f"ler mais {n - len(nr)} notas com a ferramenta Read (lidas: {len(nr)}/{n})"})


ARTIFACT_HELP = (" (frontmatter: passo, status COMPLETO|PARCIAL|NAO_AVALIADO, motivo se não completo, "
                 "examinados: [notas lidas]; depois um bloco por achado: `### A1 [WARNING] título`, "
                 "`arquivo:`, `linha:`, `trecho:` copiado LITERAL da nota, `proposta:`)")


def atom_artifact(atom, events, results, project):
    pat = atom["artifact"].lower()
    last = None
    for e in events:
        if e["kind"] == "tool" and e["name"] in WRITE_TOOLS:
            r = rel(project, e["input"].get("file_path") or e["input"].get("notebook_path"))
            raw = norm(e["input"].get("file_path") or e["input"].get("notebook_path") or "")
            if r and fnmatch(r.lower(), pat):
                last = (e["i"], r)
            elif "/" not in pat and raw and fnmatch(raw.rsplit("/", 1)[-1], pat):
                last = (e["i"], raw)
    if not last:
        return False, None, {"type": "artifact", "msg": f"gravar {atom['artifact']}"
                             + (ARTIFACT_HELP if atom.get("validate", pat.startswith("_qa/.run/")) else "")}
    if atom.get("validate", pat.startswith("_qa/.run/")):
        errs = validate_artifact(Path(project) / last[1], events, project, atom)
        if errs:
            return False, None, {"type": "artifact", "msg": f"corrigir {last[1]}: " + "; ".join(errs[:3])}
    return True, last[0], {"type": "artifact", "msg": ""}


def atom_lint(atom, events, results, project):
    """'tocados': depois da última gravação no vault, uma checagem `vault-check` bem-sucedida."""
    last_write = None
    for e in events:
        if e["kind"] != "tool":
            continue
        if e["name"] in WRITE_TOOLS:
            r = rel(project, e["input"].get("file_path") or e["input"].get("notebook_path"))
            if r and NOTE_REL.match(r):
                last_write = e["i"]
        elif e["name"] in CMD_TOOLS and re.search(r"vault-write|batch.*--write|wrapup-add|index-build.*--write",
                                                  str(e["input"].get("command", "")), re.I)                 and not results.get(e.get("id"), False):
            last_write = e["i"]
    if last_write is None:
        return True, None, {"type": "lint", "msg": ""}
    idx = _first(events, lambda e: e["kind"] == "tool" and e["name"] in CMD_TOOLS and e["i"] > last_write
                 and re.search(r"vault-check", str(e["input"].get("command", "")), re.I)
                 and not results.get(e.get("id"), False))
    return (idx is not None, idx,
            {"type": "lint", "msg": "rodar `gma vault-check` depois da última gravação e corrigir todo ERROR"})


def atom_human(atom, events, after):
    idx = _first(events, lambda e: e["kind"] == "user" and e["i"] > after and _is_human_text(e.get("text", "")))
    return (idx is not None, idx, {"type": "human", "msg": "esperar uma mensagem do mestre"})


def eval_atom(atom, events, results, project, after):
    if "read" in atom:
        return atom_read(atom, events)
    if "run" in atom:
        return atom_run(atom, events, results)
    if "read_min" in atom:
        return atom_read_min(atom, events, project)
    if "artifact" in atom:
        return atom_artifact(atom, events, results, project)
    if "human" in atom:
        return atom_human(atom, events, after)
    if "lint" in atom:
        return atom_lint(atom, events, results, project)
    return True, None, {"type": "?", "msg": ""}


# ------------------------------------------------------------------ fluxo

def load_steps(skill: str, mode: str) -> list:
    return load_spec(skill)["modes"][mode]


def _when_ok(when, project) -> bool:
    if not when:
        return True
    if "dir_exists" in when:
        return (Path(project) / when["dir_exists"]).is_dir()
    return True


def evaluate(steps, events, results, project):
    """Devolve (lista de passos com estado, passo atual ou None)."""
    after = -1
    out, current = [], None
    for st in steps:
        if not _when_ok(st.get("when"), project):
            out.append({"id": st["id"], "title": st.get("title", ""), "state": "skip", "missing": []})
            continue
        missing, idxs = [], []
        for atom in st["evidence"]:
            ok, idx, why = eval_atom(atom, events, results, project, after)
            if ok:
                if idx is not None:
                    idxs.append(idx)
            else:
                missing.append(why)
        rec = {"id": st["id"], "title": st.get("title", ""), "state": "open" if missing else "done",
               "missing": missing}
        out.append(rec)
        if not missing:
            after = max([after] + idxs)
        elif current is None:
            current = rec
    return out, current


def human_only(step) -> bool:
    return bool(step) and bool(step["missing"]) and all(m["type"] == "human" for m in step["missing"])


def status_text(skill: str, out, current) -> str:
    active = [s for s in out if s["state"] != "skip"]
    done = [s for s in active if s["state"] == "done"]
    skipped = [s["id"] for s in out if s["state"] == "skip"]
    head = f"[flow {skill}] {len(done)}/{len(active)} passos concluídos."
    if skipped:
        head += " Pulados por condição: " + ", ".join(skipped) + "."
    if not current:
        return head + " Todos os passos têm evidência. Pode concluir."
    idx = [s["id"] for s in active].index(current["id"]) + 1
    nxt = next((s for s in active[idx:] if s["state"] != "done"), None)
    lines = [head, f"Passo atual {idx}/{len(active)}: {current['id']} ({current['title']}).", "Falta:"]
    lines += [f"- {m['msg']}" for m in current["missing"]]
    if nxt:
        lines.append(f"Depois: {nxt['id']} ({nxt['title']}).")
    return "\n".join(lines)


# ------------------------------------------------------------------ artefato

def _fm(text: str):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        return None, text
    fm: dict = {}
    key = None
    for line in m.group(1).splitlines():
        if re.match(r"^\s*-\s+", line) and key:
            fm.setdefault(key, []).append(re.sub(r"^\s*-\s+", "", line).strip().strip("\"'"))
            continue
        kv = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if kv:
            key, val = kv.group(1), kv.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                fm[key] = [x.strip().strip("\"'") for x in val[1:-1].split(",") if x.strip()]
            elif val == "":
                fm[key] = []
            else:
                fm[key] = val.strip("\"'")
    return fm, m.group(2)


def _ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def scope_notes(project) -> set:
    """Notas do vault no escopo da auditoria (mesmos diretórios que contam como leitura de nota)."""
    out = set()
    root = Path(project)
    for d in ("Chapters", "Characters", "Locations", "Factions & Organizations", "Items", "Creatures",
              "Organizations", "Events", "_Campaign", "_World", "_meta"):
        base = root / d
        if base.is_dir():
            for p in base.rglob("*.md"):
                r = rel(root, p)
                if r:
                    out.add(r.lower())
    return out


def validate_artifact(path: Path, events, project, opts=None) -> list:
    """Erros escritos para a IA ler. Lista vazia = válido.
    opts: {"complete_needs_pct": N} => `status: COMPLETO` exige N% das notas do escopo examinadas."""
    path = Path(path)
    if not path.is_file():
        return [f"o arquivo {path.name} não existe"]
    fm, body = _fm(path.read_text(encoding="utf-8", errors="replace"))
    errs: list = []
    if fm is None:
        return ["falta o frontmatter (--- passo, status, examinados ---) no topo do arquivo"]
    if not fm.get("passo"):
        errs.append("frontmatter sem `passo:`")
    status = str(fm.get("status", "")).upper()
    if status not in STATUS_OK:
        errs.append("`status:` deve ser COMPLETO, PARCIAL ou NAO_AVALIADO")
    if status in ("PARCIAL", "NAO_AVALIADO") and not fm.get("motivo"):
        errs.append(f"`status: {status}` exige `motivo:` (diga o que não foi coberto e por quê)")
    exam = fm.get("examinados") or []
    if status != "NAO_AVALIADO" and not exam:
        errs.append("`examinados:` vazio (liste as notas que você leu neste passo)")
    lidas = {p for _, p in notes_read(events, project)}
    for x in exam:
        if norm(x).strip() not in lidas:
            errs.append(f"`examinados` cita {x}, mas essa nota não aparece em nenhuma leitura (use a ferramenta Read nela)")
    pct = (opts or {}).get("complete_needs_pct")
    if pct and status == "COMPLETO":
        escopo = scope_notes(project)
        have = len({norm(x).strip() for x in exam} & lidas & escopo)
        if escopo and have * 100 < pct * len(escopo):
            errs.append(f"`status: COMPLETO` exige {pct}% das {len(escopo)} notas do escopo examinadas "
                        f"(você examinou {have}). Declare `status: PARCIAL` com `motivo:` dizendo quanto foi coberto, "
                        f"ou leia mais notas com Read")
    for blk in re.split(r"(?m)^###\s+", body)[1:]:
        head, _, rest = blk.partition("\n")
        hm = re.match(r"([A-Z]\d+)\s+\[(\w+)\]", head.strip())
        if not hm:
            errs.append(f"cabeçalho de achado inválido: `### {head.strip()[:50]}` (use `### A1 [WARNING] título`)")
            continue
        aid, sev = hm.group(1), hm.group(2).upper()
        if sev not in SEVERITIES:
            errs.append(f"{aid}: severidade {sev} inválida (CRITICAL, ERROR, WARNING, INFO)")
        f = {k: v.strip() for k, v in re.findall(r"(?m)^(arquivo|linha|trecho|proposta):\s*(.*)$", rest)}
        if not f.get("arquivo") or not f.get("trecho") or not f.get("linha", "").isdigit():
            errs.append(f"{aid}: faltam `arquivo:`, `linha:` (número) ou `trecho:`")
            continue
        if norm(f["arquivo"]) not in lidas:
            errs.append(f"{aid}: cita {f['arquivo']}, que não foi lido com a ferramenta Read")
        target = Path(project) / f["arquivo"]
        if not target.is_file():
            errs.append(f"{aid}: o arquivo {f['arquivo']} não existe")
            continue
        lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
        n = int(f["linha"])
        window = _ws(" ".join(lines[max(0, n - 4): n + 3]))
        quote = _ws(f["trecho"].strip().strip("\"“”'"))
        if quote not in window:
            errs.append(f"{aid}: o trecho não está em {f['arquivo']} perto da linha {n} "
                        f"(copie o texto LITERAL da nota; não resuma)")
    return errs[:12]
