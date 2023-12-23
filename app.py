import streamlit as st
import requests

st.title("自由記述欄を自動分析する")

question = st.text_input("質問文を入力してください。")
responses = st.text_area("自由記述欄の回答を入力してください。\n1回答1行で入力してください。", height=300)

if st.button("分析する"):
    response = requests.post("https://sentiment-analysis-lf56.onrender.com", data={"responses": responses})
    results = response.json()

    if "positive" in results:
        st.subheader("ポジティブ")
        st.write(f"回答数: {len(results['positive'])}")
        st.write("回答:")
        for item in results["positive"]:
            st.text(item)

    if "negative" in results:
        st.subheader("ネガティブ")
        st.write(f"回答数: {len(results['negative'])}")
        st.write("回答:")
        for item in results["negative"]:
            st.text(item)

    if "neutral" in results:
        st.subheader("ニュートラル")
        st.write(f"回答数: {len(results['neutral'])}")
        st.write("回答:")
        for item in results["neutral"]:
            st.text(item)
