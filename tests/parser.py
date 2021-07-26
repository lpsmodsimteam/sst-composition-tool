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
    hr.get_hierarchy()
    # leaves = ctree.get_leaves()[3]
    # print(leaves, hr.get_module_from_element(leaves))
    # # 12 {'from_port': 'cout#4#8', 'to_node_type: 13, 'to_port': 'cin#3#7'}
    # print(hr.resolve_to_port(leaves, 13, "cin#3#7"))
