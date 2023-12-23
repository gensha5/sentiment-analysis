from fastapi import FastAPI, Form
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
)

@app.post("/")
async def analyze(question: str = Form(...), responses: str = Form(...)):
    respose_list = responses.split(",")

    categorized_responses = {
        "positive": [],
        "negative": [],
        "neutral": []
    }

    for response in respose_list:
        analyzed_sentiment = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Classify the sentiment of the following text as positive, negative, or neutral:\n\n{response}"}
            ]
        )
        sentiment = analyzed_sentiment.choices[0].message.content

        if sentiment in categorized_responses:
            categorized_responses[sentiment].append(response)
    
    sentiment_summaries = {}
    for sentiment, responses in categorized_responses.items():
        if responses:
            combined_responses = ",".join(responses)
            analyzed_summary = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": f"Provide a summary in Japanese for the following responses related to the question '{question}':\n\n{combined_responses}"}
                ]
            )
            sentiment_summaries[sentiment] = {
                "responses": responses,
                "summary": analyzed_summary.choices[0].message.content,
            }
    return sentiment_summaries