import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime
import time

# ---------------- 설정 ----------------
genai.configure(api_key="AIzaSyDVpKMT594xfTU2XGVrFo-tLk0y4TgxSMc")

SYSTEM_PROMPT = """
당신은 고객 응대 전문 상담사입니다.
1) 사용자는 불안감 해소를 위한 다양한 고민들을 언급합니다. 친근하고, 공감 어린 말투로 응답하세요.
2) 사용자의 감정을 구체적으로 정리하여(무엇이/언제/어디서/어떻게) 수집하고, 고객에게 맞는 고민과 요구사항을 안내하세요.
3) 마지막에는 “더 많은 상담소와 전화번호 등을 보내드릴까요?”라고 물어보세요.
   만일 사용자가 원치 않으면 “당신의 모든 고민들을 들어드릴게요, 다음에 또 편하게 말해주세요.”라고 정중히 안내하세요.
"""

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="AI 고객 상담 챗봇", page_icon="💬", layout="wide")
st.title("💬 Gemini 기반 AI 고객 상담 챗봇")

model_choice = st.selectbox(
    "모델 선택:",
    ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
    index=0
)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# CSV 저장 옵션
save_csv = st.sidebar.checkbox("대화 자동 CSV 저장", value=False)

# ---------------- 챗봇 함수 ----------------
def chat_with_gemini(prompt):
    try:
        model = genai.GenerativeModel(model_choice, system_instruction=SYSTEM_PROMPT)
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        st.error(f"⚠️ 오류 발생: {str(e)}")
        time.sleep(2)
        return "죄송합니다. 잠시 후 다시 시도해주세요."

# ---------------- 대화 영역 ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("고객님의 고민을 말씀해주세요."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = chat_with_gemini(user_input)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

    # CSV 자동 저장
    if save_csv:
        df = pd.DataFrame(st.session_state.messages)
        df.to_csv("chat_log.csv", index=False)

# ---------------- 로그 관리 ----------------
st.sidebar.download_button(
    label="📥 대화 로그 다운로드 (CSV)",
    data=pd.DataFrame(st.session_state.messages).to_csv(index=False),
    file_name=f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)

if st.sidebar.button("🧹 대화 초기화"):
    st.session_state.messages = []
    st.experimental_rerun()

st.sidebar.caption("세션 유지: 최근 6턴 이후 자동 리셋 (429 대응용)")
st.sidebar.info(f"현재 모델: {model_choice}")

