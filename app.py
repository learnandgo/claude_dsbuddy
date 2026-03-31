import streamlit as st
import anthropic
import streamlit.components.v1 as components

def add_google_analytics(measurement_id):
    components.html(
        f"""
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-RP1HCVGB5E"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());
          gtag('config', 'G-RP1HCVGB5E');
        </script>
        """,
        height=0
    )
add_google_analytics("G-RP1HCVGB5E")


st.title("Data Science Buddy - Interview Prep")
st.caption("Practice for Data Science, Analytics & Engineering interviews")

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

SYSTEM_PROMPT = """You are an expert interviewer for data science, data analytics, 
and data engineering roles. Help candidates practice interviews by:
- Asking realistic interview questions
- Giving honest, constructive feedback on answers
- Explaining concepts clearly when asked
- Adjusting difficulty based on the candidate's level"""

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
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=st.session_state.messages
        )
        reply = response.content[0].text
        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})