import streamlit as st
import google.generativeai as genai

st.title("Data Science Buddy - Interview Prep")
st.caption("Practice for Data Science, Analytics & Engineering interviews")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

SYSTEM_PROMPT = """You are an expert interviewer for data science, data analytics, 
and data engineering roles. Help candidates practice interviews by:
- Asking realistic interview questions
- Giving honest, constructive feedback on answers
- Explaining concepts clearly when asked
- Adjusting difficulty based on the candidate's level"""


model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=SYSTEM_PROMPT
)

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask a question or say 'give me an interview question'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(prompt)
        reply = response.text
        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})