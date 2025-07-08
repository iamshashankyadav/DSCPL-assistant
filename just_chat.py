import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os
from dotenv import load_dotenv

# --- Load API key from .env file ---
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# --- LLM Configuration ---
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-70b-8192",
    max_tokens=300  # Limit response length
)

# --- Prompt Setup ---
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are DSCPL, a spiritual companion who responds with warmth, biblical wisdom, and emotional support. Keep your responses under 150 words."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessage(content="{input}")
])

parser = StrOutputParser()

def chat_response_with_memory(input_text, history_messages):
    chain = chat_prompt | llm | parser
    return chain.invoke({
        "input": input_text,
        "history": history_messages
    })

# --- Main Just Chat UI ---
def render_just_chat():
    st.markdown("""
        <style>
            .chat-container {
                display: flex;
                flex-direction: column;
                gap: 1rem;
                margin-bottom: 100px;
            }
            .user-msg {
                background-color: #e6ccff;
                padding: 10px 15px;
                border-radius: 15px;
                align-self: flex-end;
                max-width: 75%;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
            }
            .ai-msg {
                background-color: #f2f2f2;
                padding: 10px 15px;
                border-radius: 15px;
                align-self: flex-start;
                max-width: 75%;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
            }
        </style>
        <h2>💬 Just Chat</h2>
        <p>Talk freely with DSCPL. Be honest. Let’s grow together.</p>
    """, unsafe_allow_html=True)

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display message history
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            st.markdown(f"<div class='user-msg'>🧍 {content}</div>", unsafe_allow_html=True)
        elif role == "ai":
            st.markdown(f"<div class='ai-msg'>🙏 {content}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Bottom input bar
    user_input = st.chat_input("What's on your heart?")

    if user_input:
        # Use last 2 turns (2 user + 2 ai) for memory
        memory_window = st.session_state.chat_history[-4:]
        formatted_memory = []

        for m in memory_window:
            if m["role"] == "user":
                formatted_memory.append(HumanMessage(content=m["content"]))
            elif m["role"] == "ai":
                formatted_memory.append(AIMessage(content=m["content"]))

        with st.spinner("DSCPL is replying..."):
            response = chat_response_with_memory(user_input, formatted_memory)

        # Store to full chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "ai", "content": response})

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
