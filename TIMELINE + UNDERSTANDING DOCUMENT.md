# 📅 DSCPL – Timeline & Understanding Document

This file outlines the plan, reasoning, and implementation breakdown for DSCPL – a spiritual assistant Streamlit app built for the internship assignment.

---

## 🧠 Understanding the Problem

The assignment was to create a spiritual AI assistant (DSCPL) that can guide users through:

- Daily Devotions  
- Daily Prayer  
- Daily Meditation  
- Daily Accountability  
- Real-time Just Chat interface

The assistant must use AI (LLM) to dynamically generate personalized, multi-day plans rooted in scripture, prayer, and biblical wisdom.

---

## 🔨 Tech Stack Used

| Tool        | Purpose                                  |
|-------------|------------------------------------------|
| **Streamlit** | UI + user interaction layer            |
| **Groq API** | Ultra-fast inference with LLaMA 3 70B    |
| **LangChain**| Prompt management and model interfacing |
| **.env + dotenv** | Secure API key handling             |

---

## 📆 Timeline

| Day | Tasks Completed |
|-----|-----------------|
| Day 1 | Understood requirements, designed app layout |
| Day 2 | Implemented `app.py`, modularized into 5 core files |Created prompt logic using LangChain + Groq API |Completed `devotion.py`, `prayer.py` with correct outputs |
| Day 3 | Built `meditation.py` (with breathing animation) and `accountability.py` (with SOS logic) | Implemented memory-backed `just_chat.py` using conversation history |Polished UI, added styles, animations, prompt tuning |
| Day 4 | Recorded Loom video demo, wrote README + deployment-ready `requirements.txt` | Wrote this Timeline + Understanding document for submission |

---

## 🧩 Modular Structure

Each file handles one domain cleanly:

- `app.py` – Routing + homepage UI
- `devotion.py` – 7-day plan with scripture, prayer, declaration
- `prayer.py` – ACTS model prayer plan
- `meditation.py` – Bible verse + breathing + reflection
- `accountability.py` – Victory planning + daily truth + SOS
- `just_chat.py` – ChatGPT-style conversation interface with memory

---

## 🔁 Improvements Made

- Replaced outdated prompt format (`HumanMessage("{input}")`) with correct `("human", "{input}")`
- Reduced hallucination via tighter prompt formatting
- Added breathing animation with CSS pulse effect
- Implemented chat memory buffer to preserve context

---

## ✅ Result

DSCPL is now fully functional, deployable, and ready to support users in their daily spiritual walk using AI and biblical truth.

---

🙏 Built with prayer, care, and purpose.
