# このアプリについて

## URL
以下から実際に利用できます

https://gensha5-sentiment-analysis-app-btjnpr.streamlit.app/

## 概要
このアプリはアンケートの自由記述の回答を分析し、

感情別（ポジティブ、ネガティブ、ニュートラル）に回答を分類します。

また、感情別に回答の要約を行います。


## 技術
- Python
- FastAPI
- OpenAI API (gpt-3.5-turbo)

バックエンド(`main.py`)はRender、フロントエンド(`app.py`)はStreamlit Cloudでデプロイしています。

感情別に分類した後に要約を行うことで、要約の精度を向上させています。
