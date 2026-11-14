
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(
    page_title="Secret Laboratory Escape",
    page_icon="🧪"
)

st.title("🧪 Secret Laboratory Escape")
st.subheader("An AI-Powered Escape Room Adventure")

st.write("""
You wake up inside a secret underground research laboratory.

A dangerous experiment has triggered an emergency lockdown.
The laboratory's security system has sealed the exit door.

Explore the laboratory, investigate mysterious equipment,
solve security puzzles, and collect essential items to escape!

⚠️ Can you unlock the emergency exit before the facility shuts down?
""")

# Initialize Gemini
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is missing. Check your .env file.")
    st.stop()

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=30000)
)

# Game Master instructions
GAME_PROMPT = """
You are the Game Master of an interactive science-fiction
escape room called "Secret Laboratory Escape".

SETTING:
The player wakes up inside a secret underground research
laboratory after an experiment triggers an emergency lockdown.

The laboratory contains advanced scientific equipment,
security terminals, warning lights, and a sealed emergency exit.

OBJECTS:
1. Research terminal
2. Laboratory workstation
3. Security notice board
4. Locked equipment cabinet
5. Reactor control panel
6. Emergency exit door

PUZZLES:
1. Research terminal:
   The player discovers four security digits in the order
   3, 1, 4, 2. Together, they form the code 3142.

2. Locked equipment cabinet:
   The cabinet opens only with code 3142.
   Inside is a security access card.
   The player must collect the card.

3. Security notice board:
   A hidden message reads:
   "The reactor control panel holds the final access code."

4. Reactor control panel:
   The player must use the security access card
   to access a protected compartment.
   The compartment reveals the emergency exit code 7285.

5. Emergency exit door:
   The exit unlocks only when the player uses
   the final code 7285 after discovering it.

RULES:
- Describe the laboratory and respond to player actions.
- Do not reveal puzzle solutions before players discover them.
- Allow players to examine objects and collect items.
- Remember previous actions from the conversation.
- Provide helpful hints when players are stuck.
- The player wins only after unlocking the emergency exit.
- Keep responses immersive, clear, and reasonably short.
- Do not introduce additional puzzle codes.
- Do not allow players to bypass the intended puzzle sequence.

IMPORTANT:
This is Version 1 of the project.
You manage the story, inventory, and game progression
through the conversation.
There is no separate Python-based action validator.
"""

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Player input
user_input = st.chat_input("What would you like to investigate?")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Laboratory AI is responding..."):
            try:
                history = "\n".join(
                    f"{msg['role']}: {msg['content']}"
                    for msg in st.session_state.messages
                )

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=GAME_PROMPT + "\n\n" + history
                )

                answer = response.text or "Please try again."
                st.write(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Gemini request failed: {e}")

# Restart game
if st.button("🔄 Restart Game"):
    st.session_state.messages = []
    st.rerun()
