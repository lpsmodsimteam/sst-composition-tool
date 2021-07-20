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
    ctree = comp_parser.generate_tree()
    pprint(ctree.get_tree())
    leaves = ctree.get_leaves()
    for leaf in leaves:
        print(ctree.find_element_by_id(leaf.node_id))
