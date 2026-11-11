import streamlit as st

st.title("Chat")

if "OpenAI_API" not in st.session_state:
  st.info("사이드바에 OpenAI API KEY를 입력하세요")
  st.stop()

client = st.session_state["OpenAI_API"]

# 대화 기록 저장 공간 (처음 한 번만 만들기)
if "chat_messages" not in st.session_state:
  st.session_state["chat_messages"] = []

# Clear 버튼: 대화 기록 지우기
def clear_chat():
  st.session_state["chat_messages"] = []

st.button("Clear", on_click=clear_chat)

# 이전 대화 다시 그리기
for msg in st.session_state["chat_messages"]:
  with st.chat_message(msg["role"]):
    st.markdown(msg["content"])

# 새 질문 입력
if prompt := st.chat_input("메시지를 입력하세요"):
  st.chat_message("user").markdown(prompt)
  st.session_state["chat_messages"].append({"role": "user", "content": prompt})

  with st.chat_message("assistant"):
    stream = client.responses.create(
      model="gpt-6-luna",
      input=st.session_state["chat_messages"],
      stream=True,
    )
    response = st.write_stream(stream)
  st.session_state["chat_messages"].append({"role": "assistant", "content": response})
    