#!/usr/bin/env python3
import json
import os
import time
import shutil
import markdown

# Builds my blog page
# Does its job so what

TIME_INFORMAT = "%Y-%m-%d"
TIME_OUTFORMAT = "%d. %B %Y"
SRC_DIR = "posts"
ASSETS_DIR = "assets"
BUILD_DIR = "build"

os.makedirs(BUILD_DIR, exist_ok=True)


def build_post(post, content):
    output = template
    output = output.replace("$BODY$", template_post)
    output = output.replace("$PAGETITLE$", "{0} - blog.janw.name".format(post["title"]))
    output = output.replace("$TITLE$", post["title"])
    output = output.replace("$CONTENT$", content)
    return output


def build_overview(content):
    output = template
    output = output.replace("$BODY$", template_overview)
    output = output.replace("$PAGETITLE$", "blog.janw.name")
    output = output.replace("$CONTENT$", content)
    return output


toc = None
template = None
template_overview = None
template_post = None

md = markdown.Markdown()

with open("toc.json", "r") as f:
    toc = json.load(f)

with open("template.html", "r") as f:
    template = f.read()

with open("template_overview.html", "r") as f:
    template_overview = f.read()

with open("template_post.html", "r") as f:
    template_post = f.read()

html_index = ""

for num, post in enumerate(
    sorted(
        toc,
        key=lambda x: time.mktime(time.strptime(x["time"], TIME_INFORMAT)),
        reverse=True,
    )
):
    output = template
    with open(os.path.join(SRC_DIR, post["file"]), "r") as f:
        content_raw = f.read()
        content = md.convert(content_raw)

        timestamp = time.strptime(post["time"], TIME_INFORMAT)
        timestamp_str = time.strftime(TIME_OUTFORMAT, timestamp)

        dirname = os.path.join(
            "posts", post["time"] + "-" + post["file"].replace(".md", "")
        )

        print(f"Writing {dirname}...")
        os.makedirs(os.path.join(BUILD_DIR, dirname), exist_ok=True)
        with open(os.path.join(BUILD_DIR, dirname, "index.html"), "w") as o:
            o.write(build_post(post, content))

        html_index += f"""
        <p>
            {timestamp_str}<br>
            <a href="/{dirname}">{post["title"]}</a>
        </p>"""

print(f"Writing index...")
with open(os.path.join(BUILD_DIR, "index.html"), "w") as o:
    o.write(build_overview(html_index))

print("Copying assets...")
ASSETS_TARGET_DIR = os.path.join(BUILD_DIR, "assets")
if os.path.exists(ASSETS_TARGET_DIR):
    shutil.rmtree(ASSETS_TARGET_DIR)
shutil.copytree(ASSETS_DIR, ASSETS_TARGET_DIR)

print("Done")
