from typing import List, Optional, Literal
from enum import Enum, EnumMeta
from dataclasses import dataclass, field

@dataclass
class Config:
    model_dir: Optional[str] = field(
        default=None, metadata={"help": "llm model dir"}
    )
    reward_model_dir: Optional[str] = field(
        default=None, metadata={"help": "reward model dir"}
    )
    positive_reward: float = field(
        default=1.0, metadata={"help": "reward for positive example"}
    )
    negative_reward: float = field(
        default=-1.0, metadata={"help": "reward for negative example"}
    )


    batch_size: int = field(
        default=10, metadata={"help": "batch size for batch inference"}
    )
    iterations: int = field(
        default=8, metadata={"help": "number of simulation iterations"}
    )
    max_depth: int = field(
        default=12, metadata={"help": "maximum depth of the tree, ie., maximum steps of completion."}
    )
