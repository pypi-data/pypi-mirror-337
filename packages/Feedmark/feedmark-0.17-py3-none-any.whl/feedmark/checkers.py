# Copyright (c) 2019-2024 Chris Pressey, Cat's Eye Technologies
# This file is distributed under an MIT license.  See LICENSES/ directory.
# SPDX-License-Identifier: LicenseRef-MIT-X-Feedmark

from __future__ import absolute_import

from feedmark.formats.markdown import markdown_to_html5


class Schema(object):
    def __init__(self, document):
        self.document = document
        self.property_rules = {}
        self.property_priority_order = []
        for section in self.document.sections:
            self.property_rules[section.title] = section
            self.property_priority_order.append(section.title)

    def check(self, section):
        results = []
        for key, value in section.properties.items():
            if key not in self.property_rules:
                results.append(["extra", key])
        for key, value in self.property_rules.items():
            optional = value.properties.get("optional", "false") == "true"
            if optional:
                continue
            if key not in section.properties:
                results.append(["missing", key])
        return results

    def check_documents(self, documents):
        results = []
        for document in documents:
            for section in document.sections:
                result = self.check(section)
                if result:
                    results.append(
                        {
                            "section": section.title,
                            "document": document.title,
                            "result": result,
                        }
                    )
        return results

    def get_property_priority_order(self):
        return self.property_priority_order
