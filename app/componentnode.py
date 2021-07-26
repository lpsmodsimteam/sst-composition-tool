class ComponentNode:
    def __init__(
        self,
        class_name: str = None,
        type: int = 0,
        name: str = None,
        links: list = None,
        module: str = None,
    ) -> None:

        self.class_name = class_name
        self.name = name
        self.type = type
        self.links = links
        self.module = module
        self.id = id(self)

    def set_class_name(self, class_name: str) -> None:
        self.class_name = class_name

    def set_type(self, type: int) -> None:
        self.type = type

    def set_links(self, links: list) -> None:
        self.links = links

    def set_module(self, module: str) -> None:
        self.module = module

    def set_name(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        # debugging method
        rep = ""
        if self.links:
            rep += " | "
            for link in self.links:
                rep += f'{link["from_port"]}/{link["to_node_type"]}/{link["to_port"]}'
                if len(self.links) > 1:
                    rep += ",\n"
        return f"{self.class_name}({self.type})/{str(self.id)[-5:]}" + rep

    def __eq__(self, other) -> bool:

        if isinstance(other, ComponentNode):
            return self.class_name == other.class_name

        elif isinstance(other, str):
            return self.class_name == other

        elif isinstance(other, int):
            return self.id == other

        raise TypeError(
            f"No methods implemented to check equality between 'ComponentNode' and {type(other)}"
        )

    def __hash__(self) -> int:
        return hash(self.id)
