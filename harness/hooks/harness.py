"""Harness do gm-apprentice: gates determinísticos para as skills do gm-apprentice.

Entradas (scripts finos que chamam run(<funcao>)):
  pretool.py  -> pre_main   (PreToolUse):  skill obrigatória + gates de leitura/comando antes de gravar
  posttool.py -> post_main  (PostToolUse): gate de conteúdo (vault-check) a cada nota gravada
A checklist e o Stop saíram na ablação de 2026-11-19: o motor de fluxos (flow_hook.py) faz os dois.

Falha aberta: qualquer erro do próprio harness vira linha em hook-errors.log e exit 0,
para um bug aqui nunca travar o projeto. Para desligar tudo: crie .claude/harness/OFF no vault.
Estes gates só valem num vault que ligou o harness (tem .claude/harness/modes.json); ver engine/paths.py.
"""
import glob
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

for _s in (sys.stdin, sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "engine"))
import paths  # noqa: E402

HARNESS = paths.DATA          # estado e logs moram no vault
PROJECT = paths.PROJECT
CFG = json.loads(paths.config("skills.json").read_text(encoding="utf-8"))

WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
CMD_TOOLS = {"Bash", "PowerShell", "mcp__terminal__run_in_terminal"}
SKILLS = set(CFG["skills"])

READ_VERBS = re.compile(r"\b(cat|head|tail|sed|awk|type|more|less|bat|xargs|Get-Content|gc)\b", re.I)
NOTE_PATH = re.compile(
    r"(?:^|[\s\"'=/])((?:Chapters|Characters|Locations|Factions & Organizations|Items|Creatures|"
    r"Organizations|Events|_Campaign|_World|_meta)/[^\"'\n;|&<>*?]*?\.md)", re.I)


# ---------------------------------------------------------------- infra

def log_error(where, exc):
    try:
        with open(HARNESS / "hook-errors.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} {where}: {type(exc).__name__}: {exc}\n")
    except Exception:
        pass


def run(main, needs_opt_in=False):
    """needs_opt_in: gate que só bloqueia (sem modo observe); roda só no vault que ligou o harness."""
    try:
        if paths.off() or (needs_opt_in and not paths.opted_in()):
            sys.exit(0)
        main()
    except SystemExit:
        raise
    except Exception as exc:  # falha aberta
        log_error(getattr(main, "__name__", "main"), exc)
        sys.exit(0)


def load_input():
    return json.load(sys.stdin)


def norm(s):
    return str(s).replace("\\", "/").lower()


def rel_to_project(p):
    if not p:
        return None
    try:
        return Path(p).resolve().relative_to(PROJECT.resolve()).as_posix()
    except Exception:
        return None


def any_re(patterns, text):
    return any(re.search(p, text) for p in patterns)


def block(msg):
    print(msg, file=sys.stderr)
    sys.exit(2)


def state_path(sid):
    d = HARNESS / "state"
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{re.sub(r'[^A-Za-z0-9_-]', '_', sid or 'sem-sessao')}.json"


def load_state(sid):
    try:
        return json.loads(state_path(sid).read_text(encoding="utf-8"))
    except Exception:
        return {"content": {}}


def save_state(sid, st):
    try:
        state_path(sid).write_text(json.dumps(st), encoding="utf-8")
    except Exception as exc:
        log_error("save_state", exc)


# ---------------------------------------------------------------- transcript

def _strings(o, out):
    if isinstance(o, str):
        out.append(o)
    elif isinstance(o, dict):
        for v in o.values():
            _strings(v, out)
    elif isinstance(o, list):
        for v in o:
            _strings(v, out)


