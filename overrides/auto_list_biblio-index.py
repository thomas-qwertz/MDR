#!/usr/bin/env python3
"""
Vérifier les fichiers de ressources de la bibliothèque MDR et mettre à jour
automatiquement certains fichiers dérivés.

Ce que fait ce script
---------------------

Ce script examine les fichiers de ressources écrits en Markdown dans le dossier :

    docs/biblio/

Il réalise trois actions principales :

1. Vérifie que chaque fichier est correctement structuré.
2. Met à jour automatiquement la page d’index de la bibliothèque :
       docs/biblio/index.md
3. Met à jour la liste complète des ressources dans la navigation du site
   (dans le fichier mkdocs.yml).

L’objectif est de s’assurer que la liste publique des ressources correspond
exactement aux fichiers présents dans le dossier.

Pourquoi ce script existe
-------------------------

Le prototype MDR repose volontairement sur un système simple :

- les ressources sont stockées dans des fichiers Markdown
- un petit script automatise la création des listes et vérifie la cohérence

Ainsi, il n’est pas nécessaire de mettre à jour manuellement plusieurs fichiers
lorsqu’on ajoute ou modifie une ressource.

Comment utiliser ce script
--------------------------

1. Mettre à jour les fichiers automatiquement :

    python overrides/auto_list_biblio-index.py --write

Cette commande :

- vérifie les fichiers
- met à jour l’index de la bibliothèque
- met à jour la navigation dans mkdocs.yml

2. Vérifier uniquement (sans modifier les fichiers) :

    python overrides/auto_list_biblio-index.py --check

Cette commande est utilisée par l’intégration continue (CI).
Elle échoue si :

- un fichier est mal structuré
- un fichier généré n’est plus à jour
"""

from __future__ import annotations

import argparse
import difflib
import html
import os
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        "La bibliothèque PyYAML est nécessaire. Installez les dépendances avec : pip install -r requirements.txt"
    ) from exc


DIGITS_HEADER = "０-９"

AUTO_NAV_START = "# BEGIN AUTO-GENERATED LIBRARY NAV"
AUTO_NAV_END = "# END AUTO-GENERATED LIBRARY NAV"

# Catégories autorisées pour les ressources
ALLOWED_TAGS = (
    "Administratif",
    "Conception",
    "Formation",
    "Recherche",
    "Usages multiples",
    "Non renseigné",
)

# Sections recommandées dans les fiches ressources
RECOMMENDED_SECTIONS = {
    "Objectif": {"Objectif"},
    "Durée/moment d'utilisation": {"Durée/moment d'utilisation"},
    "Limites": {"Limites"},
    "Remarques": {"Remarques"},
    "Personnes ressources": {"Personnes ressources"},
    "Lien vers la/les ressources": {
        "Lien vers la/les ressources",
        "Liens vers la/les ressources",
        "Lien vers la ressource",
        "Liens vers la ressource",
    },
}

# Expressions utilisées pour analyser les fichiers Markdown
FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
H1_RE = re.compile(r"(?m)^#\s+(.+?)\s*$")
H2_RE = re.compile(r"(?m)^##\s+(.+?)\s*$")
DESCRIPTION_RE = re.compile(r"(?im)^\*{0,2}description\s*:\*{0,2}\s+.+$")
RETOURS_RE = re.compile(r"(?i)retours d['’]expériences")
REFERENCES_RE = re.compile(r"(?i)références")


@dataclass(frozen=True)
class Resource:
    """Représente une ressource de la bibliothèque."""

    title: str
    filename: str
    file_path: Path
    file_rel: str
    nav_path: str
    tags: list[str]
    headings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Message:
    """
    Message de validation.

    level :
        "error"   → problème bloquant
        "warning" → avertissement
    """

    level: str
    file_rel: str
    message: str
    title: str = "MDR"


