"""
Represent the entire Drawflow node structure as a ComponentTree composed of
ComponentNode objects.

A ComponentTree is a tree of ComponentNode objects. Standalone, the class can
be instantiated by a raw Drawflow node structure composition data structure.
The object would however not be an accurate representation of the composition
if the Drawflow node structure contains submodules.
"""

from .node import ComponentNode


class ComponentTree:
    """
    Tree representation of Drawflow composition of nodes.

    Attributes
    ----------
    __composition: dict<ComponentNode, list<ComponentNode>> = None
        Prebuilt Drawflow composition data structure. In production, this
        parameter is always None due to the dynamic nature of the creation of
        the Drawflow compositions. The composition's keys are referred to as
        "modules" and its values as "nodes".

    root_key: str = "Home"
        The key of the root node in the composition data structure.

    __root: ComponentNode
        The root ComponentNode of the ComponentTree.

    __leaves: list<ComponentNode>
        List of leaf ComponentNode objects

    __tree: dict<ComponentNode, list<ComponentNode>>
        Tree representation of the Drawflow composition representing the true
        hierarchy of components.

    __height: int
        Height of the tree.

    Methods
    -------
    Public methods
    --------------
    add_parent(str)
    add_child(str, str, int, str, list, str)
    find_module(str)
    decompress()
    get_leaves()
    get_height()
    get_tree()

    Private methods
    ---------------
    __get_node_count(str)
    __get_children(ComponentNode)
    __decompress(ComponentNode)
    __get_leaves(dict, int)
    """

    def __init__(self, composition: dict = None, root_key: str = "Home") -> None:
        """
        Constructor for ComponentTree

        Params
        ------
        composition: dict<ComponentNode, list<ComponentNode>> = None
        root_key: str = "Home"

        Returns
        -------
        None
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

        self.__leaves: list = []  # <list(ComponentNode)>
        self.__tree: dict = {}  # <dict(ComponentNode: list(ComponentNode))>
        self.__height: int = 0

    def add_parent(self, parent_name: str) -> None:
        """
        Add a ComponentNode as a parent in the hierarchy.

        The parent node is a ComponentNode object with only its class_name
        and name assigned as parent_name. The parent node is added to the
        composition as a key with an empty list as its value.

        Params
        ------
        parent_name: str
            Name of the parent node

        Returns
        -------
        None
        """
        module_node = ComponentNode(class_name=parent_name, name=parent_name)
        self.__composition[module_node] = []

    def add_child(
        self,
        parent_name: str,
        node_name: str,
        node_index: int,
        node_type: str,
        node_links: list,
        node_params: str,
    ) -> None:
        """
        Add a ComponentNode as a child in the hierarchy.

        Params
        ------
        parent_name: str
            Name (and class_name) of the parent ComponentNode

        node_name: str
            Name of the current ComponentNode

        node_index: int
            The index of the current ComponentNode's parent's children. The
            index does not signify a precedence or priority within the
            children nodes.

        node_type: str
            The type of the current ComponentNode.

        node_links: list
            The links of the current ComponentNode.

        node_params: str
            The params of the current ComponentNode.

        Returns
        -------
        None
        """
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
        """
        Format the node name with the ComponentNode's class_name and its
        occurrence in the composition.

        Params
        ------
        node_name: str
            Name of the current ComponentNode.

        count: int
            The occurrence of the current ComponentNode's class_name in the
            composition.

        Returns
        -------
        str: the formatted name for the current ComponentNode.
        """
        return f"{node_name}#{count}"

    def __get_node_count(self, node_class_name: str) -> int:
        """
        Count the occurrence of the current ComponentNode's class_name in the
        composition.

        Params
        ------
        node_class_name: str
            Name of the current ComponentNode.

        Returns
        -------
        count: int
            the occurrence of the current ComponentNode's class_name.
        """
        count = -1
        for module in self.__composition.keys():
            count += self.__composition[module].count(node_class_name)

        return count

    def find_module(self, node_name: str) -> ComponentNode:
        """
        Find a module in the composition (parent ComponentNode) by its name.

        Params
        ------
        node_name: str
            Name of the parent ComponentNode.

        Returns
        -------
        ComponentNode: the found parent ComponentNode or
        None: if the parent ComponentNode was not found.
        """
        for module in self.__composition.keys():
            if module == node_name:
                return module

    def __get_children(self, node: ComponentNode) -> list:
        """
        Generates new copies of children nodes from a module.

        Params
        ------
        node: str
            Parent ComponentNode.

        Returns
        -------
        list<ComponentNode>: list of newly generated ComponentNode children.
        """
        # iterating through the keys
        for module in self.__composition:
            # if the module key is found
            if module == node:
                # new and unique instances of ComponentNode objects with
                # attributes identical to the original copies
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

        # node is a leaf
        return []

    def __decompress(self, node: ComponentNode) -> dict:
        """
        Decompresses the flat hierarchical data structure by Drawflow.

        This recursive method converts the following data structure:
            {
                "root": ["a"],
                "a": ["b", "b"],
                "b": ["c", "c", "c"],
                "c": ["d"],
            }
        into the following:
            {"root": [
                {"a": [
                    {"b": [
                        {"c": [
                            {"d": []}
                        ]},
                        {"c": [
                            {"d": []}
                        ]},
                        {"c": [
                            {"d": []}
                        ]}
                    ]},
                    {"b": [
                        {"c": [
                            {"d": []}
                        ]},
                        {"c": [
                            {"d": []}
                        ]},
                        {"c": [
                            {"d": []}
                        ]}
                    ]},
                ]}
            ]}

        Params
        ------
        node: str
            Parent ComponentNode.

        Returns
        -------
        dict<ComponentNode, list<dict<ComponentNode>, list...>>:
            nested, decompressed version of the composition
        """
        return {node: [self.__decompress(n) for n in self.__get_children(node)]}

    def decompress(self) -> None:
        """
        Generates the root ComponentNode objects and initializes the values for
        the recursive decompress method to generate the tree.

        Params
        ------
        None

        Returns
        -------
        None
        """
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
        """
        Generates and returns the list of leaf ComponentNode objects.

        Params
        ------
        None

        Returns
        -------
        self.__leaves: list<ComponentNode>
            list of leaf ComponentNode objects.
        """
        self.__get_leaves(self.__tree)
        return self.__leaves

    def get_height(self) -> int:
        """
        Returns the height of the ComponentTree.

        Params
        ------
        None

        Returns
        -------
        self.__height: int
            the height of the ComponentTree.
        """
        return self.__height

    def get_tree(self) -> dict:
        """
        Returns the ComponentTree.

        Params
        ------
        None

        Returns
        -------
        self.__tree: dict<ComponentNode, list<dict<ComponentNode>, list...>>
            the ComponentTree.
        """
        return self.__tree
