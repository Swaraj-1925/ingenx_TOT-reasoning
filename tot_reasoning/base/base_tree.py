from abc import abstractmethod

from tot_reasoning.base.base_node import BaseNode
from typing import List, Optional, Type, Any
from pydantic import BaseModel
from config import Config


class BaseTree(BaseModel):
    config: Config
    question:str
    ground_truth:str
    root: Optional[Type[BaseNode]] = None
    leaf_nodes: List[Type[BaseNode]] = []
    final_answer_nodes: List[Type[BaseNode]] = []
    candidate_nodes: List[Type[BaseNode]] = []

    llm: Any = None
    r_llm: Any = None
    node_max_retry: int = 5
    rollout_idx: int = 0
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = self.create_root()
        self.current_nodes = [self.root]

    def create_root(self, parent: Optional[Type[BaseNode]] = None)-> Type[BaseNode]:
        root = self.create_node(parent)
        root.text = self.question
        return root

    @abstractmethod
    def create_node(self, parent: Optional[Type[BaseNode]] = None) -> Type[BaseNode]:
        """
        subclass must implement
        """

    def collect_partial_solution(self, node: Type[BaseNode]) -> str:
        ancestry = node.get_path()
        partial_solution = ""
        for path in ancestry:
            partial_solution += f"->{path.text}"
