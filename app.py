import streamlit as st
from devotion import render_devotion
from prayer import render_prayer
from meditation import render_meditation
from accountability import render_accountability
from just_chat import render_just_chat

# --- Page Setup ---
st.set_page_config(page_title="DSCPL – Your Spiritual Companion", layout="centered")

# --- Navigation Logic ---
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page_name):
    st.session_state.page = page_name

# --- Homepage ---
if st.session_state.page == "home":
    st.title("🧭 DSCPL")
    st.subheader("Your Daily Spiritual Companion")

    st.markdown("### What do you need today?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📖 Daily Devotion"):
            go_to("devotion")
        if st.button("🧘 Daily Meditation"):
            go_to("meditation")
        if st.button("🛡️ Daily Accountability"):
            go_to("accountability")

    with col2:
        if st.button("🙏 Daily Prayer"):
            go_to("prayer")
        if st.button("💬 Just Chat"):
            go_to("just_chat")

# --- Routing to Feature Pages ---
elif st.session_state.page == "devotion":
    render_devotion()

elif st.session_state.page == "prayer":
    render_prayer()

elif st.session_state.page == "meditation":
    render_meditation()
    

elif st.session_state.page == "accountability":
    render_accountability()

elif st.session_state.page == "just_chat":
    render_just_chat()
