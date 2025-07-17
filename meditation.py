import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# --- Load env ---
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# --- LLM Setup ---
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-70b-8192",
    max_tokens=1000
)

# --- Prompt Setup ---
prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are DSCPL, a Christian meditation assistant. Generate a daily spiritual meditation plan.\n"
     "Each day's content should include:\n"
     "- Scripture focus (1 verse with reference)\n"
     "- Meditation prompts:\n"
     "   1. What does this reveal about God?\n"
     "   2. How can I live this out today?\n"
     "Add a simple breathing reminder at the end of each day.\n\n"
     "Format:\n"
     "Day 1:\n"
     "Scripture: ...\n"
     "Reflect:\n"
     "- What does this reveal about God?\n"
     "- How can I live this out today?\n"
     "Breathing Reminder: Inhale 4s → Hold 4s → Exhale 4s\n\n"
     "Repeat for each day."),
    ("human", "{input}")
])

parser = StrOutputParser()
chain = prompt | llm | parser

def render_meditation():
    st.markdown("""
        <h2 style='color:#7B68EE;'>🧘 Daily Meditation</h2>
        <p>Select a topic and number of days to begin your scripture-centered meditation practice.</p>
    """, unsafe_allow_html=True)

    topics = [
        "Peace",
        "God's Presence",
        "Strength",
        "Wisdom",
        "Faith",
        "Something else..."
    ]

    selected_topic = st.selectbox("Select a meditation topic:", topics)
    num_days = st.number_input("How many days would you like the plan for?", min_value=1, max_value=30, value=7)

    # Add lightweight breathing animation
    st.markdown("""
        <div style="text-align:center; margin-top: 10px; margin-bottom: 20px;">
            <div style="font-size:16px; margin-bottom:10px;">Breathe With Me</div>
            <div style="
                width: 100px;
                height: 100px;
                background-color: #e0e0ff;
                border-radius: 50%;
                animation: pulse 6s infinite;">
            </div>
        </div>
        <style>
        @keyframes pulse {
            0% { transform: scale(1); }
            25% { transform: scale(1.25); }
            50% { transform: scale(1.5); }
            75% { transform: scale(1.25); }
            100% { transform: scale(1); }
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("Generate My Meditation Plan ✨"):
        with st.spinner("Preparing your spiritual reflections..."):
            input_text = f"Topic: {selected_topic}\nDuration: {num_days} Days"
            output = chain.invoke({"input": input_text})

            for section in output.split("\n\n"):
                if section.strip():
                    st.markdown(f"<div style='padding: 15px; background-color: #272740; border-radius: 10px; margin-bottom: 10px;'>"
                                f"<pre style='font-family:Segoe UI; font-size:15px;'>{section.strip()}</pre></div>", unsafe_allow_html=True)

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
