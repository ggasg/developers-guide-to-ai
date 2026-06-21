from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from ollama import Client
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

client = Client()

class ChatRequest(BaseModel):
    question: str

# Sends a prompt to the local LLM
def generate_stream(question: str):
    result = client.generate(stream=True, model="llama3.2", prompt=question)

    for chunk in result:
        if chunk.response:
            print(chunk)
            yield chunk.response

@app.post("/")
def chat(chatRequest: ChatRequest):
    return StreamingResponse(
        generate_stream(chatRequest.question),
        media_type="text/plain")