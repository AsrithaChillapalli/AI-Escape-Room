
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

from game_state import initialize_game
from action_validator import validate_action

load_dotenv()

st.set_page_config(
    page_title="AI Escape Room - Version 2",
    page_icon="🔐"
)

st.title("🔐 AI Escape Room - Version 2")
st.subheader("The Reliable Locked Library")

st.write("""
Explore the library, solve puzzles, collect items,
and unlock the exit.

In Version 2, Python validates your actions.
""")

if "game_state" not in st.session_state:
    st.session_state.game_state = initialize_game()

if "messages" not in st.session_state:
    st.session_state.messages = []

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=30000)
)

st.sidebar.header("🎒 Inventory")
st.sidebar.write(
    st.session_state.game_state["inventory"]
    or "No items collected"
)

st.sidebar.header("🎯 Game Progress")
st.sidebar.write(
    "Drawer unlocked:",
    st.session_state.game_state["drawer_unlocked"]
)
st.sidebar.write(
    "Clock unlocked:",
    st.session_state.game_state["clock_unlocked"]
)
st.sidebar.write(
    "Escaped:",
    st.session_state.game_state["escaped"]
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input(
    "What would you like to do?",
    disabled=st.session_state.game_state["escaped"]
)

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    result = validate_action(
        user_input,
        st.session_state.game_state
    )

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=f"""
                You are an escape-room narrator.

                Describe the following validated result
                in a short, immersive way.

                You must not change the result,
                invent new items, reveal additional codes,
                or claim that other actions succeeded.

                Validated result:
                {result}
                """
            )

            answer = response.text or result

        except Exception:
            answer = result

        st.write(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    st.rerun()

if st.session_state.game_state["escaped"]:
    st.success("🎉 Congratulations! You escaped the library!")
    st.balloons()

if st.button("🔄 Restart Game"):
    st.session_state.game_state = initialize_game()
    st.session_state.messages = []
    st.rerun()
