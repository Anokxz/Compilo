from pydantic import BaseModel
from typing import List

class InputJson(BaseModel):
    code: str
    language: str
    testcases : List[str]

class TestCaseResult(BaseModel):
    stdout: str
    stderr: str
    execution_time: float = 0
    return_code: int

class OutputJson(BaseModel):
    status: str
    compilation: dict
    testcases: List[TestCaseResult]