from typing import Optional, Callable, List, Any

from pydantic import BaseModel

from tot_reasoning.base.base_tree import BaseTree
from config import Config


class Solver(BaseModel):
    config: Config
    llm: Optional[Callable[[...], List[str]]] = None
    # llm_engine: Optional[LLM] = None
    iterations: int = 1
    reward_model: Optional[Any] = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.iterations = self.config.iterations


    def create_llm(self):
        engine, sampling_params = llm_engine(self.config)
        self.llm_engine = engine
        self.generate_sampling_params = sampling_params
        return partial(
            llm_generate,
            engine=self.llm_engine,
        )
    def generate_preprocess(self, agents)-> List[str]:
        prompts = []
        for agent in agents:
            prompts.extend(agent.create_prompts())
        return  prompts

    def solve(self, agents: List[BaseTree]):
            for step in range(self.config.max_depth):
                prompts = self.generate_preprocess(agents)


