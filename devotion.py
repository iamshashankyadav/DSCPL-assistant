import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage
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
    max_tokens=500
)

# --- Prompt Setup ---

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are DSCPL, a Christian devotional assistant. Generate a spiritual plan for the user based on the selected topic and duration.\n"
     "Each day's output should include:\n"
     "- Scripture\n- Short Prayer\n- Declaration\n- Optional Video Title\n"
     "Respond in format:\nDay 1:\nScripture: ...\nPrayer: ...\nDeclaration: ...\nVideo: ..."),
    ("human", "{input}")
])


parser = StrOutputParser()

chain = prompt | llm | parser

def render_devotion():
    st.markdown("""
        <h2 style='color:#6f42c1;'>✝️ Daily Devotion</h2>
        <p>Select a topic and duration to receive a personalized spiritual growth plan.</p>
    """, unsafe_allow_html=True)

    topics = [
        "Dealing with Stress",
        "Overcoming Fear",
        "Conquering Depression",
        "Relationships",
        "Healing",
        "Purpose & Calling",
        "Anxiety",
        "Something else..."
    ]

    selected_topic = st.selectbox("Select a devotion topic:", topics)
    num_days = st.number_input("How many days would you like the plan for?", min_value=1, max_value=7, value=5)

    if st.button("Generate My Devotion Plan ✨"):
        with st.spinner("Praying and preparing your devotional..."):
            input_text = f"Topic: {selected_topic}\nDuration: {num_days} Days"
            output = chain.invoke({"input": input_text})

            for section in output.split("\n\n"):
                if section.strip():
                    st.markdown(f"<div style='padding: 15px; background-color: #272740; border-radius: 10px; margin-bottom: 10px;'>"
                                f"<pre style='font-family:Segoe UI; font-size:15px;'>{section.strip()}</pre></div>", unsafe_allow_html=True)

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
