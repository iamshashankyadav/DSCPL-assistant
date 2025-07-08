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
                # 🧠 Apply after LLM output is received
                st.markdown("---")
                for section in output.split("\n"):
                    if section.strip() and ":" in section:
                        key, val = section.split(":", 1)
                        key = key.strip()
                        val = val.strip()

                        # Color and style selection
                        color_map = {
                            "Scripture": "#1a75ff",
                            "Prayer": "#ff6600",
                            "Declaration": "#8CCFA2",
                            "Video": "#8a2be2",
                            "Thanksgiving": "#ffcc00",
                            "Supplication": "#cc3366",
                            "Confession": "#ff6666",
                            "Adoration": "#33cccc",
                            "Daily Prayer Prompt": "#3366cc",
                            "Truth Declaration": "#009933",
                            "Alternative Action": "#ff9900",
                            "SOS Encouragement": "#cc0000",
                            "Breathing Guide": "#00b3b3",
                            "Meditation Prompt 1": "#9933ff",
                            "Meditation Prompt 2": "#663399"
                        }

                        heading_color = color_map.get(key, "#444")
                        
                        st.markdown(
                            f"""
                            <div style='margin-top:30px;'>
                                <h4 style='color:{heading_color}; font-size:22px; font-family:Georgia, serif;'>{key}</h4>
                                <div style='padding:10px; font-size:17px; font-family:Segoe UI, sans-serif; background-color:#f9f9f9; border-left: 4px solid {heading_color}; border-radius: 5px;'>
                                    {val}
                                </div>
                            </div>
                            """, unsafe_allow_html=True
                        )

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