def escape_gh_command(text: str) -> str:
    """Formate un message pour GitHub Actions."""
    return text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def emit_message(msg: Message) -> None:
    """
    Affiche un message d’erreur ou d’avertissement.
    Le format dépend de l’environnement (local ou GitHub Actions).
    """
    if os.getenv("GITHUB_ACTIONS", "").lower() == "true":
        escaped = escape_gh_command(msg.message)
        prefix = f"::{msg.level} file={msg.file_rel},line=1,title={msg.title}::"
        print(prefix + escaped)
    else:
        print(f"[{msg.level}] {msg.file_rel}: {msg.message}")


def strip_accents(value: str) -> str:
    """Supprime les accents pour faciliter le tri alphabétique."""
    return "".join(
        c for c in unicodedata.normalize("NFD", value) if unicodedata.category(c) != "Mn"
    )


def sort_key(title: str) -> str:
    """Clé utilisée pour trier les titres."""
    return strip_accents(title).casefold().strip()


def group_key(title: str) -> str:
    """Détermine la lettre de classement dans l’index."""
    stripped = strip_accents(title).strip()
    if not stripped:
        return "?"
    first = stripped[0].upper()
    if first.isdigit():
        return DIGITS_HEADER
    if "A" <= first <= "Z":
        return first
    return first


def yaml_dquote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def yaml_key(value: str) -> str:
    """Formate une clé YAML en évitant les erreurs de syntaxe."""
    if not value:
        return yaml_dquote(value)
    if value.strip() != value:
        return yaml_dquote(value)
    if re.fullmatch(r"[0-9A-Za-zÀ-ÖØ-öø-ÿ _()'’.,\-]+", value):
        return value
    return yaml_dquote(value)


def parse_front_matter(md_text: str) -> dict | None:
    """Lit le bloc YAML situé en haut du fichier Markdown."""
    match = FRONT_MATTER_RE.match(md_text)
    if not match:
        return None
    raw = match.group(1)
    loaded = yaml.safe_load(raw)
    if loaded is None:
        return {}
    if not isinstance(loaded, dict):
        raise ValueError("Le front matter YAML doit être un objet clé/valeur.")
    return loaded


def extract_title(md_text: str) -> str | None:
    """Extrait le titre principal (#)."""
    match = H1_RE.search(md_text)
    return match.group(1).strip() if match else None


def extract_h2_headings(md_text: str) -> list[str]:
    """Extrait les sous-titres (##)."""
    return [heading.strip() for heading in H2_RE.findall(md_text)]


def has_description(md_text: str) -> bool:
    """Vérifie la présence d'une description courte en tête de fiche."""
    return DESCRIPTION_RE.search(md_text) is not None


def has_retours_section(md_text: str) -> bool:
    """Vérifie la présence d'un bloc de retours d'expériences."""
    return RETOURS_RE.search(md_text) is not None


def has_references_section(md_text: str) -> bool:
    """Vérifie la présence d'un bloc de références."""
    return REFERENCES_RE.search(md_text) is not None


def normalize_tags(value: object) -> list[str]:
    """Vérifie et normalise la liste des catégories."""
    if isinstance(value, str):
        candidates = [value]
    elif isinstance(value, list):
        candidates = value
    else:
        raise ValueError("La clé 'tags' doit être une chaîne ou une liste de chaînes.")

    tags: list[str] = []
    for item in candidates:
        if not isinstance(item, str):
            raise ValueError("Chaque tag doit être une chaîne de caractères.")
        normalized = item.strip()
        if normalized:
            tags.append(normalized)

    if not tags:
        raise ValueError("La clé 'tags' est présente mais vide.")
    return tags


