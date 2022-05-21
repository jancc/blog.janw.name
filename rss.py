import datetime
from email.utils import format_datetime
from collections import namedtuple
from xml.etree import ElementTree as ET

Post = namedtuple("Post", "title description link author guid pubDate")


class RSS:
    def __init__(self, title, link, description, language):
        self.posts = []
        self.title = title
        self.link = link
        self.description = description
        self.language = language

    def add_post(self, post: Post):
        self.posts.append(post)

    def write(self, filename):
        root = ET.Element("rss", version="2.0")
        channel = ET.SubElement(root, "channel")

        title = ET.SubElement(channel, "title")
        title.text = self.title

        link = ET.SubElement(channel, "link")
        link.text = self.link

        description = ET.SubElement(channel, "description")
        description.text = self.description

        language = ET.SubElement(channel, "language")
        language.text = self.language

        pubDate = ET.SubElement(channel, "pubDate")
        pubDate.text = format_datetime(datetime.datetime.now())

        for post in self.posts:
            item = ET.SubElement(channel, "item")

            title = ET.SubElement(item, "title")
            title.text = post.title

            description = ET.SubElement(item, "description")
            description.text = post.description

            link = ET.SubElement(item, "link")
            link.text = post.link

            author = ET.SubElement(item, "author")
            author.text = post.author

            guid = ET.SubElement(item, "guid")
            guid.text = post.guid

            pubDate = ET.SubElement(item, "pubDate")
            pubDate.text = format_datetime(post.pubDate)

        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
