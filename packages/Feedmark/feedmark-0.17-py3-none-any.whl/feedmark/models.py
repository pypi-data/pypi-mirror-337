# Copyright (c) 2019-2024 Chris Pressey, Cat's Eye Technologies
# This file is distributed under an MIT license.  See LICENSES/ directory.
# SPDX-License-Identifier: LicenseRef-MIT-X-Feedmark

from datetime import datetime
from collections import OrderedDict
import re

from marko.block import BlankLine, LinkRefDefs
from marko.element import Element
from marko.inline import Image, Link

from .formats.markdown import markdown_to_html5, markdown_to_html5_deep
from .renderer import CleanMarkdownRenderer
from .utils import quote


def rewrite_link_ref_defs(refdex, link_ref_defs):
    from marko.block import LinkRefDefs

    new_link_ref_defs = LinkRefDefs()
    seen_names = set()
    for name, (url, title) in link_ref_defs.items():
        name = sorted(link_ref_defs.unnormalized_labels_for(name))[0]
        if name in seen_names:
            continue
        seen_names.add(name)
        if name in refdex:
            entry = refdex[name]
            if "filename" in entry and "anchor" in entry:
                filename = quote(entry["filename"].encode("utf-8"))
                anchor = quote(entry["anchor"].encode("utf-8"))
                url = "{}#{}".format(filename, anchor)
            elif "filenames" in entry and "anchor" in entry:
                # pick the last one, for compatibility with single-refdex style
                filename = quote(entry["filenames"][-1].encode("utf-8"))
                anchor = quote(entry["anchor"].encode("utf-8"))
                url = "{}#{}".format(filename, anchor)
            elif "url" in entry:
                url = entry["url"]
            else:
                raise ValueError("Badly formed refdex entry: {}".format(entry))
        new_link_ref_defs.add(name, url, title)
    return new_link_ref_defs


class PropertyCollection:
    """Mixin that supports maintaining a set of properties on the object."""

    def __init__(self, *args, **kwargs):
        self.properties = OrderedDict()

    def add_property(self, kind, key, value):
        if kind == ":":
            if key in self.properties:
                raise KeyError("{} already given".format(key))
            self.properties[key] = value
        elif kind == "@":
            self.properties.setdefault(key, []).append(value)
        else:
            raise NotImplementedError(kind)

    def parse_property(self, listitem_text):
        match = re.match(r"^(.*?)\s*\@\s*(.*?)\s*$", listitem_text)
        if match:
            (key, val) = (match.group(1), match.group(2))
            return ("@", key, val)
        match = re.match(r"^(.*?)\s*\:\s*(.*?)\s*$", listitem_text)
        if match:
            (key, val) = (match.group(1), match.group(2))
            return (":", key, val)
        raise ValueError('Expected property, found "{}"'.format(listitem_text))

    def add_property_listitem(self, element):
        listitem_text = self.renderer.render(element).strip()
        kind, key, value = self.parse_property(listitem_text)
        self.add_property(kind, key, value)


