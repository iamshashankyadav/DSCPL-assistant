import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

# --- Load API key from .env file ---
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# --- LLM Configuration ---
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-70b-8192",
    max_tokens=300
)

# --- Prompt Template (no memory) ---

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are DSCPL, a spiritual companion and Christian guide. "
     "You respond with warmth, biblical wisdom, and emotional support. "
     "If the user asks a question or requests a plan or advice, prioritize answering clearly and directly first. "
     "Then, add encouragement or Scripture if helpful. "
     "Avoid vague replies like 'what’s on your heart today?' unless the user is silent. "
     "Keep responses under 150 words."),
    ("human", "{input}")
])

parser = StrOutputParser()

# --- Response Function ---
def chat_response(input_text):
    if not input_text.strip():
        return "I didn’t catch that. Could you rephrase it?"

    try:
        # Step 1: Format the prompt manually
        formatted_prompt = prompt.format_messages(input=input_text.strip())
        print(input_text.strip())
        # Step 2: Print formatted prompt for debugging
        print("\n--- FORMATTED PROMPT ---")
        for msg in formatted_prompt:
            print(f"{msg.type.upper()}: {msg.content}")
        print("--- END PROMPT ---\n")

        # Step 3: Call the LLM
        response = llm.invoke(formatted_prompt)
        return parser.invoke(response)

    except Exception as e:
        print("❌ Error during prompt processing or LLM call:", str(e))
        return "Sorry, I ran into an issue trying to understand your message. Please try again."

# --- UI ---
def render_just_chat():
    st.markdown("""
        <style>
            .chat-container {
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
                margin-bottom: 100px;
            }
            
            /* User message (right side, purple) */
            .user-msg {
                background-color: #9846e8;
                color: white;
                padding: 8px 12px;
                border-radius: 15px 15px 0 15px;
                align-self: flex-end;
                max-width: 75%;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                position: relative;
                margin-right: 5px;
            }
            
            /* AI message (left side, dark gray) */
            .ai-msg {
                background-color: #2d2d2d;
                color: white;
                padding: 8px 12px;
                border-radius: 15px 15px 15px 0;
                align-self: flex-start;
                max-width: 75%;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                position: relative;
                margin-left: 5px;
            }
            
            /* Optional: Add tiny message tails (like WhatsApp) */
            .user-msg::after {
                content: "";
                position: absolute;
                bottom: 0;
                right: -8px;
                width: 0;
                height: 0;
                border: 8px solid transparent;
                border-left-color: #9846e8;
                border-right: 0;
                border-bottom: 0;
                margin-bottom: 0px;
            }
            
            .ai-msg::after {
                content: "";
                position: absolute;
                bottom: 0;
                left: -8px;
                width: 0;
                height: 0;
                border: 8px solid transparent;
                border-right-color: #2d2d2d;
                border-left: 0;
                border-bottom: 0;
                margin-bottom: 0px;
            }
            
            /* Optional: Time stamp (WhatsApp-style) */
            .msg-time {
                font-size: 11px;
                color: #999;
                margin-top: 2px;
                text-align: right;
            }
        </style>
        
        <h2>💬 Just Chat</h2>
        <p>Talk freely with DSCPL. Be honest. Let’s grow together.</p>
    """, unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display past messages
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-msg'>🧍 {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ai-msg'>🙏 {msg['content']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Input box
    user_input = st.chat_input("What's on your heart?")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("DSCPL is replying..."):
            response = chat_response(user_input)

        st.session_state.chat_history.append({"role": "ai", "content": response})
        st.rerun()

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
