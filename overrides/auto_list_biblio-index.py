#!/usr/bin/env python3
"""Regenerate MDR library artifacts.

Goals
-----
- Keep **"Liste complète" in the left menu** (mkdocs.yml) but stop maintaining it by hand.
- Keep **docs/biblio/index.md** (alphabetical list) but stop maintaining it by hand.
- Only *signal* content problems (warnings), never block publishing.

What gets regenerated
---------------------
- `docs/biblio/index.md`
- The children of the `- Liste complète:` item in `mkdocs.yml`

Content warnings (non-blocking)
------------------------------
- Missing H1 title
- Missing YAML front matter `tags`
- Tag == 'Non renseigné'

Designed to run in GitHub Actions after checkout.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import unicodedata


H1_RE = re.compile(r"(?m)^#\s+(.+?)\s*$")
FRONT_MATTER_RE = re.compile(r"(?s)\A---\s*\n(.*?)\n---\s*\n", re.MULTILINE)

DIGITS_HEADER = "０-９"


def _strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def _sort_key(title: str) -> str:
    return _strip_accents(title).casefold().strip()


def _group_key(title: str) -> str:
    t = _strip_accents(title).strip()
    if not t:
        return "?"
    c = t[0].upper()
    if c.isdigit():
        return DIGITS_HEADER
    if "A" <= c <= "Z":
        return c
    return c  # fallback


def _escape_gh_command(s: str) -> str:
    # GitHub workflow commands need escaping for %, CR, LF.
    return s.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def warn(file_rel: str, message: str, title: str = "MDR") -> None:
    msg = _escape_gh_command(message)
    print(f"::warning file={file_rel},line=1,title={title}::{msg}")


def _extract_title(md_text: str) -> str | None:
    m = H1_RE.search(md_text)
    if not m:
        return None
    return m.group(1).strip()


def _extract_tags(md_text: str) -> list[str] | None:
    """
    Minimal YAML front matter parser for 'tags:' only, to keep stdlib-only.
    Expected shapes:
      ---
      tags:
        - X
        - Y
      ---
    or:
      ---
      tags: [X, Y]
      ---
    """
    m = FRONT_MATTER_RE.match(md_text)
    if not m:
        return None
    fm = m.group(1)

    # Case 1: block list
    block = re.search(r"(?m)^\s*tags\s*:\s*\n((?:\s*-\s*.*\n)+)", fm)
    if block:
        items = []
        for line in block.group(1).splitlines():
            line = line.strip()
            if line.startswith("-"):
                items.append(line[1:].strip())
        return [t for t in items if t]

    # Case 2: inline list
    inline = re.search(r"(?m)^\s*tags\s*:\s*\[(.*?)\]\s*$", fm)
    if inline:
        raw = inline.group(1)
        parts = [p.strip().strip("'\"") for p in raw.split(",")]
        return [p for p in parts if p]

    # Case 3: scalar (rare)
    scalar = re.search(r"(?m)^\s*tags\s*:\s*(.+?)\s*$", fm)
    if scalar:
        v = scalar.group(1).strip().strip("'\"")
        return [v] if v else []

    return None


def _yaml_quote_key(s: str) -> str:
    """
    Quote only when needed (keeps mkdocs.yml readable).
    If unsure -> quote.
    """
    if s == "" or s.strip() != s:
        return _yaml_dquote(s)
    # safe-ish plain keys: letters, numbers, spaces, some punctuation incl accents
    if re.fullmatch(r"[0-9A-Za-zÀ-ÖØ-öø-ÿ _()'’.,\-]+", s):
        return s
    # ':' and '#' etc => quote
    return _yaml_dquote(s)


def _yaml_dquote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


@dataclass(frozen=True)
class Resource:
    title: str
    filename: str           # e.g. entretien.md
    rel_path_docs: str      # e.g. docs/biblio/entretien.md
    nav_path: str           # e.g. biblio/entretien.md
    tags: list[str] | None


def collect_resources(repo_root: Path, docs_dir: Path) -> list[Resource]:
    biblio_dir = docs_dir / "biblio"
    resources: list[Resource] = []

    for md in sorted(biblio_dir.glob("*.md")):
        if md.name.lower() == "index.md":
            continue

        text = md.read_text(encoding="utf-8", errors="replace")
        title = _extract_title(text)

        file_rel = str(md.relative_to(repo_root)).replace("\\", "/")
        if not title:
            # fallback: filename -> title-like
            fallback = md.stem.replace("_", " ").strip()
            warn(file_rel, "Titre H1 introuvable. Fallback utilisé (nom de fichier).")
            title = fallback

        tags = _extract_tags(text)
        if tags is None:
            warn(file_rel, "Aucun tag détecté dans le front matter YAML (tags: ...).")
        else:
            if any(t.strip().lower() == "non renseigné" for t in tags):
                warn(file_rel, "Tag 'Non renseigné' présent (à clarifier).")

        resources.append(
            Resource(
                title=title,
                filename=md.name,
                rel_path_docs=file_rel,
                nav_path=f"biblio/{md.name}",
                tags=tags,
            )
        )

    # sort by title (accent-insensitive)
    resources.sort(key=lambda r: _sort_key(r.title))
    return resources


def regen_mkdocs_nav(repo_root: Path, mkdocs_path: Path, resources: list[Resource]) -> bool:
    """
    Replaces ONLY the children of the '- Liste complète:' node.
    Everything else in mkdocs.yml stays as-is.
    """
    text = mkdocs_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines(keepends=True)

    # Locate '- Liste complète:'
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "- Liste complète:":
            start = i
            break
    if start is None:
        # this is an automation contract: if it disappears, we want to know
        raise SystemExit("ERROR: Cannot find '- Liste complète:' in mkdocs.yml")

    start_indent = len(lines[start]) - len(lines[start].lstrip(" "))
    child_indent = start_indent + 2

    # Find end of that block: first non-empty line with indent <= start_indent
    end = start + 1
    while end < len(lines):
        if lines[end].strip() == "":
            end += 1
            continue
        indent = len(lines[end]) - len(lines[end].lstrip(" "))
        if indent <= start_indent:
            break
        end += 1

    new_block = []
    new_block.append(" " * child_indent + "# AUTO-GÉNÉRÉ — ne pas éditer à la main\n")
    for r in resources:
        key = _yaml_quote_key(r.title)
        new_block.append(" " * child_indent + f"- {key}: {r.nav_path}\n")

    new_lines = lines[: start + 1] + new_block + lines[end:]
    new_text = "".join(new_lines)

    if new_text == text:
        return False

    mkdocs_path.write_text(new_text, encoding="utf-8")
    return True


def regen_biblio_index(repo_root: Path, index_path: Path, resources: list[Resource]) -> bool:
    groups: dict[str, list[Resource]] = {DIGITS_HEADER: []}
    for c in [chr(i) for i in range(ord("A"), ord("Z") + 1)]:
        groups[c] = []

    for r in resources:
        g = _group_key(r.title)
        if g not in groups:
            # ignore exotic groups in the index (or map them if you prefer)
            continue
        groups[g].append(r)

    def block(letter: str, items: list[Resource], first: bool) -> str:
        style = ' style="margin-top: 0"' if first else ""
        out = []
        out.append("<div markdown>\n")
        out.append(f"<h2{style}><span class=\"md-tag\">{letter}</span></h2>\n")
        for it in items:
            out.append(f"* [{it.title}]({it.filename})\n")
        out.append("</div>\n\n")
        return "".join(out)

    out_lines = [
        "---\n",
        "hide:\n",
        "  - toc\n",
        "---\n\n",
        "# Bibliothèque des ressources\n",
        "<!-- (chemins relatifs au dossier \"biblio/\") -->\n\n",
        f"{len(resources)} ressources utiles à la recherche, triées par ordre alphabétique ou par [catégories](../categories.md) :\n\n",
        "<div class=\"two-columns\" style=\"margin-top:1.5rem\" markdown>\n\n",
    ]

    out_lines.append(block(DIGITS_HEADER, groups[DIGITS_HEADER], first=True))
    for c in [chr(i) for i in range(ord("A"), ord("Z") + 1)]:
        out_lines.append(block(c, groups[c], first=False))

    out_lines += [
        "</div>\n",
        "<style>\n",
        "  li {\n",
        "      text-align: left;\n",
        "  }\n",
        "</style>\n",
    ]

    new_text = "".join(out_lines)
    old_text = index_path.read_text(encoding="utf-8", errors="replace") if index_path.exists() else ""

    if old_text == new_text:
        return False

    index_path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    mkdocs_path = repo_root / "mkdocs.yml"
    docs_dir = repo_root / "docs"
    biblio_index = docs_dir / "biblio" / "index.md"

    resources = collect_resources(repo_root, docs_dir)

    changed_nav = regen_mkdocs_nav(repo_root, mkdocs_path, resources)
    changed_index = regen_biblio_index(repo_root, biblio_index, resources)

    if changed_nav or changed_index:
        updated = []
        if changed_nav:
            updated.append("mkdocs.yml")
        if changed_index:
            updated.append("docs/biblio/index.md")
        print("[regen] Updated files: " + " ".join(updated))
    else:
        print("[regen] Nothing to update")

    # Important: never fail the pipeline due to content warnings.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
