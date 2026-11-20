"""Reusable components for navigation, skills, project cards and photo galleries.

Plain text from JSON is escaped here. HTML fragments are produced only by
templates or the SVG definitions stored in icons.json.
"""

import posixpath
from html import escape
from urllib.parse import quote

from .rendering import SITE_DIRECTORY, render_template


def render_navigation(navigation, page_path):
    active_page = page_path
    if page_path.startswith("projects/"):
        active_page = "projects/index.html"

    links = []
    for item in navigation:
        url = posixpath.relpath(item["path"], posixpath.dirname(page_path) or ".")
        current = ' aria-current="page"' if item["path"] == active_page else ""
        links.append(
            f'<a href="{escape(url)}"{current}>{escape(item["label"])}</a>'
        )
    return "\n".join(links)


def render_featured_skills(icons):
    tiles = []
    for skill in icons["featured"]:
        icon = f'<svg viewBox="0 0 24 24" aria-hidden="true">{skill["drawing"]}</svg>'
        tiles.append(
            render_template(
                "components/skill-tile.html",
                class_name=escape(skill["class_name"]),
                label=escape(skill["label"]),
                icon=icon,
            )
        )
    return "\n".join(tiles)


def render_skill_group(group, icons):
    tiles = []
    for label in group["technologies"]:
        if label in icons["technologies"]:
            filename = icons["technologies"][label]
            icon = (
                f'<img class="technology-logo" src="assets/icons/{filename}.svg"'
                ' alt="" width="28" height="28" loading="lazy">'
            )
        else:
            drawing = icons["concepts"][label]
            icon = f'<svg viewBox="0 0 24 24" aria-hidden="true">{drawing}</svg>'

        tiles.append(
            render_template(
                "components/skill-tile.html",
                class_name="technology",
                label=escape(label),
                icon=icon,
            )
        )

    return render_template(
        "components/skill-group.html",
        title=escape(group["title"]),
        tiles="\n".join(tiles),
    )


def render_skills(content, icons):
    intro = content["intro"]
    sections = [
        '<header class="intro">',
        f'  <h1>{escape(intro["title"])}</h1>',
        f'  <p class="lede">{escape(intro["description"])}</p>',
        "</header>",
    ]
    for section in content["sections"]:
        groups = [render_skill_group(group, icons) for group in section["groups"]]
        sections.extend(
            [
                '<section class="section">',
                f'  <h2>{escape(section["title"])}</h2>',
                *groups,
            ]
        )
        if section.get("description"):
            sections.append(f'<p class="prose">{escape(section["description"])}</p>')
        sections.append("</section>")

    return "\n".join(sections)


def render_projects(projects, page_path):
    heading_tag = "h2" if page_path == "projects/index.html" else "h3"
    cards = []
    for project in projects:
        url = posixpath.relpath(project["path"], posixpath.dirname(page_path) or ".")
        cards.append(
            render_template(
                "components/project-card.html",
                heading_tag=heading_tag,
                project_type=escape(project["type"]),
                title=escape(project["title"]),
                description=escape(project["description"]),
                url=escape(url),
                link_label=escape(project["link_label"]),
            )
        )
    return '<div class="grid">\n' + "\n".join(cards) + "</div>"


def render_gallery(settings):
    assets = SITE_DIRECTORY / "assets"
    photos = sorted(
        photo
        for photo in assets.glob(settings["prefix"] + "*")
        if photo.suffix.lower() in (".webp", ".jpg", ".jpeg", ".png")
        and photo.name not in settings["excluded"]
    )
    if not photos:
        return render_template("components/photo-placeholder.html")

    slides = []
    for position, photo in enumerate(photos, start=1):
        caption = settings["captions"].get(photo.name, settings["caption"])
        slides.append(
            render_template(
                "components/slide.html",
                position=position,
                total=len(photos),
                url="assets/" + quote(photo.name),
                caption=escape(caption),
            )
        )
    return render_template(
        "components/gallery.html",
        caption=escape(settings["caption"]),
        slides="\n".join(slides),
    )
