import streamlit as st
from openai import OpenAI
import base64

st.title("GPT-6 Luna에게 질문하기")


# ==========실습3
@st.cache_data
# 입력 받으면 답변 생각하고 답변하는 기능
def ask_gpt(_client, question):
  response = _client.responses.create(
    model="gpt-6-luna",
    input=question,
  )
  return response.output_text

ques = st.text_input("질문을 입력하세요 : ")

if(ques):
    if("OpenAI_API" not in st.session_state):
        st.warning("API KEY 부터 입력하시고 오세요")
    else :
        with st.spinner("답변중.."):
            answer = ask_gpt(st.session_state["OpenAI_API"], ques)
        st.write(answer)

# ==============실습4
st.divider()
st.subheader("이미지 생성")

prompt = st.text_input("그리고 싶은 이미지의 프롬프트 입력")

if st.button("이미지 생성"):
  if "OpenAI_API" not in st.session_state:
    st.warning("API KEY 부터 입력하숑")
  elif not prompt:
    st.warning("이미지 설명이 없는뎁숑")
  else:
    client = st.session_state["OpenAI_API"]
    with st.spinner("이미지 생성중.. 수십 초 걸릴 수 있어요"):
      img = client.images.generate(
        model="gpt-image-2.6-flare",
        prompt=prompt,
      )
    st.session_state["image_bytes"] = base64.b64decode(img.data[0].b64_json)

if "image_bytes" in st.session_state:
  st.image(st.session_state["image_bytes"])