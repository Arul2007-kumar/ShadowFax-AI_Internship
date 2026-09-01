from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
class LLMRequest(BaseModel):
    prompt:str
    content:str

@app.post("/summarisation")
def summarisation(data:LLMRequest):
    llm_input=f"""
    Instruction:{data.prompt}  
    content:{data.content}"""
    response=client.models.generate_content(
        model="gemini-3.6-flash",contents=llm_input
    )

    return{
        "response":response.text
    }
@app.post("/quizegeneration")
def quize(data:LLMRequest):
    llm_input=f"""
    Instruction:{data.prompt}  
    content:{data.content}"""
    response=client.models.generate_content(
            model="gemini-3.6-flash",contents=llm_input
    )
    
    return{
            "response":response.text
        }
@app.post("/concept")
def concept(data:LLMRequest):
    llm_input=f"""
    Instruction:{data.prompt}  
    content:{data.content}"""
    response=client.models.generate_content(
                model="gemini-3.6-flash",contents=llm_input
        )
        
    return{
        "response":response.text
        }
