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
    max_tokens=600
)

# --- Prompt Setup ---
prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are DSCPL, a Christian accountability companion. Generate a spiritual accountability plan for the given topic and duration.\n"
     "Each day's response should include:\n"
     "- Scripture for Strength\n"
     "- Truth Declaration\n"
     "- Alternative Action (what to do instead of the vice)\n"
     "- SOS Encouragement (short message of grace + action plan)\n\n"
     "Respond in format:\n"
     "Day 1:\n"
     "Scripture: ...\n"
     "Declaration: ...\n"
     "Alternative Action: ...\n"
     "SOS Encouragement: ...\n\n"
     "Repeat for each day."),
    ("human", "{input}")
])

parser = StrOutputParser()
chain = prompt | llm | parser

def render_accountability():
    st.markdown("""
        <h2 style='color:#FF4500;'>🛡️ Daily Accountability</h2>
        <p>Choose a struggle area and duration to receive a strength-building, grace-centered action plan.</p>
    """, unsafe_allow_html=True)

    topics = [
        "Pornography",
        "Alcohol",
        "Drugs",
        "Sex",
        "Addiction",
        "Laziness",
        "Something else..."
    ]

    selected_topic = st.selectbox("Select an area of accountability:", topics)
    num_days = st.number_input("How many days would you like the plan for?", min_value=1, max_value=30, value=7)

    if st.button("Generate My Accountability Plan ✨"):
        with st.spinner("Equipping you with truth and grace..."):
            input_text = f"Topic: {selected_topic}\nDuration: {num_days} Days"
            output = chain.invoke({"input": input_text})

            for section in output.split("\n\n"):
                if section.strip():
                    st.markdown(f"<div style='padding: 15px; background-color: #272740; border-radius: 10px; margin-bottom: 10px;'>"
                                f"<pre style='font-family:Segoe UI; font-size:15px;'>{section.strip()}</pre></div>", unsafe_allow_html=True)

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
