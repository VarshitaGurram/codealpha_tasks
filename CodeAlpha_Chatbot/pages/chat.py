import streamlit as st
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from deep_translator import GoogleTranslator
from gtts import gTTS
import numpy as np
import re as _re
import base64, io, datetime

st.set_page_config(page_title="TechBot | AI FAQ Chatbot", page_icon="🤖", layout="centered",
                   initial_sidebar_state="collapsed")

# ── Auth guard ────────────────────────────────────────────────────────────────
for k,v in [("logged_in",False),("username",""),("plan","Pro"),("guest",False)]:
    if k not in st.session_state: st.session_state[k] = v
if not st.session_state.logged_in and not st.session_state.guest:
    st.switch_page("pages/login.py")

PLAN        = st.session_state.get("plan","Pro")
USERNAME    = st.session_state.get("username","User")
GUEST       = st.session_state.get("guest", False)
PLAN_LIMITS = {
    "Guest":  {"q_limit":5,  "lang":False,"export":False,"fav_limit":0, "tts":False,"theme":False},
    "Basic":  {"q_limit":20, "lang":False,"export":False,"fav_limit":5, "tts":False,"theme":False},
    "Pro":    {"q_limit":999,"lang":True, "export":True, "fav_limit":999,"tts":True, "theme":True},
    "Ultra":  {"q_limit":999,"lang":True, "export":True, "fav_limit":999,"tts":True, "theme":True},
}
LIMITS = PLAN_LIMITS.get(PLAN, PLAN_LIMITS["Pro"])

