#!/usr/bin/env python3
import json
import os
import time
import shutil
import markdown

# Builds my blog page
# Does its job so what

TIME_FORMAT = '%Y-%m-%d'
SRC_DIR = 'posts'
ASSETS_DIR = 'assets'
BUILD_DIR = 'build'
PREVIEW_END_TOKEN = '===ENDPREVIEW==='

os.makedirs(BUILD_DIR, exist_ok=True)


def build_post(post, content):
    output = template
    output = output.replace('$BODY$', template_post)
    output = output.replace('$PAGETITLE$', '{0} - blog.klockenschooster.de'.format(post['title']))
    output = output.replace('$TITLE$', post['title'])
    output = output.replace('$CONTENT$', content)
    return output


def build_overview(content):
    output = template
    output = output.replace('$BODY$', template_overview)
    output = output.replace('$PAGETITLE$', 'blog.klockenschooster.de')
    output = output.replace('$CONTENT$', content)
    return output


toc = None
template = None
template_overview = None
template_post = None
html_index = '<table>'

md = markdown.Markdown()

with open('toc.json', 'r') as f:
    toc = json.load(f)

with open('template.html', 'r') as f:
    template = f.read()

with open('template_overview.html', 'r') as f:
    template_overview = f.read()

with open('template_post.html', 'r') as f:
    template_post = f.read()

for num, post in enumerate(
        sorted(toc,
            key=lambda x: time.mktime(time.strptime(x['time'], TIME_FORMAT)),
            reverse=True
            )
        ):
    output = template
    with open(os.path.join(SRC_DIR, post['file']), 'r') as f:
        content_raw = f.read()
        content = md.convert(content_raw.replace(PREVIEW_END_TOKEN, ''))
        content_preview = md.convert(content_raw.split(PREVIEW_END_TOKEN)[0])

        html_filename = post['file'].replace('.md', '.html')

        if(len(content_preview) < len(content)):
            content_preview += f'<p><a href="{html_filename}">read more...</a></p>'

        print(f'Writing {html_filename}...')
        with open(os.path.join(BUILD_DIR, html_filename), 'w') as o:
            o.write(build_post(post, content))

        html_index += '''
        <tr>
        <td><h2>{0}. {2}</h2></td>
        <td class="toc_right">{3}</td>
        </tr>
        <tr>
        <td colspan="2">
            {4}
        </td>
        </tr>
        '''.format(len(toc) - num, html_filename, post['title'], post['time'], content_preview)

html_index += '</table>'

print(f'Writing index...')
with open(os.path.join(BUILD_DIR, 'index.html'), 'w') as o:
    o.write(build_overview(html_index))

print('Copying assets...')
ASSETS_TARGET_DIR = os.path.join(BUILD_DIR, 'assets')
if os.path.exists(ASSETS_TARGET_DIR):
    shutil.rmtree(ASSETS_TARGET_DIR)
shutil.copytree(ASSETS_DIR, ASSETS_TARGET_DIR)

print('Done')

