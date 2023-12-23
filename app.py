import streamlit as st
import requests

st.title("自由記述欄を自動分析する")

question = st.text_input("質問文を入力してください。")
responses = st.text_area("自由記述欄の回答を入力してください。\n1回答1行で入力してください。", height=300)

if st.button("分析する"):
    response = requests.post("https://sentiment-analysis-lf56.onrender.com", data={"question": question, "responses": responses})
    results = response.json()

    for sentiment in ["positive", "negative", "neutral"]:
        if sentiment in results:
            st.subheader(f"{sentiment.title()}")
            st.write(f"回答数: {len(results[sentiment]['responses'])}")
            st.write("要約:")
            st.write(results[sentiment]['summary'])
            st.write("回答一覧:")
            for item in results[sentiment]['responses']:
                st.text(item)