# ── FAQ Data ──────────────────────────────────────────────────────────────────
FAQS = [
    ("What is artificial intelligence?",
     "Artificial Intelligence (AI) is the simulation of human intelligence in machines that think, learn, and problem-solve like humans. It includes machine learning, deep learning, NLP, and robotics.", "🧠 AI"),
    ("What is machine learning?",
     "Machine Learning (ML) is a subset of AI where systems learn from data to improve without being explicitly programmed. It includes supervised, unsupervised, and reinforcement learning.", "🧠 AI"),
    ("What is deep learning?",
     "Deep Learning uses neural networks with many layers to automatically learn from data. It powers image recognition, speech recognition, and more.", "🧠 AI"),
    ("What is a neural network?",
     "A neural network is a computing system inspired by the human brain, made of interconnected nodes (neurons). It learns patterns from data and is the foundation of deep learning.", "🧠 AI"),
    ("What is natural language processing?",
     "NLP is a branch of AI that enables computers to understand, interpret, and generate human language. Examples include chatbots, translation tools, and sentiment analysis.", "🧠 AI"),
    ("What is computer vision?",
     "Computer Vision trains machines to interpret visual data from images and videos — like object detection, facial recognition, and medical imaging.", "🧠 AI"),
    ("What is reinforcement learning?",
     "Reinforcement Learning is a type of ML where an agent learns by interacting with an environment, receiving rewards or penalties. Used in game AI, robotics, and autonomous driving.", "🧠 AI"),
    ("What is generative AI?",
     "Generative AI creates new content — text, images, audio, or video — based on patterns learned from training data. Examples include ChatGPT, DALL·E, and Stable Diffusion.", "🧠 AI"),
    ("What is a large language model?",
     "A Large Language Model (LLM) is AI trained on massive text data to understand and generate language. Examples include GPT-4, Claude, Gemini, and LLaMA.", "🧠 AI"),
    ("What is ChatGPT?",
     "ChatGPT is an AI chatbot by OpenAI based on the GPT architecture. It can answer questions, write code, summarize text, and hold conversations.", "🧠 AI"),
    ("What is Claude AI?",
     "Claude is an AI assistant by Anthropic, designed to be helpful, harmless, and honest. It can write, analyze, code, and have nuanced conversations.", "🧠 AI"),
    ("What is prompt engineering?",
     "Prompt engineering is designing and refining input prompts to get the best possible responses from AI language models like ChatGPT or Claude.", "🧠 AI"),
    ("What is the difference between AI and automation?",
     "Automation follows fixed rules for repetitive tasks. AI can learn from data, adapt to new situations, and make decisions — going beyond fixed rules.", "🧠 AI"),
    ("What is a chatbot?",
     "A chatbot is software that simulates conversation with humans using rule-based or AI/NLP approaches to understand and reply to queries.", "🧠 AI"),
    ("What is Python?",
     "Python is a high-level programming language known for simple syntax and readability. It's widely used in AI, data science, web development, and automation.", "🐍 Python"),
    ("What is a library in programming?",
     "A library is pre-written code that developers use to perform common tasks. Python examples include NumPy, Pandas, and TensorFlow.", "🐍 Python"),
    ("What is TensorFlow?",
     "TensorFlow is an open-source deep learning framework by Google, used to build and train machine learning models.", "🐍 Python"),
    ("What is PyTorch?",
     "PyTorch is an open-source deep learning framework by Meta. It's popular in research due to its dynamic computation graph and intuitive design.", "🐍 Python"),
    ("What is Scikit-learn?",
     "Scikit-learn is a Python library for machine learning providing tools for classification, regression, clustering, and model evaluation.", "🐍 Python"),
    ("What is Pandas?",
     "Pandas is a Python library for data manipulation. It provides DataFrames that make it easy to clean, transform, and analyze structured data.", "🐍 Python"),
    ("What is NumPy?",
     "NumPy is a Python library for numerical computing. It provides arrays, matrices, and math functions — the foundation for many data science libraries.", "🐍 Python"),
    ("What is Streamlit?",
     "Streamlit is an open-source Python framework for building interactive web apps for data science and ML — without front-end web development skills.", "🐍 Python"),
    ("What is data science?",
     "Data Science uses statistics, programming, and domain expertise to extract insights from structured and unstructured data.", "📊 Data"),
    ("What is overfitting?",
     "Overfitting happens when a model learns training data too well, including noise, causing poor performance on new unseen data.", "📊 Data"),
    ("What is underfitting?",
     "Underfitting occurs when a model is too simple to capture data patterns, resulting in poor performance on both training and test data.", "📊 Data"),
    ("What is a dataset?",
     "A dataset is a collection of data used to train, validate, or test a machine learning model. It typically has features (inputs) and labels (outputs).", "📊 Data"),
    ("What is training a model?",
     "Training a model means feeding it data so it can learn patterns and adjust its parameters (weights) to minimize errors and make accurate predictions.", "📊 Data"),
    ("What is a GPU and why is it used in AI?",
     "A GPU handles many operations in parallel. In AI, GPUs dramatically accelerate training of deep learning models compared to CPUs.", "📊 Data"),
    ("What is cloud computing?",
     "Cloud computing delivers computing services — servers, storage, databases, networking — over the internet. Major providers include AWS, Google Cloud, and Microsoft Azure.", "☁️ Cloud"),
    ("What is the Internet of Things?",
     "IoT refers to physical devices — smart gadgets, wearables, sensors — connected to the internet to collect and exchange data.", "☁️ Cloud"),
    ("What is blockchain?",
     "Blockchain is a distributed digital ledger recording transactions across multiple computers. It's the technology behind Bitcoin and Ethereum.", "☁️ Cloud"),
    ("What is cybersecurity?",
     "Cybersecurity protects systems, networks, and programs from digital attacks, unauthorized access, data theft, and damage.", "☁️ Cloud"),
    ("What is an API?",
     "An API (Application Programming Interface) allows different software to communicate. For example, a weather app uses an API to fetch weather data.", "☁️ Cloud"),
    ("What is open source software?",
     "Open source software has freely available source code that anyone can view, use, modify, and distribute. Examples: Linux, Python, TensorFlow.", "☁️ Cloud"),
]

QUESTIONS = [f[0] for f in FAQS]
ANSWERS   = [f[1] for f in FAQS]
TAGS      = [f[2] for f in FAQS]

# ── Related questions map ─────────────────────────────────────────────────────
RELATED = {
    "🧠 AI":     ["What is machine learning?", "What is deep learning?", "What is ChatGPT?",
                  "What is generative AI?", "What is a neural network?"],
    "🐍 Python": ["What is Python?", "What is TensorFlow?", "What is Pandas?",
                  "What is NumPy?", "What is Scikit-learn?"],
    "📊 Data":   ["What is data science?", "What is overfitting?", "What is a dataset?",
                  "What is training a model?", "What is a GPU and why is it used in AI?"],
    "☁️ Cloud":  ["What is cloud computing?", "What is an API?", "What is cybersecurity?",
                  "What is blockchain?", "What is open source software?"],
}

def get_followups(tag, current_q, n=3):
    pool = RELATED.get(tag, QUESTIONS)
    return [q for q in pool if q.lower() != current_q.lower()][:n]

# ── NLP ───────────────────────────────────────────────────────────────────────
@st.cache_resource
def build_vectorizer():
    v = TfidfVectorizer(ngram_range=(1,2), stop_words="english")
    v.fit(QUESTIONS + ANSWERS)
    return v, v.transform(QUESTIONS), v.transform(ANSWERS)

