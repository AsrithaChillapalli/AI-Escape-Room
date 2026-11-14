
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(
    page_title="AI Escape Room",
    page_icon="🔐"
)

st.title("🔐 AI Escape Room")
st.subheader("The Mystery of the Locked Library")

st.write("""
You wake up inside a mysterious library.
The door is locked with a four-digit code.

Explore the room, discover clues, solve puzzles,
and find the code to escape!
""")

# Initialize Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=30000)
)

# Game Master instructions
GAME_PROMPT = """
You are the Game Master of an interactive escape room.

SETTING:
The player is trapped inside an old library.

OBJECTS:
1. Bookshelf
2. Wooden desk
3. Painting
4. Locked drawer
5. Antique clock
6. Exit door

PUZZLES:
1. Bookshelf: Four special books reveal the code 3142.
2. Locked drawer: Opens with code 3142 and contains a brass key.
3. Painting: Behind it is a note saying
   "The clock holds the final secret."
4. Antique clock: Using the brass key opens a compartment
   containing the final exit code 7285.
5. Exit door: Opens using code 7285.

RULES:
- Describe the library and respond to player actions.
- Do not reveal puzzle solutions before players discover them.
- Allow players to examine objects and collect items.
- Remember previous actions from the conversation.
- Guide players with hints when needed.
- The player wins only after unlocking the exit door.
- Keep responses immersive, clear, and reasonably short.
"""

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Player input
user_input = st.chat_input("What would you like to do?")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Game Master is thinking..."):
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
