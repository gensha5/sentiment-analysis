# このアプリについて

## URL
以下から実際に利用できます。

https://gensha5-sentiment-analysis-app-btjnpr.streamlit.app/

## 概要
アンケートの自由記述の回答を分析するアプリです。

gpt-3.5-turboによって、感情別（ポジティブ、ネガティブ、ニュートラル）に回答を分類します。

また、gpt-4によって、感情別に回答の要約を行います。

感情別に分類した後に要約を行うことで、要約の精度を向上させています。


## 技術
- Python
- FastAPI
- OpenAI API

バックエンド(`main.py`)はRender、フロントエンド(`app.py`)はStreamlit Cloudでデプロイしています。

