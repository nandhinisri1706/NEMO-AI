
import streamlit as st
import ollama
import json
import os
import uuid
from datetime import datetime

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="NEMO AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

APP_NAME = "NEMO AI"
MODEL = "gemma3:1b"
HISTORY_FILE = "chat_history.json"
SETTINGS_FILE = "nemo_settings.json"

SYSTEM_PROMPT = """
You are NEMO AI, an intelligent, friendly and capable personal AI assistant.

IDENTITY:
- Your name is NEMO AI.
- Never introduce yourself as Gemma, Google Gemma or Ollama.
- If asked your name, reply: I am NEMO AI.
- The underlying AI model is only technical infrastructure.
- Never claim to be created by another company.

BEHAVIOUR:
- Be helpful, intelligent, friendly and professional.
- Give accurate and useful answers.
- Explain difficult concepts in simple language.
- Help with programming, AI, projects, studies, writing and creativity.
- Provide step-by-step guidance when needed.
- Use clear headings and code blocks where useful.
- Never invent facts.
"""

# =====================================================
# SESSION STATE
# =====================================================

if "chats" not in st.session_state:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                st.session_state.chats = json.load(f)
        except (json.JSONDecodeError, OSError):
            st.session_state.chats = {}
    else:
        st.session_state.chats = {}

if "active_chat" not in st.session_state:
    st.session_state.active_chat = None

if "theme" not in st.session_state:
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
            st.session_state.theme = settings.get("theme", "dark")
    except (OSError, json.JSONDecodeError):
        st.session_state.theme = "dark"

if "composer" not in st.session_state:
    st.session_state.composer = ""

if "clear_composer" not in st.session_state:
    st.session_state.clear_composer = False

# Clear input before rendering its widget
if st.session_state.clear_composer:
    st.session_state.composer = ""
    st.session_state.clear_composer = False


# =====================================================
# THEME COLORS
# =====================================================

DARK = st.session_state.theme == "dark"

if DARK:
    C = {
        "bg": "#090812",
        "sidebar": "#100e1c",
        "surface": "#171425",
        "surface2": "#211b34",
        "text": "#f5f2ff",
        "muted": "#9991ad",
        "border": "#302844",
        "accent": "#a78bfa",
        "accent2": "#7655e8",
        "input": "#171425",
        "user": "#29203f",
        "shadow": "rgba(0,0,0,0.25)"
    }
else:
    C = {
        "bg": "#f5f3fc",
        "sidebar": "#ffffff",
        "surface": "#ffffff",
        "surface2": "#f0ebff",
        "text": "#211b35",
        "muted": "#77718c",
        "border": "#e5def5",
        "accent": "#7655d9",
        "accent2": "#9775ed",
        "input": "#ffffff",
        "user": "#eee8ff",
        "shadow": "rgba(65,40,120,0.08)"
    }


# =====================================================
# SAVE FUNCTIONS
# =====================================================

def save_chats():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            st.session_state.chats,
            f,
            indent=4,
            ensure_ascii=False
        )


def save_settings():
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {"theme": st.session_state.theme},
            f,
            indent=4
        )


def create_chat():
    chat_id = str(uuid.uuid4())

    st.session_state.chats[chat_id] = {
        "title": "New Conversation",
        "messages": [],
        "updated_at": datetime.now().isoformat()
    }

    st.session_state.active_chat = chat_id
    st.session_state.composer = ""

    save_chats()


def delete_chat(chat_id):
    if chat_id in st.session_state.chats:
        del st.session_state.chats[chat_id]

    if st.session_state.active_chat == chat_id:
        st.session_state.active_chat = None

    save_chats()


# =====================================================
# INITIAL CHAT
# =====================================================

if not st.session_state.chats:
    create_chat()

if (
    not st.session_state.active_chat
    or st.session_state.active_chat not in st.session_state.chats
):
    st.session_state.active_chat = next(
        iter(st.session_state.chats)
    )

chat_id = st.session_state.active_chat
current_chat = st.session_state.chats[chat_id]
messages = current_chat["messages"]


# =====================================================
# PREMIUM CSS
# =====================================================

st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {{
    --bg: {C["bg"]};
    --sidebar: {C["sidebar"]};
    --surface: {C["surface"]};
    --surface2: {C["surface2"]};
    --text: {C["text"]};
    --muted: {C["muted"]};
    --border: {C["border"]};
    --accent: {C["accent"]};
    --accent2: {C["accent2"]};
    --input: {C["input"]};
    --user: {C["user"]};
}}

.stApp {{
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}}

header[data-testid="stHeader"] {{
    background: transparent;
}}

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

