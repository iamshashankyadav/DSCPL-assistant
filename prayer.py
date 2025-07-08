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

# --- Prompt Template for ACTS Prayer ---
prayer_prompt = ChatPromptTemplate.from_template("""
You are a spiritual mentor. Create a structured ACTS prayer for the topic: {topic}

Follow this format:
Adoration: ...
Confession: ...
Thanksgiving: ...
Supplication: ...
Daily Prayer Prompt: ...

Each section should be 1–2 sentences and Biblically grounded.
""")

prayer_chain = prayer_prompt | llm | StrOutputParser()

def generate_prayer(topic):
    return prayer_chain.invoke({"topic": topic})


# --- Prayer Page Renderer ---
def render_prayer():
    st.title("🙏 Daily Prayer")

    topics = [
        "Personal Growth", "Healing", "Family/Friends",
        "Forgiveness", "Finances", "Work/Career", "Something else..."
    ]

    topic = st.selectbox("Choose a topic", topics)

    if topic == "Something else...":
        topic = st.text_input("Enter your own topic")

    if st.button("Generate Prayer"):
        if topic:
            with st.spinner("Preparing your prayer..."):
                output = generate_prayer(topic)
                st.markdown("### 🙏 ACTS Prayer")
                for section in output.split("\n"):
                    if section.strip():
                        st.markdown(f"**{section.split(':')[0]}:** {':'.join(section.split(':')[1:]).strip()}")

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