class Session:
    def __init__(self, transcript_path):
        self.tools = []        # (nome, input, texto_normalizado)
        self.user_texts = []
        self.first_ts = None
        self.last_text = ""
        if not transcript_path or not os.path.exists(transcript_path):
            return
        with open(transcript_path, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if self.first_ts is None and obj.get("timestamp"):
                    self.first_ts = obj["timestamp"]
                msg = obj.get("message") or {}
                content = msg.get("content")
                if obj.get("type") == "assistant" and isinstance(content, list):
                    texts = []
                    for it in content:
                        if it.get("type") == "tool_use":
                            parts = []
                            _strings(it.get("input"), parts)
                            self.tools.append((it.get("name", ""), it.get("input") or {},
                                               norm("\n".join(parts))))
                        elif it.get("type") == "text":
                            texts.append(it.get("text", ""))
                    if texts:
                        self.last_text = "\n".join(texts)
                elif obj.get("type") == "user":
                    if isinstance(content, str):
                        self.user_texts.append(content)
                    elif isinstance(content, list):
                        for it in content:
                            if it.get("type") == "text":
                                self.user_texts.append(it.get("text", ""))

    def invoked(self):
        found = set()
        for name, inp, _ in self.tools:
            if name == "Skill":
                found.add(str(inp.get("skill", "")).split(":")[-1])
        for t in self.user_texts:
            for m in re.finditer(r"<command-name>/?(?:[\w-]+:)?([\w-]+)</command-name>", t):
                found.add(m.group(1))
        return found & SKILLS

    def _read_blob(self):
        if not hasattr(self, "_blob"):
            self._blob = "\n".join(t for n, _, t in self.tools
                                   if n not in WRITE_TOOLS and n not in ("Skill", "ToolSearch"))
        return self._blob

    def has_read(self, sub):
        return norm(sub) in self._read_blob()

    def has_cmd(self, regex):
        for n, inp, _ in self.tools:
            if n in CMD_TOOLS and re.search(regex, str(inp.get("command", "")), re.I):
                return True
        return False

    def vault_reads(self):
        """Notas distintas lidas: ferramenta Read + comandos de leitura (cat, head, sed...) no Bash.
        Limite conhecido: curingas (cat Characters/NPCs/*.md) não são expandidos."""
        seen = set()
        for n, inp, _ in self.tools:
            if n == "Read":
                rel = rel_to_project(inp.get("file_path"))
                if rel and rel.endswith(".md") and not re.match(r"^(\.claude|_QA|_inbox)/", rel):
                    seen.add(rel.lower())
            elif n in CMD_TOOLS:
                cmd = str(inp.get("command", ""))
                if READ_VERBS.search(cmd):
                    for m in NOTE_PATH.finditer(cmd.replace("\\", "/")):
                        seen.add(m.group(1).lower())
        return len(seen)


# ---------------------------------------------------------------- gates

def gate_matches(g, tool, rel, cmd):
    m = g["match"]
    if tool not in m["tools"]:
        return False
    if "path" in m:
        return rel is not None and re.search(m["path"], rel) is not None
    if "cmd" in m:
        return cmd is not None and re.search(m["cmd"], cmd, re.I) is not None
    return False


def missing_for(g, sess):
    miss = []
    for r in g.get("require_reads", []):
        if not sess.has_read(r):
            miss.append(f"ler {r}")
    for d, rs in g.get("require_reads_if_dir", {}).items():
        if (PROJECT / d).is_dir():
            for r in rs:
                if not sess.has_read(r):
                    miss.append(f"ler {r}")
    for r in g.get("require_reads_if_exists", []):
        if (PROJECT / r).exists() and not sess.has_read(r):
            miss.append(f"ler {r}")
    anyl = g.get("require_reads_any")
    if anyl and not any(sess.has_read(x) for x in anyl):
        miss.append("ler pelo menos um arquivo de: " + ", ".join(anyl))
    for rc in g.get("require_cmds", []):
        if not sess.has_cmd(rc):
            miss.append(f"rodar um comando que case com /{rc}/")
    mv = g.get("min_vault_reads")
    if mv and sess.vault_reads() < mv:
        miss.append(f"ler pelo menos {mv} notas do vault (lidas até agora: {sess.vault_reads()})")
    return miss


def routing_text():
    return "; ".join(f"{k} -> {v}" for k, v in CFG["routing"].items())


def pre_main():
    d = load_input()
    tool = d.get("tool_name", "")
    inp = d.get("tool_input") or {}
    rel = cmd = None
    if tool in WRITE_TOOLS:
        rel = rel_to_project(inp.get("file_path") or inp.get("notebook_path"))
        if rel is None or any_re(CFG["exempt_write_paths"], rel):
            return
    elif tool in CMD_TOOLS:
        cmd = str(inp.get("command", ""))
    else:
        return

    sess = Session(d.get("transcript_path"))
    invoked = sess.invoked()

    is_vault_write = (rel is not None) or (cmd and re.search(CFG["vault_write_commands"], cmd, re.I))
    if is_vault_write and not invoked:
        alvo = rel or "o vault (comando de gravação do gma)"
        block(
            f"BLOQUEADO pelo harness (regra do mestre): gravar em {alvo} sem nenhuma skill do gm-apprentice ativa. "
            "Todo trabalho de campanha passa pela skill certa, carregada com a ferramenta Skill. "
            f"Roteamento: {routing_text()}. Carregue a skill, siga o procedimento dela e tente de novo."
        )

    problems = []
    for g in CFG["gates"]:
        relevant = invoked & set(g["skills"])
        if not relevant or not gate_matches(g, tool, rel, cmd):
            continue
        miss = missing_for(g, sess)
        if miss:
            problems.append((g, miss))
    if problems:
        out = []
        for g, miss in problems:
            out.append(f"[gate {g['id']}] {g['message']}\n  Falta nesta sessão:\n" +
                       "\n".join(f"  - {m}" for m in miss))
        block("BLOQUEADO pelo harness: " + "\n".join(out) +
              "\nFaça o que falta e tente de novo. (Desligar: criar .claude/harness/OFF.)")


# ---------------------------------------------------------------- gate de conteúdo

def gma_path():
    own = paths.CODE.parent / "skills" / "shared" / "scripts" / "gma.py"   # o gma do mesmo plugin
    if own.is_file():
        return str(own)
    cands = glob.glob(str(Path.home() / ".claude/plugins/cache/gm-apprentice/gm-apprentice/*/skills/shared/scripts/gma.py"))
    def ver(p):
        m = re.search(r"gm-apprentice[\\/]gm-apprentice[\\/]([\d.]+)", p)
        return tuple(int(x) for x in m.group(1).split(".")) if m else (0,)
    cands.sort(key=ver)
    return cands[-1] if cands else None


def run_gma(args, timeout=60):
    gma = gma_path()
    if not gma:
        return ""
    env = dict(os.environ, PYTHONUTF8="1")
    r = subprocess.run([sys.executable, gma] + args, capture_output=True, timeout=timeout, env=env)
    return r.stdout.decode("utf-8", errors="replace")


def checks_for(rel):
    p = Path(rel)
    name, folder = p.name, p.parent.as_posix()
    cs = []
    if re.search(r"Wrap_Up\.md$", name):
        cs.append(("wrapup", ["--file", rel]))
    cs.append(("frontmatter", ["--folder", folder]))
    cs.append(("relationships", ["--file", rel]))
    if rel.startswith("Characters/PCs/") and not name.endswith("_Story.md"):
        cs.append(("pc-body", ["--file", rel]))
    cs.append(("gm-leak", ["--folder", folder]))
    return cs


def content_check(rel, levels):
    rows, seen = [], set()
    for check, extra in checks_for(rel):
        out = run_gma(["vault-check", str(PROJECT), check] + extra)
        for line in out.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "\t" not in line:
                continue
            parts = line.split("\t")
            level, where = parts[0].strip(), parts[1].strip() if len(parts) > 1 else ""
            msg = " ".join(parts[2:]).strip()
            if level not in levels:
                continue
            if where.split(":")[0].replace("\\", "/") != rel:
                continue
            if re.search(r"\btone\b", msg, re.I):  # tons pertencem ao campaign-qa
                continue
            key = (check, level, where, msg)
            if key not in seen:
                seen.add(key)
                rows.append(f"{level} [{check}] {where}: {msg}")
    return rows


def post_main():
    d = load_input()
    tool = d.get("tool_name", "")
    inp = d.get("tool_input") or {}
    sid = d.get("session_id")

    if tool not in WRITE_TOOLS:
        return
    rel = rel_to_project(inp.get("file_path") or inp.get("notebook_path"))
    cg = CFG["content_gate"]
    if rel is None or not rel.endswith(".md") or any_re(cg["exempt_paths"], rel):
        return
    st = load_state(sid)
    n = st["content"].get(rel, 0)
    if n >= cg["max_attempts_per_file"]:
        return
    rows = content_check(rel, {"ERROR", "WARNING"})
    if not rows:
        st["content"][rel] = 0
        save_state(sid, st)
        return
    st["content"][rel] = n + 1
    save_state(sid, st)
    block(f"[GATE DE CONTEÚDO] {rel}: o vault-check encontrou {len(rows)} problema(s) nesta nota "
          f"(tentativa {n + 1}/{cg['max_attempts_per_file']}):\n" + "\n".join(f"- {r}" for r in rows) +
          "\nCorrija a nota; a checagem roda de novo ao salvar. Se o aviso for intencional, "
          "diga ao mestre em vez de forçar.")
