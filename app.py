from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

# Load your OpenAI key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_bot(data: Question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": data.question}]
        )
        answer = response.choices[0].message.content
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}