from pydantic import BaseModel
from typing import List

class InputJson(BaseModel):
    code: str
    language: str
    testcases : List[str]
