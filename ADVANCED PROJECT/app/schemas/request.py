from pydantic import BaseModel,Field

class QuestionRequest(BaseModel):
    question:str=Field(
        ...,
        min_length=2,
        max_length=2000,
        description="user's question"
    )
    document_id:str|None=Field(
        default=None,
        description="optional document ID"
    )
    top_k:int=Field(
        default=5,
        ge=1,
        le=20,
        description="number of chunks to retrive"
    )