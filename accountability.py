import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

# --- Groq LLM Setup ---
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-70b-8192"
)

# --- Prompt Template for Accountability ---
accountability_prompt = ChatPromptTemplate.from_template("""
You are an accountability partner and spiritual guide. Help someone resist the temptation of: {topic}

Give:
1. Scripture for Strength (with reference)
2. Truth Declaration (e.g., “I am not a slave to sin...”)
3. Alternative Action Suggestion (Instead of {topic}, do ...)
4. SOS Encouragement – Quick verse and 1-line action plan if they need urgent help

Keep it grounded in hope and truth.
""")

accountability_chain = accountability_prompt | llm | StrOutputParser()

def generate_accountability(topic):
    return accountability_chain.invoke({"topic": topic})


# --- Accountability Page Renderer ---
def render_accountability():
    st.title("🛡️ Daily Accountability")

    topics = [
        "Pornography", "Alcohol", "Drugs", "Sex", "Addiction", "Laziness", "Something else..."
    ]

    topic = st.selectbox("Choose an area you’re working on", topics)

    if topic == "Something else...":
        topic = st.text_input("Enter your own area of struggle")

    if st.button("Generate Accountability Plan"):
        if topic:
            with st.spinner("Preparing spiritual guidance..."):
                output = generate_accountability(topic)
                st.markdown("### 🛡️ Accountability Support")
                for section in output.split("\n"):
                    if section.strip():
                        st.markdown(f"**{section.split(':')[0]}:** {':'.join(section.split(':')[1:]).strip()}")

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
