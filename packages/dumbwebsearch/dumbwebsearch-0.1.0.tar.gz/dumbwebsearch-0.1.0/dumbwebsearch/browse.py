#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import os
from pathlib import Path
import shutil
import subprocess

import bottle

from . import index


APP = bottle.Bottle()

BASEURL = os.environ.get("HTTP_SERVER_BASEURL", "")

JPAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document search</title>
</head>
<body>
<form method="post" action="{{ baseurl }}/search">
    <input name="term" value="{{ search | espace }}" />
</form>
<hr/>
{% for res in results %}
    <li><a href="{{ baseurl }}/{{ res[0] | urlencode }}">
        {{- res[0] | escape -}}
    </a>
    {%- if res[1] %} -- {{ res[1] | escape }}
    {%- endif -%}
    </li>
{% endfor %}
</body>
</html>
"""

ROOT = Path(os.environ["INDEX_DIR"])

DB = index.Db(ROOT)
DB.open(os.environ["INDEX_DATABASE"])


@APP.get("/")
def root():
    return bottle.jinja2_template(JPAGE, search="", results=sorted([
        (f.name, "")
        for f in ROOT.glob("*.md")
    ]), baseurl=BASEURL)


@APP.post("/search")
def search():
    term = bottle.request.POST["term"].strip()
    if not term:
        return bottle.redirect(f"{BASEURL}/")

    results = list(DB.searchiter(term))
    return bottle.jinja2_template(
        JPAGE, results=results, search=term, baseurl=BASEURL
    )


@APP.get("/<name>.md")
def getfile(name):
    if "." in name or "/" in name:
        return bottle.abort(403)

    if shutil.which("pandoc"):
        return subprocess.check_output([
            "pandoc", "--sandbox=true", "-s", f"{ROOT}/{name}.md"
        ])

    return bottle.static_file(f"{name}.md", str(ROOT))


if __name__ == "__main__":
    APP.run(port=int(os.environ.get("HTTP_SERVER_PORT", 3046)))
