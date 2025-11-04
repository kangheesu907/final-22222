import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="고객 응대 AI 챗봇", page_icon="💬")

# Google Gemini API 설정
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

st.title("💬 고객 응대 AI 챗봇")
st.write("불편사항이나 고민을 말씀해 주세요. 친절히 도와드릴게요.")

# 모델 선택
model_name = st.selectbox("모델 선택", ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"])

# 대화 기록 저장
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 입력
user_input = st.text_area("✏️ 메시지를 입력하세요", "")

# 버튼
if st.button("전송"):
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # 시스템 프롬프트
        system_prompt = (
            "당신은 친절한 고객 응대 AI 상담원입니다. "
            "사용자의 불안과 고민을 경청하며 공감하고, 감정을 구체적으로 정리하세요. "
            "마지막에는 '더 많은 상담소와 전화번호 등을 보내드릴까요?'라고 제안하세요. "
            "만약 사용자가 원치 않으면 '당신의 모든 고민들을 들어드릴게요, 다음에 또 편하게 말해주세요.'라고 말하세요."
        )

        try:
            model = genai.GenerativeModel(model_name)
            chat = model.start_chat(history=st.session_state.chat_history)
            response = chat.send_message(f"{system_prompt}

{user_input}")
            answer = response.text
        except Exception as e:
            answer = f"⚠️ 오류 발생: {e}"

        st.session_state.chat_history.append({"role": "assistant", "content": answer})
    else:
        st.warning("메시지를 입력해주세요.")

# 대화 표시
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"👤 **고객:** {msg['content']}")
    else:
        st.markdown(f"🤖 **상담원:** {msg['content']}")

# 초기화 버튼
if st.button("대화 초기화"):
    st.session_state.chat_history = []
    st.success("대화가 초기화되었습니다.")
