from fastapi import FastAPI, Form
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
)

@app.get("/analyze")
async def analyze(responses: str = Form(...)):
    respose_list = responses.split(",")

    positive_responses = []
    negative_responses = []
    neutral_responses = []

    for response in respose_list:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messeages=[
                {"role": "user", "content": f"Classify the sentiment of the following text as positive, negative, or neutral:\n\n{response}"}
            ]
        )
        sentiment = chat_completion.choices[0].messeage

        if sentiment == "positive":
            positive_responses.append(response)
        elif sentiment == "negative":
            negative_responses.append(response)
        else:
            neutral_responses.append(response)

    return {
        "positive": positive_responses,
        "negative": negative_responses,
        "neutral": neutral_responses
    }