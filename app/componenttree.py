#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Represent the entire Drawflow node structure as a ComponentTree composed of
ComponentNode objects.

A ComponentTree is a tree of ComponentNode objects. Standalone, the class can
be instantiated by a raw Drawflow node structure composition data structure.
The object would however not be an accurate representation of the composition
if the Drawflow node structure contains submodules.
"""


from .componentnode import ComponentNode


class ComponentTree:

    """
    Tree representation of Drawflow composition of nodes

    Attributes
    ----------
    __composition : dict = None
        Prebuilt Drawflow composition data structure. In production, this
        parameter is always None due to the dynamic nature of the creation of
        the Drawflow compositions.

    root_key : str = "Home"
        The key of the root node in the composition data structure.

    __root : ComponentNode
        The root ComponentNode of the ComponentTree.

    __leaves : list<ComponentNode>
        List of leaf ComponentNode objects

    __tree : dict<ComponentNode: list<ComponentNode>>
        Tree representation of the Drawflow composition representing the true
        hierarchy of components.

    __height : int
        Height of the tree.

    Methods
    -------
    Public methods
    --------------
    add_parent(module_name)
    add_child(parent_name, node_name, node_index, node_type, node_links,
        node_params)
    find_module(node_name)
    decompress()
    get_leaves()
    get_height()
    get_tree()

    Private methods
    ---------------
    __get_node_count(node_name)
    __get_children(node)
    __decompress(node)
    __get_leaves(subtree, depth)
    """

    def __init__(self, composition: dict = None, root_key: str = "Home") -> None:
        """
        Constructor for ComponentTree

        Params
        ------
        composition: dict = None
        root_key: str = "Home"
        """
        self.__composition = composition
        self.root_key = root_key

        # if a composition is provided
        if self.__composition:
            for module in self.__composition.keys():
                if module == self.root_key:
                    self.__root = module
                    break
        else:
            self.__composition = {}
            self.__root = None

        self.__leaves = []  # <list(ComponentNode)>
        self.__tree = {}  # <dict(ComponentNode: list(ComponentNode))>
        self.__height = 0

    def add_parent(self, module_name: str):

        module_node = ComponentNode(class_name=module_name, name=module_name)
        self.__composition[module_node] = []

    def add_child(
        self,
        parent_name: str,
        node_name: str,
        node_index: int,
        node_type: str,
        node_links: list,
        node_params: str,
    ):

        module_node = self.find_module(parent_name)

        # append a new ComponentNode object with ComponentNode.class_name
        self.__composition[module_node].append(ComponentNode(class_name=node_name))
        node = self.__composition[module_node][node_index]

        node.set_parent(parent_name)
        node_count = self.__get_node_count(node_name)
        node.set_name(self.__get_node_name(node_name, node_count))
        node.set_type(node_type)
        node.set_links(node_links)
        node.set_params(node_params)

    def __get_node_name(self, node_name: str, count: int) -> str:

        return f"{node_name}#{count}"

    def __get_node_count(self, node_name: str) -> int:

        count = -1
        for module in self.__composition.keys():
            count += self.__composition[module].count(node_name)

        return count

    def find_module(self, node_name: str):

        for module in self.__composition.keys():
            if module == node_name:
                return module

    def __get_children(self, node: ComponentNode) -> list:

        for module in self.__composition:
            if module == node:
                return [
                    ComponentNode(
                        class_name=i.class_name,
                        type=i.type,
                        parent=i.parent,
                        name=i.name,
                        links=i.links,
                        params=i.params,
                    )
                    for i in self.__composition[module]
                ]

        return []

    def __decompress(self, node: ComponentNode) -> dict:
        return {node: [self.__decompress(n) for n in self.__get_children(node)]}

    def decompress(self) -> dict:

        self.__root = self.find_module(self.root_key)
        self.__tree = self.__decompress(self.__root)

    def __get_leaves(self, subtree: dict, depth: int = 0) -> None:

        for key, value in subtree.items():
            if not value:
                self.__leaves.append(key)
                self.__height = max(self.__height, depth)

            for node in value:
                self.__get_leaves(node, depth + 1)

    def get_leaves(self) -> list:

        self.__get_leaves(self.__tree)
        return self.__leaves

    def get_height(self) -> int:

        return self.__height

    def get_tree(self) -> dict:

        return self.__tree
