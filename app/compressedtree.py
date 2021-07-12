un = [
    {
        "class": "four",
        "id": 11,
        "links": [{"from_port": "cout__4__8", "to_id": 12, "to_port": "cin__7"}],
        "module": "eight",
        "name": "four#0%eight#0",
    },
    {
        "class": "four",
        "id": 12,
        "links": [],
        "module": "eight",
        "name": "four#1%eight#0",
    },
    {
        "class": "fulladder",
        "id": 3,
        "links": [{"from_port": "cout", "to_id": 4, "to_port": "cin"}],
        "module": "two",
        "name": "fulladder#0%two#1",
    },
    {
        "class": "fulladder",
        "id": 4,
        "links": [],
        "module": "two",
        "name": "fulladder#1%two#1",
    },
    {
        "class": "fulladder",
        "id": 3,
        "links": [{"from_port": "cout", "to_id": 4, "to_port": "cin"}],
        "module": "two",
        "name": "fulladder#0%two#2",
    },
    {
        "class": "fulladder",
        "id": 4,
        "links": [],
        "module": "two",
        "name": "fulladder#1%two#2",
    },
    {"class": "two", "id": 7, "links": [], "module": "four", "name": "two#0%four#3"},
    {
        "class": "two",
        "id": 8,
        "links": [{"from_port": "cout__4", "to_id": 7, "to_port": "cin__3"}],
        "module": "four",
        "name": "two#1%four#3",
    },
    {"class": "two", "id": 7, "links": [], "module": "four", "name": "two#0%four#4"},
    {
        "class": "two",
        "id": 8,
        "links": [{"from_port": "cout__4", "to_id": 7, "to_port": "cin__3"}],
        "module": "four",
        "name": "two#1%four#4",
    },
]
from pprint import pprint


class CompressedNode:
    def __init__(self, class_name, option=0) -> None:

        self.class_name = class_name
        self.option = option
        self.data = {}
        self.children = []

    def __repr__(self) -> str:
        return f"{self.class_name}, {self.option}"

    def __eq__(self, other) -> bool:
        if isinstance(other, CompressedNode):
            return self.class_name == other.class_name

    def __hash__(self) -> int:
        return hash(self.class_name)


class CompressedTree:
    def __init__(self) -> None:
        self.root = CompressedNode("root")

        self.tree = [
            {
                "node": CompressedNode("root"),
                "children": [CompressedNode("a", option=8)],
            },
            {
                "node": CompressedNode("a"),
                "children": [
                    CompressedNode("b"),
                    CompressedNode("b", option=8),
                ],
            },
            {
                "node": CompressedNode("b"),
                "children": [
                    CompressedNode("c"),
                    CompressedNode("c"),
                    CompressedNode("c", option=8),
                ],
            },
            {"node": CompressedNode("c"), "children": [CompressedNode("d")]},
        ]

    def chain(self) -> None:

        self.compressed = {e["node"]: e["children"] for e in self.tree}

    def __get_children(self, node) -> list:

        for parent in self.compressed:
            if parent == node:
                return self.compressed[parent]

        return []

    def decompress(self, node) -> dict:
        return {node: [self.decompress(n) for n in self.__get_children(node)]}


tree = CompressedTree()
tree.chain()
pprint(tree.decompress(tree.root))
