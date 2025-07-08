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

# --- Prompt Template for Meditation ---
meditation_prompt = ChatPromptTemplate.from_template("""
You are a Biblical meditation guide. Create a reflective meditation for the topic: {topic}.

Structure:
1. Scripture Focus (with reference)
2. Meditation Prompt 1: "What does this reveal about God?"
3. Meditation Prompt 2: "How can I live this out today?"
4. Breathing Guide (e.g., Inhale 4s → Hold 4s → Exhale 4s)

Keep it calming, peaceful, and focused on truth.
""")

meditation_chain = meditation_prompt | llm | StrOutputParser()

def generate_meditation(topic):
    return meditation_chain.invoke({"topic": topic})


# --- Meditation Page Renderer ---
def render_meditation():
    st.title("🧘 Daily Meditation")

    topics = [
        "Peace", "God’s Presence", "Strength", "Wisdom", "Faith", "Something else..."
    ]

    topic = st.selectbox("Choose a topic", topics)

    if topic == "Something else...":
        topic = st.text_input("Enter your own topic")

    if st.button("Begin Meditation"):
        if topic:
            with st.spinner("Generating your meditation..."):
                output = generate_meditation(topic)
                st.markdown("### 🧘 Meditation Guide")
                for section in output.split("\n"):
                    if section.strip():
                        st.markdown(f"**{section.split(':')[0]}:** {':'.join(section.split(':')[1:]).strip()}")

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
