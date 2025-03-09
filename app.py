from openai import OpenAI
import streamlit as st

openai_api_key = st.secrets.get("OPENAI_API_KEY")
PASSWORD = st.secrets.get("PASSWORD")

st.set_page_config(page_title="Simbionte´s Assistant", page_icon="🧬", layout="wide")

with st.sidebar:
    st.image("logo.png")
    st.markdown(
        """
    ### Core Business Elements
    - 🎯 Mission
    - 👀 Vision
    - ⭐ Values (up to 3)
    - 💡 Value Proposition
    - 🛍️ Products or Services
    - 🎯 Goals
    
    ### Customer Analysis
    **For each ICP (Ideal Customer Profile):**
    - 😣 Pain Description
    - 💪 Pain Point of View
    - 📊 Pain Goal
    - 🛒 Buying Behavior
    
    ### Strategic Targets
    - 🎯 Other Non-Customer Targets
    """
    )


st.title("Digital Marketing Onboarding")
st.caption("🚀 Powered by Simbionte")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password_input = st.text_input("Please enter the password:", type="password")
    if password_input:
        if password_input == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
    st.stop()

if "messages" not in st.session_state:
    SYSTEM_PROMPT = st.secrets.get("SYSTEM_PROMPT")
    st.session_state["messages"] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "assistant",
            "content": "Hello! I’m Simbionte’s assistant, here to help you refine your company’s positioning and messaging.",
        },
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(
        model="gpt-4o", messages=st.session_state.messages, temperature=0
    )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
