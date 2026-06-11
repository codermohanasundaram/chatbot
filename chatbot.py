import anthropic
import streamlit as st

st.set_page_config(
    page_title="Mohan Bot",
    page_icon="@@",
    layout="centered"
)


# ── Sidebar — Customize Your Bot ────────────────────────
st.sidebar.title("⚙️ Customize Your Bot")

bot_name = st.sidebar.text_input(
    "Bot Name", 
    value="Buddy"
)


bot_role = st.sidebar.selectbox(
    "Bot Personality",
    [
        "Friendly Personal Assistant",
        "Python Tutor",
        "Fitness Coach",
        "Interview Coach",
        "Tamil Language Tutor",
        "Custom (type below)"
    ]
)


custom_role = st.sidebar.text_area(
    "Custom Personality (optional)",
    placeholder="e.g. You are a cooking expert who loves South Indian food..."
)

temperature = st.sidebar.slider(
    "Creativity Level",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
    help="0 = factual & precise  |  1 = creative & random"
)


# Clear chat button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# ── Build System Prompt ──────────────────────────────────
role_prompts = {
    "Friendly Personal Assistant":
        f"You are {bot_name}, a friendly helpful assistant. Keep answers short and simple.",
    "Python Tutor":
        f"You are {bot_name}, a Python tutor for beginners. Always give code examples.",
    "Fitness Coach":
        f"You are {bot_name}, a fitness coach. Give simple workout and diet advice.",
    "Interview Coach":
        f"You are {bot_name}, a tech interview coach. Ask one question at a time.",
    "Tamil Language Tutor":
        f"You are {bot_name}, a Tamil tutor. Teach Tamil words with English meaning.",
    "Custom (type below)":
        custom_role if custom_role else f"You are {bot_name}, a helpful assistant.",
}

system_prompt = role_prompts[bot_role]

# ── Main Chat Area ───────────────────────────────────────
st.title(f"🤖 {bot_name}")
st.caption(f"Personality: {bot_role}")
st.divider()

# ── Initialize Chat History ──────────────────────────────
# st.session_state keeps data alive across reruns
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Display All Previous Messages ────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ── Chat Input Box ───────────────────────────────────────
user_input = st.chat_input(f"Message {bot_name}...")

if user_input:

    # Show user message on screen
    with st.chat_message("user"):
        st.markdown(user_input)

    # Add to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # ── Call Claude API ──────────────────────────────────
    client = anthropic.Anthropic(
        api_key=st.secrets["ANTHROPIC_API_KEY"]
    )

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=1024,
                system=system_prompt,
                messages=st.session_state.messages
            )
            ai_reply = response.content[0].text
            st.markdown(ai_reply)

    # Add AI reply to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

