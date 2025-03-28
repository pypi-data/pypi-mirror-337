# Copyright (c) 2019-2024 Chris Pressey, Cat's Eye Technologies
# This file is distributed under an MIT license.  See LICENSES/ directory.
# SPDX-License-Identifier: LicenseRef-MIT-X-Feedmark

from datetime import datetime
from collections import OrderedDict
import re

from marko.block import (
    SetextHeading,
    Heading,
    HTMLBlock,
    BlankLine,
    List,
    Paragraph,
    LinkRefDef,
)
from marko.inline import Image, Link, RawText, Literal
from marko.parser import Parser as MarkoParser

from .models import Document, Section
from .formats.markdown import markdown_to_html5, markdown_to_html5_deep
from .utils import quote


def strip_square_brackets(s):
    if s.startswith("[") and s.endswith("]"):
        return s[1:-1]
    return s


def has_image_child(child):
    return isinstance(child, Image) or (
        isinstance(child, Link) and isinstance(child.children[0], Image)
    )


def is_image_paragraph(child):
    return isinstance(child, Paragraph) and has_image_child(child.children[0])


def obtain_heading_text(element):
    chunks = []
    for child in element.children:
        if isinstance(child, RawText):
            chunks.append(child.children)
        elif isinstance(child, Literal):
            chunks.append("\\")
            chunks.append(child.children)
    return "".join(chunks)


class Parser:
    def __init__(self):
        pass

    def parse(self, markdown_text):
        marko_parser = MarkoParser()
        marko_document = marko_parser.parse(markdown_text)

        document = Document()
        section = None
        reading_images = True
        reading_properties = True

        for child in marko_document.children:
            if isinstance(child, (Heading, SetextHeading)):
                title_text = obtain_heading_text(child)
                if child.level == 1:
                    document.set_title(title_text)
                elif child.level == 3:
                    section = Section(title_text)
                    reading_images = True
                    reading_properties = True
                    document.sections.append(section)
                    section.document = document
                elif section:
                    section.add_to_body(child)
                else:
                    document.add_to_preamble(child)
            elif isinstance(child, HTMLBlock) and not section:
                document.add_to_header_comment(child)
            elif reading_properties and isinstance(child, List):
                reading_images = False
                reading_properties = False
                for listitem in child.children:
                    if not section:
                        document.add_property_listitem(listitem)
                    else:
                        section.add_property_listitem(listitem)
            elif isinstance(child, LinkRefDef):
                # LinkRefDef elements always go in the main document, not sections.
                document.link_ref_defs.add(
                    strip_square_brackets(child.label.text), child.dest, child.title
                )
            elif reading_images and is_image_paragraph(child):
                section.add_image_paragraph(child)
            else:
                if isinstance(child, Paragraph):
                    reading_images = False
                    reading_properties = False
                if section:
                    section.add_to_body(child)
                else:
                    document.add_to_preamble(child)

        return document
