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
    response_list = responses.split(",")

    categorized_responses = {
        "positive": [],
        "negative": [],
        "neutral": []
    }

    for response in response_list:
        analyzed_sentiment = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Classify the sentiment of the following text as positive, negative, or neutral:\n\n{response}"}
            ]
        )
        sentiment = analyzed_sentiment.choices[0].message.content.strip()

        if sentiment in categorized_responses:
            categorized_responses[sentiment].append(response)
    
    sentiment_summaries = {}
    for sentiment, responses in categorized_responses.items():
        if responses:
            combined_responses = ",".join(responses)
            analyzed_summary = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "This is a task to create a formal, detailed summary in Japanese, focusing on the '{sentiment}' responses to a specific question. The summary should capture the key themes and reasons behind the sentiments expressed, suitable for direct inclusion in a report. It should be concise, informative, and reflect the nuances of Japanese language."
                    },
                    {
                        "role": "user",
                        "content": f"Please provide a structured summary in Japanese of the '{sentiment}' responses to the question '{question}'. The summary should elucidate the key themes and reasons for these sentiments, formatted for direct use in a report."
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