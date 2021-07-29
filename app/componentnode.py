class ComponentNode:
    def __init__(
        self,
        class_name: str = None,
        type: int = 0,
        name: str = None,
        parent: str = None,
        links: list = None,
        params: str = None,
    ) -> None:

        self.class_name = class_name
        self.type = type
        self.name = name
        self.parent = parent
        self.links = links
        self.params = params
        self.id = id(self)

    def set_class_name(self, class_name: str) -> None:
        self.class_name = class_name

    def set_type(self, type: int) -> None:
        self.type = type

    def set_name(self, name: str) -> None:
        self.name = name

    def set_parent(self, parent: str) -> None:
        self.parent = parent

    def set_links(self, links: list) -> None:
        self.links = links

    def set_params(self, params: str) -> None:
        self.params = params

    def __repr__(self) -> str:
        # debugging method
        return f"{self.class_name}{str(self.id)[-5:]}"

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
