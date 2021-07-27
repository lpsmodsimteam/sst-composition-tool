#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pprint import pprint

from app.compositionparser import CompositionParser
from app.hierarchyresolver import HierarchyResolver


if __name__ == "__main__":

    composition_data = ""
    with open("dump.json") as dump_file:
        composition_data = json.loads(dump_file.read())

    comp_parser = CompositionParser(composition_data)
    comp_parser.filter()
    ctree = comp_parser.generate_tree()
    tree = ctree.get_tree()
    pprint(tree)
    hr = HierarchyResolver(tree)
    hr.resolve_hierarchy()
    pprint(sorted(hr.get_hierarchy(), key=lambda x: x[0][0].id))
