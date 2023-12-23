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
                        {
                            "role": "system",
                            "content": "This is a task to summarize the key themes and reasons behind the sentiments expressed in the provided responses, related to a specific question. The summary should be concise, informative, and in Japanese."
                        },
                        {
                            "role": "user",
                            "content": f"The following are responses related to the question '{question}'. Please summarize the key themes and reasons behind the sentiments expressed in these responses."
                        },
                        {
                            "role": "assistant",
                            "content": combined_responses
                        }
                    ]
            )
            sentiment_summaries[sentiment] = {
                "responses": responses,
                "summary": analyzed_summary.choices[0].message.content,
            }
    return sentiment_summaries