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
     "You are DSCPL, a Christian prayer assistant. Generate a daily prayer plan using the ACTS model (Adoration, Confession, Thanksgiving, Supplication).\n"
     "Each day's output should include:\n"
     "- Adoration: One sentence to praise God\n"
     "- Confession: One line of honest repentance\n"
     "- Thanksgiving: One gratitude point\n"
     "- Supplication: One specific prayer request\n\n"
     "Respond in the format:\n"
     "Day 1:\n"
     "Adoration: ...\n"
     "Confession: ...\n"
     "Thanksgiving: ...\n"
     "Supplication: ...\n\n"
     "Repeat for each day."),
    ("human", "{input}")
])

parser = StrOutputParser()
chain = prompt | llm | parser

def render_prayer():
    st.markdown("""
        <h2 style='color:#008080;'>🙏 Daily Prayer</h2>
        <p>Select a topic and number of days to receive a guided prayer journey using the ACTS format.</p>
    """, unsafe_allow_html=True)

    topics = [
        "Personal Growth",
        "Healing",
        "Family/Friends",
        "Forgiveness",
        "Finances",
        "Work/Career",
        "Something else..."
    ]

    selected_topic = st.selectbox("Select a prayer topic:", topics)
    num_days = st.number_input("How many days would you like the plan for?", min_value=1, max_value=7, value=5)

    if st.button("Generate My Prayer Plan ✨"):
        with st.spinner("Seeking God's presence and preparing your plan..."):
            input_text = f"Topic: {selected_topic}\nDuration: {num_days} Days"
            output = chain.invoke({"input": input_text})

            for section in output.split("\n\n"):
                if section.strip():
                    st.markdown(f"<div style='padding: 15px; background-color: #272740; border-radius: 10px; margin-bottom: 10px;'>"
                                f"<pre style='font-family:Segoe UI; font-size:15px;'>{section.strip()}</pre></div>", unsafe_allow_html=True)

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
