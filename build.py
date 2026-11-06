"""Assemble index.html from src/shell.html and src/papers/*.html.

Each paper fragment cites its own quote list:
  - `[[key]]` in the text becomes a superscript citation button;
  - `<blockquote class="pull" data-from="key">` gets the quoted English inserted
    and a citation appended to its footer;
  - `<li data-key="key">` items in `<ol class="quotes">` hold the verbatim quotes.
Citations are numbered per paper in order of first appearance and the quote list
is reordered to match. Unknown or unused keys stop the build.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
PAPERS = [
    "overview", "agentboard", "deltabox", "llmservingsim", "agentservesim", "cost-of-reasoning", "crab",
    "agentsysbench", "sessions", "xperf", "murakkab", "agentix", "conserve", "cachescout",
    "simthesizer", "specbox", "yolofs", "safe-resume", "briefs",
]

QUOTES_RE = re.compile(r'(<ol class="quotes">)(.*?)(</ol>)', re.S)
ITEM_RE = re.compile(r'<li data-key="([^"]+)">(.*?)</li>', re.S)
TEXT_RE = re.compile(r"<blockquote lang=\"en\">(.*?)</blockquote>", re.S)
PULL_RE = re.compile(r'<blockquote class="pull" data-from="([^"]+)">(.*?)</footer></blockquote>', re.S)
MARK_RE = re.compile(r"\[\[([a-z0-9-]+)\]\]")


def cite(n):
    return f'<button class="cite" data-q="{n}">{n}</button>'


def build_paper(name):
    src = (ROOT / "src" / "papers" / f"{name}.html").read_text(encoding="utf-8")
    m = QUOTES_RE.search(src)
    if not m:
        if MARK_RE.search(src):
            sys.exit(f"{name}: citations but no quote list")
        print(f"{name}: no quotes")
        return src
    items = dict(ITEM_RE.findall(m.group(2)))
    texts = {k: TEXT_RE.search(v).group(1).strip() for k, v in items.items()}
    body = src[: m.start()] + "\0QUOTES\0" + src[m.end():]

    order = []

    def number(key):
        if key not in items:
            sys.exit(f"{name}: unknown quote key '{key}'")
        if key not in order:
            order.append(key)
        return order.index(key) + 1

    # Walk pull quotes and [[key]] marks together, in document order.
    out, pos = [], 0
    token = re.compile(PULL_RE.pattern + "|" + MARK_RE.pattern, re.S)
    for t in token.finditer(body):
        out.append(body[pos: t.start()])
        if t.group(1):
            key, footer = t.group(1), t.group(2)
            n = number(key)
            out.append(
                f'<blockquote class="pull"><p lang="en">{texts[key]}</p>'
                f"{footer}{cite(n)}</footer></blockquote>"
            )
        else:
            out.append(cite(number(t.group(3))))
        pos = t.end()
    out.append(body[pos:])
    body = "".join(out)

    unused = [k for k in items if k not in order]
    if unused:
        sys.exit(f"{name}: quotes never cited: {', '.join(unused)}")
    lis = "\n".join(f'    <li id="{name}-q{i + 1}">{items[k]}</li>' for i, k in enumerate(order))
    body = body.replace("\0QUOTES\0", f'<ol class="quotes">\n{lis}\n  </ol>')
    print(f"{name}: {len(order)} quotes")
    return body


def main():
    shell = (ROOT / "src" / "shell.html").read_text(encoding="utf-8")
    for name in PAPERS:
        marker = f"<!-- PAPER:{name} -->"
        frag = ROOT / "src" / "papers" / f"{name}.html"
        shell = shell.replace(marker, build_paper(name) if frag.exists() else "")
    (ROOT / "index.html").write_text(shell, encoding="utf-8")
    print("wrote index.html", len(shell.encode()), "bytes")


if __name__ == "__main__":
    main()
