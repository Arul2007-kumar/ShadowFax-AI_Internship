from pydantic import BaseModel

class source(BaseModel):
    document_id:str
    filename:str
    page:int|None=None
    chunk_id:int
    score:float


class AnswerResponse(BaseModel):
    answer:str
    sources:list[source]
    confidence:float
    retrieved_chunks:list[str]