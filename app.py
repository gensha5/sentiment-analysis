import streamlit as st
import requests
import matplotlib.pyplot as plt

st.title("自由記述欄を自動分析する")

question = st.text_input("質問文を入力してください。")
responses = st.text_area("自由記述欄の回答を入力してください。コンマ区切りで入力してください。", height=300)

if st.button("分析する"):
    response = requests.post("http://localhost:8000/", data={"question": question, "responses": responses})
    # response = requests.post("https://sentiment-analysis-lf56.onrender.com", data={"question": question, "responses": responses})
    if response.status_code == 200:
        results = response.json()

        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        for sentiment in ["positive", "negative", "neutral"]:
            if sentiment in results:
                sentiment_counts[sentiment] = len(results[sentiment]['responses'])
        fig, ax = plt.subplots()
        ax.pie(sentiment_counts.values(), labels=sentiment_counts.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)


        for sentiment in ["positive", "negative", "neutral"]:
            if sentiment in results:
                st.subheader(f"{sentiment.title()}")
                st.write(f"回答数: {len(results[sentiment]['responses'])}")
                st.write("要約:")
                st.write(results[sentiment]['summary'])
                st.write("回答一覧:")
                for item in results[sentiment]['responses']:
                    st.text(item)
    else:
        st.error(f"Error: Status code {response.status_code}")