vectorizer, faq_q_vecs, faq_a_vecs = build_vectorizer()

# Expand common short/slang queries to full phrases for better matching
EXPANSIONS = {
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "llm": "large language model",
    "nn": "neural network",
    "cv": "computer vision",
    "rl": "reinforcement learning",
    "api": "application programming interface",
    "iot": "internet of things",
    "gpu": "graphics processing unit",
    "genai": "generative ai",
}

def expand_query(text):
    words = text.lower().split()
    expanded = []
    for w in words:
        expanded.append(EXPANSIONS.get(w, w))
    return " ".join(expanded)

def get_answer(user_input, threshold=0.07):
    cleaned  = _re.sub(r'[^\w\s]', '', user_input.lower()).strip()
    expanded = expand_query(cleaned)
    # use expanded query for matching
    uv      = vectorizer.transform([expanded])
    merged  = np.maximum(
        cosine_similarity(uv, faq_q_vecs).flatten(),
        cosine_similarity(uv, faq_a_vecs).flatten() * 0.6
    )
    idx   = int(np.argmax(merged))
    score = float(merged[idx])
    if score < threshold:
        return None, score, None
    return ANSWERS[idx], score, TAGS[idx]

# ── Language map ──────────────────────────────────────────────────────────────
REPLY_LANGUAGES = {
    "English":"en", "Hindi":"hi", "Tamil":"ta", "Telugu":"te",
    "French":"fr",  "Spanish":"es","German":"de","Japanese":"ja",
    "Arabic":"ar",  "Korean":"ko", "Chinese":"zh-CN",
}

SUGGESTIONS = [
    "What is AI?",        "What is machine learning?",
    "What is Python?",    "What is ChatGPT?",
    "What is an API?",    "What is deep learning?",
    "What is cloud?",     "What is prompt engineering?",
]

# ── Export helper ─────────────────────────────────────────────────────────────
def export_chat_txt():
    lines = [f"TechBot Chat Export — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n{'='*50}\n"]
    for m in st.session_state.messages:
        role = "You" if m["role"] == "user" else "TechBot"
        clean_text = _re.sub(r'\*\*(.*?)\*\*', r'\1', m['text'])
        lines.append(f"{role}:\n{clean_text}\n")
    return "\n".join(lines)

# ── Theme helpers ─────────────────────────────────────────────────────────────
def get_theme():
    return st.session_state.get("dark_mode", True)

def theme(dark_val, light_val):
    return dark_val if get_theme() else light_val

# ── CSS (dynamic based on theme) ─────────────────────────────────────────────
def inject_css(dark):
    bg      = "#080810" if dark else "#f4f4fb"
    bg2     = "#0e0e1a" if dark else "#ffffff"
    bg3     = "#13131f" if dark else "#f0f0fa"
    border  = "#1e1e35" if dark else "#ddddf0"
    text    = "#ececff" if dark else "#1a1a2e"
    subtext = "#6060a0" if dark else "#8888aa"
    muted   = "#2a2a40" if dark else "#888899"
    bubble_bot_bg   = bg3
    bubble_bot_text = "#d8d8f0" if dark else "#1a1a2e"
    followup_hover_color = "#fff" if dark else "#1a1a2e"

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap');

html, body, .stApp, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: {bg} !important;
    color: {text} !important;
}}
.block-container {{ padding: 2rem 2.5rem 5rem; max-width: 780px; }}
#MainMenu, footer, header {{ visibility: hidden; }}