.block-container {{
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}}

[data-testid="stSidebar"] {{
    background: var(--sidebar);
    border-right: 1px solid var(--border);
}}

[data-testid="stSidebar"] > div:first-child {{
    padding-top: 1.5rem;
}}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{
    color: var(--text);
}}

h1, h2, h3 {{
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif;
}}

p, label, span {{
    font-family: 'DM Sans', sans-serif;
}}

.brand {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: var(--text);
}}

.brand span {{
    color: var(--accent);
}}

.brand-sub {{
    color: var(--muted);
    font-size: 12px;
    margin-top: 3px;
}}

.eyebrow {{
    color: var(--accent);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
}}

.hero-title {{
    font-family: 'Space Grotesk', sans-serif;
    color: var(--text);
    font-size: clamp(30px, 4vw, 48px);
    line-height: 1.15;
    font-weight: 700;
    letter-spacing: -2px;
    margin-top: 10px;
}}

.hero-sub {{
    color: var(--muted);
    font-size: 15px;
    margin-top: 10px;
}}

.stButton > button {{
    border-radius: 12px;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    min-height: 42px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    transition: all 0.2s ease;
}}

.stButton > button:hover {{
    border-color: var(--accent);
    color: var(--accent);
    transform: translateY(-1px);
}}

.stButton > button[kind="primary"] {{
    background: linear-gradient(110deg, #7955e8, #a47cfb);
    color: white;
    border: none;
}}

.stButton > button[kind="primary"]:hover {{
    background: linear-gradient(110deg, #8b6af0, #b091ff);
    color: white;
}}

[data-testid="stVerticalBlockBorderWrapper"] {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px;
    transition: all 0.2s ease;
}}

[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    border-color: var(--accent);
    box-shadow: 0 8px 30px var(--shadow);
}}

[data-testid="stChatMessage"] {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 17px;
    margin-bottom: 16px;
}}

[data-testid="stChatMessage"] p {{
    color: var(--text);
}}

[data-testid="stTextInput"] input {{
    background: var(--input);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 14px;
    min-height: 48px;
}}

[data-testid="stTextInput"] input:focus {{
    border-color: var(--accent);
    box-shadow: 0 0 0 1px var(--accent);
}}

[data-testid="stMarkdownContainer"] p {{
    color: var(--text);
}}

[data-testid="stCaptionContainer"] p {{
    color: var(--muted);
}}

hr {{
    border-color: var(--border);
}}

div[data-testid="stStatusWidget"] {{
    visibility: hidden;
}}

[data-testid="stSidebar"] [data-testid="stButton"] button {{
    text-align: left;
}}

.footer {{
    color: var(--muted);
    text-align: center;
    font-size: 11px;
    padding: 15px;
}}

.stApp {{
    transition: background 0.2s ease;
}}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">NEMO<span> AI</span></div>'
        '<div class="brand-sub">Your intelligent AI companion</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    if st.button(
        "＋   New Chat",
        type="primary",
        use_container_width=True
    ):
        create_chat()
        st.rerun()

    st.write("")

    st.markdown(
        '<div class="eyebrow">YOUR WORKSPACE</div>',
        unsafe_allow_html=True
    )

    st.write("")

    sorted_chats = sorted(
        st.session_state.chats.items(),
        key=lambda x: x[1].get("updated_at", ""),
        reverse=True
    )

    for old_id, chat in sorted_chats:

        col1, col2 = st.columns([0.82, 0.18])

        title = chat.get("title", "New Conversation")

        if len(title) > 23:
            title = title[:23] + "..."

        with col1:

            label = (
                "● " + title
                if old_id == chat_id
                else "   " + title
            )

            if st.button(
                label,
                key=f"history_{old_id}",
                use_container_width=True
            ):
                st.session_state.active_chat = old_id
                st.session_state.composer = ""
                st.rerun()

        with col2:

            if st.button(
                "×",
                key=f"delete_{old_id}"
            ):
                delete_chat(old_id)
                st.rerun()

    st.divider()

    st.markdown(
        '<div class="eyebrow">AI STATUS</div>',
        unsafe_allow_html=True
    )

    st.success("NEMO is ready")

    st.caption("Local model")
    st.write("`" + MODEL + "`")

    st.divider()

    st.caption("NEMO AI · Personal AI Workspace")


# =====================================================
# TOP HEADER + THEME TOGGLE
# =====================================================

top_left, top_right = st.columns([0.88, 0.12])

with top_left:

    st.markdown(
        '<div class="brand">NEMO AI</div>'
        '<div class="brand-sub">Think smarter. Create more. Explore everything.</div>',
        unsafe_allow_html=True
    )

