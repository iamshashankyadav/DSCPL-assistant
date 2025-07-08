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

# --- Prompt Template ---
devotion_prompt = ChatPromptTemplate.from_template("""
You are a spiritual guide. Generate a structured devotional based on the topic: {topic}

Include:
1. Scripture (with reference)
2. Short Prayer
3. Faith Declaration
4. Suggested Video Title

Respond in the following format:
Scripture: ...
Prayer: ...
Declaration: ...
Video: ...
""")

devotion_chain = devotion_prompt | llm | StrOutputParser()

def generate_devotion(topic):
    return devotion_chain.invoke({"topic": topic})


# --- Devotion Page Renderer ---
def render_devotion():
    st.title("📖 Daily Devotion")

    topics = [
        "Dealing with Stress", "Overcoming Fear", "Conquering Depression",
        "Relationships", "Healing", "Purpose & Calling", "Anxiety", "Something else..."
    ]

    topic = st.selectbox("Choose a topic", topics)

    if topic == "Something else...":
        topic = st.text_input("Enter your own topic")

    if st.button("Generate Devotion"):
        if topic:
            with st.spinner("Generating devotion..."):
                output = generate_devotion(topic)
                st.markdown("### 🙏 Your Devotion")
                for section in output.split("\n"):
                    if section.strip():
                        st.markdown(f"**{section.split(':')[0]}:** {':'.join(section.split(':')[1:]).strip()}")

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