def collect_resources(repo_root: Path) -> tuple[list[Resource], list[Message]]:
    """
    Parcourt les fichiers Markdown de la bibliothèque et vérifie leur structure.
    """
    docs_dir = repo_root / "docs"
    biblio_dir = docs_dir / "biblio"
    if not biblio_dir.exists():
        raise SystemExit("Le dossier docs/biblio/ est introuvable.")

    messages: list[Message] = []
    resources: list[Resource] = []

    for md_file in sorted(biblio_dir.glob("*.md")):
        if md_file.name.lower() == "index.md":
            continue

        file_rel = md_file.relative_to(repo_root).as_posix()
        text = md_file.read_text(encoding="utf-8", errors="replace")

        try:
            front_matter = parse_front_matter(text)
        except ValueError as exc:
            messages.append(Message("error", file_rel, f"Front matter YAML invalide : {exc}"))
            continue

        if front_matter is None:
            messages.append(
                Message("error", file_rel, "Front matter YAML manquant (bloc '--- ... ---').")
            )
            continue

        title = extract_title(text)
        if not title:
            messages.append(Message("error", file_rel, "Titre principal (H1) introuvable."))
            continue

        try:
            tags = normalize_tags(front_matter.get("tags"))
        except ValueError as exc:
            messages.append(Message("error", file_rel, f"Tags invalides : {exc}"))
            continue

        invalid_tags = [tag for tag in tags if tag not in ALLOWED_TAGS]
        if invalid_tags:
            messages.append(
                Message(
                    "error",
                    file_rel,
                    "Catégorie(s) non reconnue(s) : "
                    + ", ".join(sorted(invalid_tags))
                    + ". Catégories autorisées : "
                    + ", ".join(ALLOWED_TAGS)
                    + ".",
                )
            )
            continue

        if len(set(tags)) != len(tags):
            messages.append(
                Message("warning", file_rel, "Des catégories sont présentes en double.")
            )

        if "Non renseigné" in tags:
            messages.append(
                Message(
                    "warning",
                    file_rel,
                    "Le tag 'Non renseigné' est encore présent ; une catégorisation plus précise serait préférable.",
                )
            )

        headings = extract_h2_headings(text)

        for canonical, aliases in RECOMMENDED_SECTIONS.items():
            if not any(heading in aliases for heading in headings):
                messages.append(
                    Message(
                        "warning",
                        file_rel,
                        f"Rubrique recommandée absente : '{canonical}'.",
                    )
                )

        if not has_description(text):
            messages.append(
                Message(
                    "warning",
                    file_rel,
                    "Description courte absente ou introuvable en tête de fiche.",
                )
            )

        if not has_retours_section(text):
            messages.append(
                Message(
                    "warning",
                    file_rel,
                    "Bloc 'Retours d'expériences' absent ou non détecté.",
                )
            )

        if not has_references_section(text):
            messages.append(
                Message(
                    "warning",
                    file_rel,
                    "Bloc 'Références' absent ou non détecté.",
                )
            )

        resources.append(
            Resource(
                title=title,
                filename=md_file.name,
                file_path=md_file,
                file_rel=file_rel,
                nav_path=f"biblio/{md_file.name}",
                tags=tags,
                headings=headings,
            )
        )

    seen_titles: dict[str, str] = {}
    for resource in sorted(resources, key=lambda item: sort_key(item.title)):
        normalized = sort_key(resource.title)
        if normalized in seen_titles:
            messages.append(
                Message(
                    "error",
                    resource.file_rel,
                    f"Titre dupliqué : '{resource.title}' déjà utilisé dans {seen_titles[normalized]}.",
                )
            )
        else:
            seen_titles[normalized] = resource.file_rel

    resources.sort(key=lambda item: sort_key(item.title))
    return resources, messages


def html_escape(value: str) -> str:
    """Échappe un texte pour une insertion sûre dans du HTML généré."""
    return html.escape(value, quote=True)


def normalize_search_blob(*parts: str) -> str:
    """Construit une chaîne normalisée pour la recherche côté client."""
    return sort_key(" ".join(part for part in parts if part))


def render_tag_badges(tags: list[str]) -> str:
    """Génère les badges HTML d'une ressource."""
    return "".join(
        f'<span class="mdr-library-badge">{html_escape(tag)}</span>'
        for tag in tags
    )


def render_filter_button(label: str, count: int, *, is_active: bool = False) -> str:
    """Génère un bouton de filtre par catégorie."""
    classes = "mdr-chip is-active" if is_active else "mdr-chip"
    return (
        f'<button type="button" class="{classes}" data-filter="{html_escape(label)}">'
        f'<span class="mdr-chip__label">{html_escape(label)}</span>'
        f'<span class="mdr-chip__count">{count}</span>'
        "</button>"
    )