/* HERO */
.hero {{ text-align:center; padding:1.8rem 0 1.2rem; }}
.bot-ring {{
    width:68px; height:68px; border-radius:50%;
    background:linear-gradient(135deg,#f97316,#ec4899,#8b5cf6);
    display:flex; align-items:center; justify-content:center;
    font-size:1.8rem; margin:0 auto 0.8rem;
    box-shadow:0 0 0 4px rgba(236,72,153,0.15), 0 0 28px rgba(236,72,153,0.3);
    animation:glow 3s ease-in-out infinite;
}}
@keyframes glow {{
    0%,100% {{ box-shadow:0 0 0 4px rgba(236,72,153,0.15),0 0 22px rgba(236,72,153,0.25); }}
    50%      {{ box-shadow:0 0 0 6px rgba(236,72,153,0.25),0 0 42px rgba(236,72,153,0.45); }}
}}
.hero-title {{
    font-size:2.8rem; font-weight:800;
    background:linear-gradient(135deg,#f97316,#ec4899,#8b5cf6);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; margin:0 0 0.25rem; letter-spacing:-1px;
}}
.hero-sub {{ font-size:0.72rem; letter-spacing:3px; text-transform:uppercase; color:{muted}; }}

/* COUNTER */
.counter-bar {{ text-align:center; font-size:0.62rem; letter-spacing:2px; text-transform:uppercase; color:{muted}; margin-bottom:1rem; }}

/* CHAT */
.chat-wrap {{
    background:{bg2}; border:1px solid {border};
    border-radius:16px; padding:1.2rem;
    min-height:280px; max-height:400px;
    overflow-y:auto; margin-bottom:1rem;
    scrollbar-width:thin; scrollbar-color:{border} transparent;
}}
.msg-row {{ display:flex; margin-bottom:14px; align-items:flex-end; gap:10px; }}
.msg-row.user {{ flex-direction:row-reverse; }}
.avatar {{
    width:30px; height:30px; border-radius:50%; flex-shrink:0;
    display:flex; align-items:center; justify-content:center; font-size:0.85rem;
}}
.avatar.bot  {{ background:linear-gradient(135deg,#f97316,#ec4899); }}
.avatar.user {{ background:linear-gradient(135deg,#8b5cf6,#2563eb); }}
.bubble {{
    max-width:74%; padding:10px 15px; border-radius:16px;
    font-size:0.92rem; line-height:1.65; word-break:break-word;
}}
.bubble.bot  {{
    background:{bubble_bot_bg}; border:1px solid {border};
    border-bottom-left-radius:4px; color:{bubble_bot_text};
}}
.bubble.user {{
    background:linear-gradient(135deg,#7c3aed,#2563eb);
    border-bottom-right-radius:4px; color:white;
}}
.meta {{ display:flex; gap:5px; margin-top:7px; flex-wrap:wrap; align-items:center; }}
.badge {{
    font-family:'JetBrains Mono',monospace;
    font-size:0.56rem; border-radius:20px; padding:2px 8px;
}}
.badge-tag  {{ background:rgba(139,92,246,0.15); color:#a78bfa; border:1px solid rgba(139,92,246,0.25); }}
.badge-conf {{ background:rgba(249,115,22,0.12); color:#fb923c; border:1px solid rgba(249,115,22,0.2); }}

/* TYPING ANIMATION */
.typing-cursor::after {{
    content:'▋';
    animation:blink 0.7s step-end infinite;
    color:#ec4899;
}}
@keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:0}} }}

/* FOLLOW-UP CHIPS */
.followup-label {{
    font-size:0.62rem; font-weight:700; letter-spacing:2px;
    text-transform:uppercase; color:#ec4899; margin:10px 0 7px;
}}
.followup-wrap {{ display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px; }}
.followup-chip {{
    background:{bg2}; border:1px solid rgba(236,72,153,0.3);
    border-radius:8px; padding:5px 12px; font-size:0.76rem;
    color:#ec4899; cursor:pointer; font-family:'Plus Jakarta Sans',sans-serif;
    transition:all 0.15s;
}}
.followup-chip:hover {{ background:rgba(236,72,153,0.15); color:{followup_hover_color}; }}

/* SUGGESTIONS */
.sugg-label {{
    font-size:0.62rem; font-weight:700; letter-spacing:2px;
    text-transform:uppercase; color:{muted}; margin-bottom:8px;
}}

/* SECTION DIVIDER */
.sdiv {{ border:none; border-top:1px solid {border}; margin:0.8rem 0; }}

/* TEXTAREA */
textarea, .stTextArea textarea,
div[data-baseweb="textarea"] textarea {{
    background-color:{bg2} !important; color:{text} !important;
    border:1.5px solid {border} !important; border-radius:12px !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-size:0.93rem !important; caret-color:#ec4899 !important;
    resize:none !important;
}}
textarea:focus, .stTextArea textarea:focus {{
    border-color:#ec4899 !important;
    box-shadow:0 0 0 3px rgba(236,72,153,0.1) !important;
    outline:none !important;
}}
textarea::placeholder {{ color:{muted} !important; }}

/* SELECTBOX */
div[data-baseweb="select"] > div, .stSelectbox > div > div {{
    background-color:{bg2} !important; border:1.5px solid {border} !important;
    border-radius:10px !important; color:{text} !important;
}}
div[data-baseweb="select"] span,
div[data-baseweb="select"] div {{ color:{text} !important; }}
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="popover"] > div > div {{
    background-color:{bg2} !important;
    border:1px solid {border} !important; border-radius:12px !important;
}}
ul[data-baseweb="menu"],
ul[data-baseweb="menu"] > li {{ background-color:{bg2} !important; }}
li[role="option"] {{
    color:{text} !important; background-color:{bg2} !important; font-size:0.86rem !important;
}}
li[role="option"]:hover {{ background-color:rgba(236,72,153,0.12) !important; color:#fff !important; }}
li[aria-selected="true"] {{ background-color:rgba(236,72,153,0.2) !important; color:#ec4899 !important; }}

/* DOWNLOAD BUTTON */
.stDownloadButton > button {{
    background:linear-gradient(135deg,#f97316,#ec4899) !important;
    color:white !important; font-family:'Plus Jakarta Sans',sans-serif !important;
    font-weight:700 !important; font-size:0.84rem !important;
    border:none !important; border-radius:10px !important;
    padding:0.55rem 1rem !important; width:100% !important;
    transition:all 0.18s !important;
    box-shadow:0 3px 12px rgba(236,72,153,0.22) !important;
}}
.stDownloadButton > button:hover {{
    opacity:0.88 !important; transform:translateY(-1px) !important;
    box-shadow:0 5px 18px rgba(236,72,153,0.38) !important;
}}

/* BUTTONS */
.stButton > button {{
    background:linear-gradient(135deg,#f97316,#ec4899) !important;
    color:white !important; font-family:'Plus Jakarta Sans',sans-serif !important;
    font-weight:700 !important; font-size:0.84rem !important;
    border:none !important; border-radius:10px !important;
    padding:0.55rem 1rem !important; width:100% !important;
    transition:all 0.18s !important;
    box-shadow:0 3px 12px rgba(236,72,153,0.22) !important;
}}
.stButton > button:hover {{
    opacity:0.88 !important; transform:translateY(-1px) !important;
    box-shadow:0 5px 18px rgba(236,72,153,0.38) !important;
}}

/* TABS */
.stTabs [data-baseweb="tab-list"] {{
    background:{bg2} !important; border-radius:10px !important;
    padding:4px !important; border:1px solid {border} !important; gap:4px !important;
}}
.stTabs [data-baseweb="tab"] {{
    color:{text} !important; opacity:0.55; border-radius:8px !important;
    font-size:0.8rem !important; font-weight:600 !important; padding:6px 14px !important;
}}
.stTabs [aria-selected="true"] {{
    background:linear-gradient(135deg,#f97316,#ec4899) !important; color:white !important;
}}
.stTabs [data-baseweb="tab-panel"] {{ padding:0.8rem 0 0 !important; }}

/* FAV CARDS */
.fav-card {{
    background:{bg2}; border:1px solid {border};
    border-radius:12px; padding:12px 16px; margin-bottom:10px;
}}
.fav-q {{ color:#a78bfa; font-weight:700; font-size:0.8rem; margin-bottom:5px; }}
.fav-a {{ color:{subtext}; font-size:0.85rem; line-height:1.6; }}

hr {{ border-color:{border} !important; margin:1.2rem 0 !important; }}
audio {{ width:100%; border-radius:8px; margin-top:6px; }}

/* THEME TOGGLE */
.theme-toggle {{
    position:fixed; top:16px; right:16px; z-index:999;
    background:{bg2}; border:1px solid {border};
    border-radius:20px; padding:5px 12px;
    font-size:0.78rem; color:{subtext}; cursor:pointer;
}}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
WELCOME = {"role":"bot","text":"👋 Hi! I'm **TechBot** — your AI & Technology FAQ assistant.\n\nAsk me anything about **AI, ML, Python, Data Science, Cloud** or **APIs**. I reply in your language too! 🌐","score":None,"tag":None,"done":True}
for k,v in [("messages",[WELCOME]),("msg_count",0),("inp",""),
            ("reply_lang","English"),("favourites",[]),
            ("dark_mode",True),("typing",False),("pending_answer",None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Inject CSS ────────────────────────────────────────────────────────────────
inject_css(get_theme())

# ── THEME TOGGLE ─────────────────────────────────────────────────────────────
tcol1, tcol2, tcol3 = st.columns([7,1,1])
with tcol2:
    if LIMITS["theme"]:
        icon = "☀️" if get_theme() else "🌙"
        if st.button(icon, key="theme_btn"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
with tcol3:
    if st.button("↩️", key="logout_btn", help="Logout"):
        for k in ["logged_in","username","plan","guest","messages","msg_count",
                  "inp","reply_lang","favourites","dark_mode","typing","pending_answer","selected_plan"]:
            if k in st.session_state: del st.session_state[k]
        st.switch_page("app.py")

# ── HERO ─────────────────────────────────────────────────────────────────────
PLAN_COLORS = {"Guest":"#6060a0","Basic":"#06b6d4","Pro":"#ec4899","Ultra":"#8b5cf6"}
plan_color = PLAN_COLORS.get(PLAN,"#ec4899")
st.markdown(f"""
<div class="hero">
  <div class="bot-ring">🤖</div>
  <p class="hero-title">TechBot</p>
  <p class="hero-sub">Technology &amp; AI FAQ Chatbot</p>
  <p style="margin-top:0.5rem">
    <span style="font-size:0.75rem;color:#6060a0">Logged in as </span>
    <span style="font-size:0.8rem;font-weight:700;color:#ececff">{USERNAME}</span>
    &nbsp;
    <span style="background:{plan_color}22;border:1px solid {plan_color}55;border-radius:20px;padding:2px 12px;font-size:0.65rem;font-weight:700;color:{plan_color};letter-spacing:1px;text-transform:uppercase">{PLAN}</span>
  </p>
</div>""", unsafe_allow_html=True)

st.markdown(f'<div class="counter-bar">💬 {st.session_state.msg_count} questions &nbsp;·&nbsp; {len(FAQS)} FAQs &nbsp;·&nbsp; ⭐ {len(st.session_state.favourites)} saved</div>', unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────────────────
tab_chat, tab_favs, tab_export = st.tabs(["💬  Chat", "⭐  Saved", "📤  Export"])

# ════════════════════════════════════════════════════════
with tab_chat:

    # Language selector
    lc1, lc2 = st.columns([1,2])
    with lc1:
        st.markdown('<p style="font-size:0.68rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#ec4899;margin-top:10px">🌐 Reply in</p>', unsafe_allow_html=True)
    with lc2:
        if LIMITS["lang"]:
            reply_lang = st.selectbox(" ", list(REPLY_LANGUAGES.keys()),
                                      index=list(REPLY_LANGUAGES.keys()).index(st.session_state.reply_lang),
                                      key="lang_sel", label_visibility="collapsed")
            st.session_state.reply_lang = reply_lang
        else:
            st.markdown('<div style="background:#13131f;border:1.5px solid #1e1e35;border-radius:10px;padding:8px 12px;font-size:0.82rem;color:#3a3a55">English only &nbsp;<span style="font-size:0.65rem;color:#ec4899;border:1px solid rgba(236,72,153,0.3);border-radius:10px;padding:1px 8px">Pro / Ultra</span></div>', unsafe_allow_html=True)
            st.session_state.reply_lang = "English"

    st.markdown('<hr class="sdiv">', unsafe_allow_html=True)

    # ── TYPING ANIMATION: stream answer word by word ──────────────────────────
    if st.session_state.typing and st.session_state.pending_answer:
        full_text = st.session_state.pending_answer["text"]
        words     = full_text.split()
        displayed = ""
        placeholder = st.empty()
        for i, word in enumerate(words):
            displayed += word + " "
            clean = _re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', displayed.strip())
            placeholder.markdown(
                f'<div style="background:{"#13131f" if get_theme() else "#f0f0fa"};border:1px solid {"#1e1e35" if get_theme() else "#ddddf0"};border-radius:12px;padding:12px 16px;font-size:0.92rem;line-height:1.65;color:{"#d8d8f0" if get_theme() else "#1a1a2e"}">'
                f'🤖 &nbsp;{clean}<span class="typing-cursor"></span></div>',
                unsafe_allow_html=True
            )
            time.sleep(0.03)
        placeholder.empty()
        # commit to messages
        st.session_state.messages.append(st.session_state.pending_answer)
        st.session_state.typing = False
        st.session_state.pending_answer = None
        st.rerun()

    # ── CHAT WINDOW ───────────────────────────────────────────────────────────
    chat_html = '<div class="chat-wrap">'
    for msg in st.session_state.messages:
        if msg["role"] == "bot":
            text  = _re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', msg["text"].replace("\n","<br>"))
            tag   = f'<span class="badge badge-tag">{msg["tag"]}</span>' if msg.get("tag") else ""
            conf  = f'<span class="badge badge-conf">match {msg["score"]:.0%}</span>' if msg.get("score") else ""
            meta  = f'<div class="meta">{tag}{conf}</div>' if (tag or conf) else ""
            chat_html += f'<div class="msg-row bot"><div class="avatar bot">🤖</div><div class="bubble bot">{text}{meta}</div></div>'
        else:
            chat_html += f'<div class="msg-row user"><div class="avatar user">👤</div><div class="bubble user">{msg["text"]}</div></div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # ── FOLLOW-UP QUESTIONS ───────────────────────────────────────────────────
    bot_answers = [m for m in st.session_state.messages if m["role"]=="bot" and m.get("tag")]
    last_user_msg = next((m for m in reversed(st.session_state.messages) if m["role"]=="user"), None)
    if bot_answers:
        last_bot = bot_answers[-1]
        followups = get_followups(last_bot["tag"], last_user_msg["text"] if last_user_msg else "")
        if followups:
            st.markdown('<p class="followup-label">🔁 You might also ask</p>', unsafe_allow_html=True)
            fu_cols = st.columns(len(followups))
            for i, fq in enumerate(followups):
                with fu_cols[i]:
                    if st.button(fq, key=f"fu_{i}_{fq[:10]}"):
                        st.session_state.inp = fq
                        st.rerun()

    # ── ACTION BUTTONS ────────────────────────────────────────────────────────
    if bot_answers:
        last_bot = bot_answers[-1]
        ac1, ac2, ac3 = st.columns(3)
        with ac1:
            fav_limit = LIMITS["fav_limit"]
            if fav_limit == 0:
                st.markdown('<div style="text-align:center;font-size:0.7rem;color:#3a3a55;border:1px solid #1e1e35;border-radius:10px;padding:8px">⭐ Basic+ only</div>', unsafe_allow_html=True)
            elif st.button("⭐  Save Answer", key="save_btn", use_container_width=True):
                entry = {"q": last_user_msg["text"] if last_user_msg else "—",
                         "a": last_bot["text"], "tag": last_bot.get("tag","")}
                if len(st.session_state.favourites) >= fav_limit and fav_limit < 999:
                    st.warning(f"⚠️ Favourite limit reached ({fav_limit}). Upgrade to Pro for unlimited.")
                elif entry not in st.session_state.favourites:
                    st.session_state.favourites.append(entry)
                    st.success("Saved!")
                else:
                    st.info("Already saved.")
        with ac2:
            if not LIMITS["tts"]:
                st.markdown('<div style="text-align:center;font-size:0.7rem;color:#3a3a55;border:1px solid #1e1e35;border-radius:10px;padding:8px">🔊 Pro/Ultra only</div>', unsafe_allow_html=True)
            elif st.button("🔊  Speak Answer", key="speak_btn", use_container_width=True):
                try:
                    lc = REPLY_LANGUAGES[st.session_state.reply_lang]
                    tts = gTTS(text=last_bot["text"], lang=lc, slow=False)
                    buf = io.BytesIO(); tts.write_to_fp(buf); buf.seek(0)
                    b64 = base64.b64encode(buf.read()).decode()
                    st.markdown(f'<audio autoplay controls><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
                except:
                    st.error("TTS not available for this language.")
        with ac3:
            if st.button("🗑️  Clear Chat", key="clear_btn", use_container_width=True):
                st.session_state.messages = [WELCOME]
                st.session_state.msg_count = 0
                st.session_state.inp = ""
                st.rerun()

    st.markdown('<hr class="sdiv">', unsafe_allow_html=True)

    # ── SUGGESTIONS ───────────────────────────────────────────────────────────
    st.markdown('<p class="sugg-label">💡 Quick questions</p>', unsafe_allow_html=True)
    sc = st.columns(4)
    for i, s in enumerate(SUGGESTIONS):
        with sc[i % 4]:
            if st.button(s, key=f"s{i}"):
                st.session_state.inp = s
                st.rerun()

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # ── INPUT + SEND ──────────────────────────────────────────────────────────
    user_input = st.text_area(" ", value=st.session_state.inp,
                               placeholder="Type your question here…",
                               height=78, key="chat_input", label_visibility="collapsed")
    send = st.button("🚀  Send Message", key="send_btn", use_container_width=True)

    # ── PROCESS ───────────────────────────────────────────────────────────────
    query = user_input.strip()
    q_limit = LIMITS["q_limit"]
    if send and query:
        if st.session_state.msg_count >= q_limit:
            st.warning(f"⚠️ You've reached the **{q_limit} question limit** for the **{PLAN}** plan. Login with a Pro/Ultra account for unlimited.")
        else:
            st.session_state.messages.append({"role":"user","text":query})
            st.session_state.msg_count += 1
            st.session_state.inp = ""
            answer, score, tag = get_answer(query)
            if answer:
                lc = REPLY_LANGUAGES[st.session_state.reply_lang]
                if lc != "en":
                    try:
                        answer = GoogleTranslator(source="en", target=lc).translate(answer)
                    except:
                        pass
                st.session_state.pending_answer = {"role":"bot","text":answer,"score":score,"tag":tag,"done":True}
                st.session_state.typing = True
            else:
                st.session_state.messages.append({
                    "role":"bot","text":"🤔 I don't have a specific answer for that yet. Try rephrasing, or ask about **AI, ML, Python, Data Science, APIs, or Cloud**.",
                    "score":None,"tag":None,"done":True
                })
            st.rerun()

# ════════════════════════════════════════════════════════
with tab_favs:
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    if not st.session_state.favourites:
        st.markdown(f"""
        <div style='text-align:center;padding:2.5rem 1rem'>
          <p style='font-size:2.2rem;margin-bottom:0.6rem'>⭐</p>
          <p style='color:{"#3a3a5a" if get_theme() else "#8888aa"};font-size:0.92rem;font-weight:600'>No saved answers yet</p>
          <p style='color:{"#2a2a40" if get_theme() else "#aaaacc"};font-size:0.8rem'>Click <b style="color:#f97316">⭐ Save Answer</b> in the Chat tab to bookmark answers here.</p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f'<p class="sugg-label">⭐ {len(st.session_state.favourites)} saved answers</p>', unsafe_allow_html=True)
        for fav in st.session_state.favourites:
            tag_html = f'&nbsp;<span class="badge badge-tag">{fav["tag"]}</span>' if fav.get("tag") else ""
            st.markdown(f"""
            <div class="fav-card">
              <div class="fav-q">❓ {fav['q']}{tag_html}</div>
              <div class="fav-a">{fav['a']}</div>
            </div>""", unsafe_allow_html=True)
        if st.button("🗑️  Clear All Saved", key="clear_favs"):
            st.session_state.favourites = []
            st.rerun()

# ════════════════════════════════════════════════════════
with tab_export:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if not LIMITS["export"]:
        st.markdown(f"""
        <div style='text-align:center;padding:2.5rem 1rem'>
          <p style='font-size:2rem;margin-bottom:0.6rem'>🔒</p>
          <p style='color:#3a3a5a;font-size:0.95rem;font-weight:600'>Export is a Pro & Ultra feature</p>
          <p style='color:#2a2a40;font-size:0.8rem'>Your current plan: <b style="color:#ec4899">{PLAN}</b><br>Login with a Pro or Ultra account to unlock chat export.</p>
        </div>""", unsafe_allow_html=True)
    else:
        if len(st.session_state.messages) <= 1:
            st.markdown(f"""
            <div style='text-align:center;padding:2rem 1rem'>
              <p style='font-size:2rem;margin-bottom:0.6rem'>📭</p>
              <p style='color:{"#3a3a5a" if get_theme() else "#8888aa"};font-size:0.9rem'>No chat to export yet. Start chatting first!</p>
            </div>""", unsafe_allow_html=True)
        else:
            chat_txt = export_chat_txt()
            st.download_button(
                label="📄  Download as .txt",
                data=chat_txt,
                file_name=f"techbot_chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="dl_txt"
            )
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.markdown(f'<p class="sugg-label">👁️ Preview</p>', unsafe_allow_html=True)
            preview_bg = "#0e0e1a" if get_theme() else "#ffffff"
            preview_color = "#ececff" if get_theme() else "#1a1a2e"
            preview_border = "#1e1e35" if get_theme() else "#ddddf0"
            st.markdown(f"""
            <div style="background:{preview_bg};border:1px solid {preview_border};border-radius:12px;
                        padding:14px 18px;font-size:0.8rem;color:{preview_color};
                        line-height:1.8;max-height:220px;overflow-y:auto;
                        font-family:'JetBrains Mono',monospace;white-space:pre-wrap">{chat_txt[:800]}{"..." if len(chat_txt)>800 else ""}</div>
            """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
footer_color = '#1e1e35' if get_theme() else '#ccccdd'
st.markdown(f"<p style='text-align:center;color:{footer_color};font-size:0.62rem;letter-spacing:3px'>TECHBOT — AI FAQ CHATBOT</p>", unsafe_allow_html=True)