with top_right:

    theme_icon = "☀️" if DARK else "🌙"

    if st.button(
        theme_icon,
        key="theme_toggle",
        help="Switch Dark / Light theme",
        use_container_width=True
    ):

        st.session_state.theme = (
            "light" if DARK else "dark"
        )

        save_settings()
        st.rerun()

st.write("")


# =====================================================
# WELCOME SCREEN
# =====================================================

if not messages:

    st.write("")

    st.markdown(
        '<div class="eyebrow">YOUR PERSONAL AI ASSISTANT</div>'
        '<div class="hero-title">What are we creating<br>today?</div>'
        '<div class="hero-sub">Your next big idea starts with one conversation.</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.markdown("### 💡")
            st.markdown("**Start a project**")

            st.caption(
                "Transform your idea into a real project."
            )

            if st.button(
                "Explore project ideas  →",
                key="idea",
                use_container_width=True
            ):

                st.session_state.composer = (
                    "I want to start a project. "
                    "Help me plan it step by step."
                )

                st.rerun()

    with col2:

        with st.container(border=True):

            st.markdown("### 💻")
            st.markdown("**Build with code**")

            st.caption(
                "Write, debug and understand programming."
            )

            if st.button(
                "Start coding  →",
                key="code",
                use_container_width=True
            ):

                st.session_state.composer = (
                    "I want to build a coding project. "
                    "Help me choose the technology and start."
                )

                st.rerun()

    col3, col4 = st.columns(2)

    with col3:

        with st.container(border=True):

            st.markdown("### 📚")
            st.markdown("**Learn something new**")

            st.caption(
                "Explore concepts with simple explanations."
            )

            if st.button(
                "Start learning  →",
                key="learn",
                use_container_width=True
            ):

                st.session_state.composer = (
                    "I want to learn a new topic. "
                    "Teach me step by step."
                )

                st.rerun()

    with col4:

        with st.container(border=True):

            st.markdown("### ✍️")
            st.markdown("**Create content**")

            st.caption(
                "Write, brainstorm and improve your ideas."
            )

            if st.button(
                "Create content  →",
                key="content",
                use_container_width=True
            ):

                st.session_state.composer = (
                    "Help me create professional and engaging content."
                )

                st.rerun()

    st.write("")
    st.write("")


# =====================================================
# CONVERSATION DISPLAY
# =====================================================

else:

    for message in messages:

        if message["role"] not in ("user", "assistant"):
            continue

        avatar = "👤" if message["role"] == "user" else "🤖"

        with st.chat_message(
            message["role"],
            avatar=avatar
        ):
            st.markdown(message["content"])


# =====================================================
# MESSAGE COMPOSER
# =====================================================

st.write("")

with st.form(
    key=f"composer_form_{chat_id}",
    clear_on_submit=False
):

    st.text_input(
        "Message",
        placeholder="Message NEMO AI... Ask anything or share your idea.",
        label_visibility="collapsed",
        key="composer"
    )

    send_col, hint_col = st.columns([0.22, 0.78])

    with send_col:

        submitted = st.form_submit_button(
            "➤  Send",
            type="primary",
            use_container_width=True
        )

    with hint_col:

        st.caption("Enter your message and let NEMO help you.")


# =====================================================
# AI RESPONSE
# =====================================================

if submitted:

    prompt = st.session_state.composer.strip()

    if prompt:

        messages.append({
            "role": "user",
            "content": prompt
        })

        if current_chat["title"] == "New Chat" or current_chat["title"] == "New Conversation":
            current_chat["title"] = prompt[:30]

        current_chat["updated_at"] = datetime.now().isoformat()

        save_chats()

        st.session_state.clear_composer = True

        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🤖"):

            response_box = st.empty()
            full_response = ""

            try:

                ollama_messages = [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    }
                ] + messages

                stream = ollama.chat(
                    model=MODEL,
                    messages=ollama_messages,
                    stream=True
                )

                for chunk in stream:

                    full_response += chunk["message"]["content"]

                    response_box.markdown(
                        full_response + " ▌"
                    )

                response_box.markdown(full_response)

                messages.append({
                    "role": "assistant",
                    "content": full_response
                })

                current_chat["updated_at"] = datetime.now().isoformat()

                save_chats()

            except Exception as error:

                st.error(f"NEMO AI error: {error}")

                messages.pop()
                save_chats()

        st.rerun()


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
    '<div class="footer">'
    'NEMO AI · Your Personal AI Workspace · Powered by Local AI'
    '</div>',
    unsafe_allow_html=True
)