class Document(PropertyCollection):
    def __init__(self, *args, renderer=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.renderer = renderer or CleanMarkdownRenderer()

        self.title = "Untitled"
        self.properties = OrderedDict()

        self._header_comment: list(Element) = []
        self._preamble: list(Element) = []
        self.sections: list(Section) = []
        self.link_ref_defs = LinkRefDefs()

    def __str__(self):
        return "document '{}'".format(self.title.encode("utf-8"))

    def set_title(self, title):
        self.title = title

    @property
    def header_comment(self):
        md = ""
        for element in self._header_comment:
            md += self.renderer.render(element)
        md += "\n"
        return md

    def has_header_comment(self) -> bool:
        return bool(self._header_comment)

    def add_to_header_comment(self, element):
        self._header_comment.append(element)

    @property
    def preamble(self):
        md = ""
        skipping_blanks = True
        for element in self._preamble:
            if skipping_blanks and isinstance(element, BlankLine):
                continue
            else:
                skipping_blanks = False
            md += self.renderer.render(element)
        md += "\n"
        return md

    def add_to_preamble(self, element):
        self._preamble.append(element)

    def has_preamble(self) -> bool:
        return bool(self._preamble)

    def rewrite_link_ref_defs(self, refdex):
        self.link_ref_defs = rewrite_link_ref_defs(refdex, self.link_ref_defs)

    def global_link_ref_defs(self):
        return self.link_ref_defs

    def to_json_data(self, htmlize=False, ordered=False, link_ref_defs=None):
        preamble = self.preamble.strip()
        properties = self.properties

        if htmlize:
            if not link_ref_defs:
                link_ref_defs = self.global_link_ref_defs()
            preamble = markdown_to_html5(preamble, link_ref_defs=link_ref_defs)
            properties = markdown_to_html5_deep(
                self.properties, link_ref_defs=link_ref_defs
            )

        if ordered:
            properties_list = []
            for key, value in properties.items():
                properties_list.append([key, value])
            properties = properties_list
        else:
            properties = dict(properties)

        return {
            "filename": self.filename,
            "title": self.title,
            "properties": properties,
            "preamble": preamble,
            "sections": [
                section.to_json_data(
                    htmlize=htmlize, ordered=ordered, link_ref_defs=link_ref_defs
                )
                for section in self.sections
            ],
        }


class Section(PropertyCollection):
    def __init__(self, title, *args, renderer=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.renderer = renderer or CleanMarkdownRenderer()
        self.document = None
        self.title = title
        self._body: list(Element) = []
        self.images = []

    def __str__(self):
        s = "section '{}'".format(self.title.encode("utf-8"))
        if self.document:
            s += " of " + str(self.document)
        return s

    def collect_image_children(self, element):
        for child in element.children:
            if isinstance(child, Image):
                yield {
                    "description": self.renderer.render(child.children[0]).strip(),
                    "source": child.dest,
                }
            if isinstance(child, Link) and isinstance(child.children[0], Image):
                yield {
                    "description": self.renderer.render(
                        child.children[0].children[0]
                    ).strip(),
                    "source": child.children[0].dest,
                    "link": child.dest,
                }

    def add_image_paragraph(self, element):
        for image_record in self.collect_image_children(element):
            self.images.append(image_record)

    @property
    def body(self):
        md = ""
        for element in self._body:
            md += self.renderer.render(element)
        md += "\n"
        md = re.sub(r"^\n+", "", md)
        md = re.sub(r"\n+$", "\n", md)
        return md

    def add_to_body(self, element):
        self._body.append(element)

    @property
    def publication_date(self):
        formats = (
            "%b %d %Y %H:%M:%S",
            "%a, %d %b %Y %H:%M:%S GMT",
        )
        for format in formats:
            try:
                return datetime.strptime(self.properties["date"], format)
            except KeyError:
                raise KeyError("could not find 'date' on {}".format(self))
            except ValueError:
                pass
        raise NotImplementedError

    @property
    def anchor(self):
        title = self.title.strip().lower()
        title = re.sub(r"[^\w]+$", "", title)
        title = re.sub(r"[^\w\s\/\.\'-]", "", title)
        return re.sub(r"[\s\/\.\'-]+", "-", title)

    def to_json_data(self, htmlize=False, ordered=False, link_ref_defs=None):
        body = self.body
        properties = self.properties

        if htmlize:
            body = markdown_to_html5(body, link_ref_defs=link_ref_defs)
            properties = markdown_to_html5_deep(
                self.properties, link_ref_defs=link_ref_defs
            )

        if ordered:
            properties_list = []
            for key, value in properties.items():
                properties_list.append([key, value])
            properties = properties_list
        else:
            properties = dict(properties)

        return {
            "title": self.title,
            "anchor": self.anchor,
            "images": self.images,
            "properties": properties,
            "body": body,
        }
