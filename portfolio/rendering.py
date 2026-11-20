"""Read structured content and render the shared HTML templates."""

import json
import re
from pathlib import Path
from string import Template


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SITE_DIRECTORY = PROJECT_ROOT / "site"
TEMPLATE_DIRECTORY = PROJECT_ROOT / "templates"


def read_data(filename):
    path = PROJECT_ROOT / "data" / filename
    return json.loads(path.read_text(encoding="utf-8"))


def render_template(filename, **values):
    path = TEMPLATE_DIRECTORY / filename
    template = Template(path.read_text(encoding="utf-8"))
    # Keep generated HTML indented when a slot contains a multiline component.
    for indentation, name in re.findall(r"^([ ]*)\$(\w+)\s*$", template.template, re.MULTILINE):
        value = str(values[name]).rstrip()
        values[name] = value.replace("\n", "\n" + indentation)
    return template.substitute(values)
