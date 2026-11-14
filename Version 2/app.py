
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pathlib import Path
from game_state import initialize_game
from action_validator import validate_action

load_dotenv()

st.set_page_config(
    page_title="Secret Laboratory Escape - Version 2",
    page_icon="🧪"
)
# Load custom laboratory styling
css_path = Path(__file__).resolve().parent.parent / "style.css"

if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True
    )

st.title("🧪 Secret Laboratory Escape - Version 2")
st.subheader("Escape Protocol — Version 2")

st.write("""
You wake up inside a secret underground research laboratory.

A dangerous experiment has triggered an emergency lockdown.
The laboratory's security system has sealed the exit.

Investigate the research terminal, unlock the equipment cabinet,
collect a security access card, and discover the emergency exit code.

In Version 2, Python validates your actions to prevent
invalid moves and puzzle bypasses.
""")

# Initialize game state
if "game_state" not in st.session_state:
    st.session_state.game_state = initialize_game()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Gemini
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is missing. Check your .env file.")
    st.stop()

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=30000)
)

# Sidebar: Inventory
st.sidebar.header("🎒 Inventory")

inventory = st.session_state.game_state["inventory"]

if inventory:
    for item in inventory:
        st.sidebar.write(f"✅ {item}")
else:
    st.sidebar.write("No items collected")

# Sidebar: Game progress
st.sidebar.header("🎯 Game Progress")

state = st.session_state.game_state

st.sidebar.write(
    "Research terminal examined:",
    state["terminal_examined"]
)

st.sidebar.write(
    "Equipment cabinet unlocked:",
    state["cabinet_unlocked"]
)

st.sidebar.write(
    "Security notice board examined:",
    state["notice_board_examined"]
)

st.sidebar.write(
    "Reactor control panel unlocked:",
    state["reactor_unlocked"]
)

st.sidebar.write(
    "Emergency exit unlocked:",
    state["door_unlocked"]
)

st.sidebar.write(
    "Escaped:",
    state["escaped"]
)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Player input
user_input = st.chat_input(
    "What would you like to investigate?",
    disabled=state["escaped"]
)

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Python validates the action first
    result = validate_action(
        user_input,
        st.session_state.game_state
    )

    # Gemini narrates the validated result
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"""
            You are the narrator of a science-fiction
            escape room called Secret Laboratory Escape.

            SETTING:
            A secret underground research laboratory
            is under emergency lockdown.

            Describe the following Python-validated result
            in a short, immersive way.

            RULES:
            - Do not change the validated result.
            - Do not invent additional items or puzzle codes.
            - Do not claim that other actions succeeded.
            - Do not reveal secrets before they are discovered.
            - Keep your response clear and reasonably short.

            VALIDATED RESULT:
            {result}
            """
        )

        answer = response.text or result

    except Exception:
        # Use the validated result if Gemini is unavailable
        answer = result

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()

# Successful escape
if state["escaped"]:
    st.success(
        "🎉 Congratulations! You successfully escaped "
        "the secret laboratory!"
    )
    st.balloons()

# Restart game
if st.button("🔄 Restart Game"):
    st.session_state.game_state = initialize_game()
    st.session_state.messages = []
    st.rerun()
