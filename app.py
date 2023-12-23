import streamlit as st
import requests

st.title("自由記述欄を自動分析する")

responses = st.text_area("自由記述欄の回答を入力してください。\n1回答1行で入力してください。", height=300)

if st.button("分析する"):
    response = requests.post("https://sentiment-analysis-lf56.onrender.com", data={"responses": responses})
    results = response.json()

    for sentiment, items in results.items():
        st.subheader(f"{sentiment.title()}")
        st.write(f"回答数: {len(items)}")
        st.write("回答:")
        for item in items:
            st.text(item)