"""Generate the ready-to-host HTML pages using Python's standard library."""

import argparse
from html import escape
from pathlib import PurePosixPath
from urllib.parse import urlsplit
from xml.etree.ElementTree import Element, SubElement, tostring

from portfolio.components import (
    render_featured_skills,
    render_gallery,
    render_navigation,
    render_projects,
    render_skills,
)
from portfolio.rendering import SITE_DIRECTORY, read_data, render_template


def parse_origin(value):
    """Accept a production HTTPS origin before writing any output."""
    try:
        origin = urlsplit(value)
        origin.port
    except ValueError as error:
        raise argparse.ArgumentTypeError("The origin has an invalid port.") from error

    if (
        origin.scheme != "https"
        or not origin.hostname
        or origin.path not in ("", "/")
        or origin.query
        or origin.fragment
        or origin.username
        or origin.password
        or any(character.isspace() for character in value)
    ):
        raise argparse.ArgumentTypeError(
            "Use an HTTPS origin without a path, such as https://your-site.vercel.app."
        )
    return f"{origin.scheme}://{origin.netloc}"


def build_pages():
    site = read_data("site.json")
    pages = read_data("pages.json")
    icons = read_data("icons.json")
    projects = read_data("projects.json")
    galleries = read_data("galleries.json")

    shared_content = {
        "name": escape(site["name"]),
        **{key: escape(value) for key, value in site["links"].items()},
        "featured_skills": render_featured_skills(icons),
        "skill_sections": render_skills(read_data("skills.json"), icons),
        **{key: render_gallery(settings) for key, settings in galleries.items()},
    }

    # Render every page first so a missing template or data field fails before writing.
    output = {}
    for page in pages:
        page_path = page["path"]
        page_content = render_template(
            page["template"],
            **shared_content,
            selected_projects=render_projects(projects, page_path),
        )
        depth = len(PurePosixPath(page_path).parts) - 1
        output[page_path] = render_template(
            "layout.html",
            **{key: escape(value) for key, value in site["links"].items()},
            name=escape(site["name"]),
            page_title=escape(page["title"]),
            description=escape(page["description"]),
            asset_prefix="../" * depth,
            navigation=render_navigation(site["navigation"], page_path),
            content=page_content,
        )

    for page_path, html in output.items():
        destination = SITE_DIRECTORY / page_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(html, encoding="utf-8")
    return pages


def write_search_files(pages, origin):
    robots = "User-agent: *\nAllow: /\n"
    sitemap_path = SITE_DIRECTORY / "sitemap.xml"

    if origin:
        sitemap = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        for page in pages:
            route = page["path"]
            if route.endswith("index.html"):
                route = route[:-len("index.html")]
            entry = SubElement(sitemap, "url")
            SubElement(entry, "loc").text = f"{origin}/{route}"

        xml = tostring(sitemap, encoding="utf-8", xml_declaration=True)
        sitemap_path.write_bytes(xml + b"\n")
        robots += f"Sitemap: {origin}/sitemap.xml\n"
    else:
        sitemap_path.unlink(missing_ok=True)

    (SITE_DIRECTORY / "robots.txt").write_text(robots, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--origin", type=parse_origin, help="Production HTTPS site origin.")
    arguments = parser.parse_args()

    pages = build_pages()
    write_search_files(pages, arguments.origin)
    print(f"Built {len(pages)} pages in {SITE_DIRECTORY}")


if __name__ == "__main__":
    main()
