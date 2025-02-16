from typing import Dict, Optional, Type, List
from tot_reasoning.constants import (
    LOW_SCORE_STEP,LOW_SCORE_STEP_END,
    HIGH_SCORE_STEP,HIGH_SCORE_STEP_END,
    CURRENT_STEP,CURRENT_STEP_END)

from tot_reasoning.base.base_node import BaseNode
from tot_reasoning.base.base_tree import BaseTree


class TotTree(BaseTree):
    intermediate_metric: Dict = {
        "question": "",
        "gt": "",
        "answers": [],
        "judgements": [],
        "value_estimate": [],
        "rollout_indexs": [],
    }

    def create_prompt(self)->str:
        promts = []
        for i , node in enumerate(self.candidate_nodes):
            left_node = self.candidate_nodes[i - 1] if i > 0 else None
            right_node = self.candidate_nodes[i + 1] if i < len(self.candidate_nodes) - 1 else None
            left_branch = self.collect_partial_solution(left_node) if left_node else ""
            current_branch = self.collect_partial_solution(node)
            right_branch = self.collect_partial_solution(right_node) if right_node else ""
            prompt = (
                f"{LOW_SCORE_STEP}{left_branch}{LOW_SCORE_STEP_END}\n"
                f"{CURRENT_STEP}{current_branch}{CURRENT_STEP_END}\n"
                f"{HIGH_SCORE_STEP}{right_branch}{HIGH_SCORE_STEP_END}"
            ).strip()
            promts.append(prompt)
        return promts


    #TODO: Need to implmet using llm
    def reward_step(self,context:str)->float:
        return random.uniform(-1, 1)

    #TODO: Need to implmet using llm
    def generate_steps(self,left_branch:str,current_branch:str,right_branch:str)->str:
        promt = self.create_prompt()
        return f"Generated step based on: {context}"

    def create_node(self, parent: Optional[Type[BaseNode]] = None) -> Type[BaseNode]:
        return BaseNode(parent=parent)

    def shortlist_node(self) -> List[BaseNode]:
        shortlisted_node = []
        for node in self.leaf_nodes:
            if not node.is_terminated:
                shortlisted_node.append(node)
        return shortlisted_node
