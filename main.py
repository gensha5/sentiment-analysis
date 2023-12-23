from fastapi import FastAPI, Form
from openai import OpenAI
import os

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

@app.get("/analyze")
async def analyze(responses: str = Form(...)):
    respose_list = responses.split(",")

    positive_responses = []
    negative_responses = []
    neutral_responses = []

    for response in respose_list:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messeages=[
                {"role": "user", "content": f"Classify the sentiment of the following text as positive, negative, or neutral:\n\n{response}"}
            ]
        )