def render_index(resources: list[Resource]) -> str:
    """
    Génère automatiquement la page index de la bibliothèque.
    """
    groups: dict[str, list[Resource]] = {}
    for resource in resources:
        bucket = group_key(resource.title)
        groups.setdefault(bucket, []).append(resource)

    ordered_group_keys = [DIGITS_HEADER] + [chr(code) for code in range(ord("A"), ord("Z") + 1)]
    ordered_group_keys = [key for key in ordered_group_keys if groups.get(key)]

    tag_counts: dict[str, int] = {tag: 0 for tag in ALLOWED_TAGS}
    for resource in resources:
        for tag in resource.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    lines: list[str] = [
        "---",
        "hide:",
        "  - toc",
        "---",
        "",
        "# Bibliothèque des ressources",
        "",
        f"{len(resources)} ressources utiles à la recherche, triées par ordre alphabétique ou par [catégories](../categories.md) :",
        "",
        '<div class="mdr-library-index" markdown="1">',
        "",
        '<div class="mdr-library-toolbar">',
        '  <label class="mdr-library-search" for="mdr-library-search">',
        '    <span class="mdr-library-search__label">Filtrer la liste</span>',
        '    <input id="mdr-library-search" class="mdr-library-search__input" type="search" placeholder="Titre ou catégorie" autocomplete="off">',
        "  </label>",
        '  <div class="mdr-library-filters" role="toolbar" aria-label="Filtrer par catégorie">',
        f'    <button type="button" class="mdr-chip is-active" data-filter="*"><span class="mdr-chip__label">Toutes</span><span class="mdr-chip__count">{len(resources)}</span></button>',
    ]

    for tag in ALLOWED_TAGS:
        count = tag_counts.get(tag, 0)
        if count:
            lines.append("    " + render_filter_button(tag, count))

    lines.extend(
        [
            "  </div>",
            "</div>",
            "",
            f'<p class="mdr-library-status" aria-live="polite">{len(resources)} ressources affichées</p>',
            '<p class="mdr-library-empty" hidden>Aucune ressource ne correspond aux filtres en cours.</p>',
            "",
        ]
    )

    for letter in ordered_group_keys:
        lines.append(f'<section class="mdr-library-group" data-group="{html_escape(letter)}">')
        lines.append(f"## {letter}")
        lines.append("")
        lines.append('<ul class="mdr-library-list">')
        for resource in groups[letter]:
            search_blob = normalize_search_blob(resource.title, " ".join(resource.tags))
            tags_attr = "|".join(resource.tags)
            badge_html = render_tag_badges(resource.tags)
            lines.append(
                '<li class="mdr-library-item" '
                f'data-search="{html_escape(search_blob)}" '
                f'data-tags="{html_escape(tags_attr)}">'
                f'<a href="{html_escape(resource.filename)}">{html_escape(resource.title)}</a>'
                f'<span class="mdr-library-item__tags">{badge_html}</span>'
                "</li>"
            )
        lines.append("</ul>")
        lines.append("</section>")
        lines.append("")

    lines.extend(
        [
            "</div>",
            "",
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def render_nav_block(resources: list[Resource], indent: str) -> str:
    """Génère la liste complète des ressources pour mkdocs.yml."""
    return "".join(
        f"{indent}- {yaml_key(resource.title)}: {resource.nav_path}\n" for resource in resources
    )


def replace_nav_block(mkdocs_text: str, resources: list[Resource]) -> str:
    """
    Remplace dans mkdocs.yml la section auto-générée contenant
    la liste complète des ressources.
    """
    lines = mkdocs_text.splitlines(keepends=True)

    start_idx = end_idx = None
    for idx, line in enumerate(lines):
        if AUTO_NAV_START in line:
            start_idx = idx
        if AUTO_NAV_END in line:
            end_idx = idx
            break

    if start_idx is None or end_idx is None or end_idx <= start_idx:
        raise SystemExit(
            "Le bloc auto-généré de mkdocs.yml est introuvable. "
            f"Les marqueurs '{AUTO_NAV_START}' et '{AUTO_NAV_END}' sont requis."
        )

    indent = re.match(r"^(\s*)", lines[start_idx]).group(1)
    new_block = render_nav_block(resources, indent)

    return "".join(lines[: start_idx + 1]) + new_block + "".join(lines[end_idx:])


def write_if_changed(path: Path, content: str) -> bool:
    """Écrit un fichier uniquement si son contenu a changé."""
    current = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    if current == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def current_nav_block(mkdocs_text: str) -> str:
    """Extrait le bloc de navigation auto-généré actuel."""
    lines = mkdocs_text.splitlines(keepends=True)
    start_idx = end_idx = None
    for idx, line in enumerate(lines):
        if AUTO_NAV_START in line:
            start_idx = idx
        if AUTO_NAV_END in line:
            end_idx = idx
            break
    if start_idx is None or end_idx is None or end_idx <= start_idx:
        return ""
    return "".join(lines[start_idx + 1 : end_idx])


def unified_diff(label: str, current: str, expected: str) -> str:
    """Affiche les différences entre deux versions d’un fichier."""
    return "".join(
        difflib.unified_diff(
            current.splitlines(keepends=True),
            expected.splitlines(keepends=True),
            fromfile=f"{label} (actuel)",
            tofile=f"{label} (attendu)",
        )
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Vérifie sans écrire.")
    mode.add_argument("--write", action="store_true", help="Régénère les fichiers.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    check_mode = args.check and not args.write

    repo_root = Path(__file__).resolve().parents[1]
    mkdocs_path = repo_root / "mkdocs.yml"
    index_path = repo_root / "docs" / "biblio" / "index.md"

    resources, messages = collect_resources(repo_root)

    for message in messages:
        emit_message(message)

    error_count = sum(1 for msg in messages if msg.level == "error")
    warning_count = sum(1 for msg in messages if msg.level == "warning")

    if error_count:
        print(f"[mdr] {error_count} erreur(s) bloquante(s), {warning_count} avertissement(s).")
        return 1

    expected_index = render_index(resources)
    current_index = index_path.read_text(encoding="utf-8", errors="replace") if index_path.exists() else ""

    mkdocs_current = mkdocs_path.read_text(encoding="utf-8", errors="replace")
    mkdocs_expected = replace_nav_block(mkdocs_current, resources)

    stale_files: list[str] = []

    if current_index != expected_index:
        stale_files.append("docs/biblio/index.md")

    if current_nav_block(mkdocs_current) != current_nav_block(mkdocs_expected):
        stale_files.append("mkdocs.yml")

    if check_mode:
        if stale_files:
            print(
                "[mdr] Fichiers générés obsolètes : "
                + ", ".join(stale_files)
                + ". Lancez : python overrides/auto_list_biblio-index.py --write"
            )

            if "mkdocs.yml" in stale_files:
                print(
                    unified_diff(
                        "mkdocs.yml",
                        current_nav_block(mkdocs_current),
                        current_nav_block(mkdocs_expected),
                    )
                )

            if "docs/biblio/index.md" in stale_files:
                print(unified_diff("docs/biblio/index.md", current_index, expected_index))

            return 1

        print(f"[mdr] Vérification OK : {len(resources)} ressource(s), {warning_count} avertissement(s).")
        return 0

    changed: list[str] = []

    if write_if_changed(index_path, expected_index):
        changed.append("docs/biblio/index.md")

    if write_if_changed(mkdocs_path, mkdocs_expected):
        changed.append("mkdocs.yml")

    if changed:
        print("[mdr] Fichiers mis à jour : " + ", ".join(changed))
    else:
        print("[mdr] Aucun changement nécessaire.")

    print(f"[mdr] {len(resources)} ressource(s), {warning_count} avertissement(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
