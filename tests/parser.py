#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pprint import pprint

from app.compositionparser import CompositionParser


if __name__ == "__main__":

    composition_data = ""
    with open("dump.json") as dump_file:
        composition_data = json.loads(dump_file.read())

    comp_parser = CompositionParser(composition_data)
    comp_parser.filter()
    comp_parser.generate_tree()
    comp_parser.resolve_hierarchy()
    resolved_links = comp_parser.get_resolved_links()
    pprint(sorted(resolved_links, key=lambda x: x[0][0].type))
