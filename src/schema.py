import pydantic
from typing import List

class Transition(pydantic.BaseModel):
    src: str
    tgt: str

    def __str__(self):
        return f"{self.src} -> {self.tgt}"
    
    def __repr__(self):
        return str(self)
    
    # Check if transition is non-empty
    @pydantic.model_validator(mode="after")
    def check_transition(self):
        if len(self.src) == 0 and len(self.tgt) == 0:
            raise ValueError("Transition is empty")
        return self
    

class Problem(pydantic.BaseModel):
    """
    {
        “problem_id”: “000”,
        "initial_string": "HELLOWORLD",
        "transitions": [
            {
                "src": "HELLO",
                "tgt": ""
            },
            {
                "src": "WORLD",
                "tgt": "”
            }
        ]
    }
    """
    problem_id: str
    initial_string: str
    transitions: List[Transition]

    # Check if the list is non-empty
    @pydantic.model_validator(mode="after")
    def check_transitions(self):
        if not self.transitions:
            raise ValueError("Transitions list is empty")
        return self
        
    # Check if the initial string is non-empty
    @pydantic.model_validator(mode="after")
    def check_initial_string(self):
        if len(self.initial_string) == 0:
            raise ValueError("Initial string is empty")
        return self
        
    # Check if there exists a transition with an empty target
    @pydantic.model_validator(mode="after")
    def check_empty_target(self):
        for transition in self.transitions:
            if len(transition.tgt) == 0:
                return self
        raise ValueError("No transition with empty target found")

class Solution(pydantic.BaseModel):
    """
    {
        “problem_id”: “000”,
        “solution”: [0, 1]
    }
    """
    problem_id: str
    solution: List[int]

    # Check if the solution list is non-empty
    @pydantic.model_validator(mode="after")
    def check_solution(self):
        if len(self.solution) == 0:
            raise ValueError("Solution list is empty")
        return self