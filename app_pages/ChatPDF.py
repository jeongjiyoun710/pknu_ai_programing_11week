import streamlit as st

st.title("ChatPDF")

if "OpenAI_API" not in st.session_state:
  st.info("사이드바에 OpenAI API KEY를 입력하세요")
  st.stop()

client = st.session_state["OpenAI_API"]

# Clear: 대화 내용만 삭제
def clear_chat():
  st.session_state["pdf_messages"] = []

# Leave: vector store와 업로드한 파일 삭제 후 업로드 화면으로
def leave_pdf():
  client = st.session_state["OpenAI_API"]
  vs_id = st.session_state["pdf_vector_store_id"]
  for f in client.vector_stores.files.list(vector_store_id=vs_id):
    client.files.delete(f.id)
  client.vector_stores.delete(vs_id)
  del st.session_state["pdf_vector_store_id"]
  del st.session_state["pdf_name"]
  st.session_state["pdf_messages"] = []

# ===== 1. 아직 PDF가 없으면: 업로드 화면 =====
if "pdf_vector_store_id" not in st.session_state:
  uploaded = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")

  if uploaded is not None:
    with st.spinner("PDF를 읽고 검색 준비 중..."):
      vector_store = client.vector_stores.create(name="ChatPDF")
      client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files=[(uploaded.name, uploaded.getvalue())],
      )
    # vector store는 한 번만 만들도록 session_state에 저장
    st.session_state["pdf_vector_store_id"] = vector_store.id
    st.session_state["pdf_name"] = uploaded.name
    st.session_state["pdf_messages"] = []
    st.rerun()

  st.stop()

# ===== 2. PDF가 준비되면: 대화 화면 =====
st.caption(f"현재 파일: {st.session_state['pdf_name']}")

col1, col2 = st.columns(2)
col1.button("Clear", on_click=clear_chat, use_container_width=True)
col2.button("Leave", on_click=leave_pdf, use_container_width=True)

for msg in st.session_state["pdf_messages"]:
  with st.chat_message(msg["role"]):
    st.markdown(msg["content"])

if prompt := st.chat_input("PDF 내용에 대해 물어보세요"):
  st.chat_message("user").markdown(prompt)
  st.session_state["pdf_messages"].append({"role": "user", "content": prompt})

  with st.chat_message("assistant"):
    stream = client.responses.create(
      model="gpt-6-luna",
      instructions="업로드된 PDF 파일의 내용을 검색해서 그 내용을 근거로 답하세요. 파일에 없는 내용은 없다고 답하세요.",
      input=st.session_state["pdf_messages"],
      tools=[{
        "type": "file_search",
        "vector_store_ids": [st.session_state["pdf_vector_store_id"]],
      }],
      stream=True,
    )
    response = st.write_stream(stream)
  st.session_state["pdf_messages"].append({"role": "assistant", "content": response})