from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class BaseNode(BaseModel):
    is_terminal:bool = False
    is_terminated:bool = False

    error: Optional[str] = None

    parent: Optional[List[BaseNode]] = None
    children: List[BaseNode] = Field(default_factory=list)

    answer: Optional[str] = None
    text: Optional[str] = None
    reward: Optional[float] = None


    tag:str = "0"
    depth: int = 0
    consecutive_errors: int = 0

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


    def add_child(self, child: BaseNode):
        child.depth = self.depth + 1
        self.children.append(child)
        if child.parent is None:
            child.parent = []
        child.tag = f"{self.tag}.{len(self.children)+1}"
        child.parent.append(self)
        self.children.append(child)

    def is_leaf(self)-> bool:
        return not self.children

    def get_path(self)-> List[Type["BaseNode"]]:
        path = [self]
        current = self
        while current.parent and len(current.parent) > 0:
            # Take the last parent as the immediate parent.
            current = current.parent[-1]
            path.append(current)
        return path[::-1]
