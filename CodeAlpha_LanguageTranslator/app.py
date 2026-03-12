import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64, io

st.set_page_config(page_title="LinguaFlow", page_icon="🌐", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, .stApp, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #0f0e17 !important;
    color: #fffffe !important;
}
.block-container { padding: 2rem 3rem; max-width: 1100px; }
#MainMenu, footer, header { visibility: hidden; }

/* ── HERO ── */
.hero { text-align: center; padding: 2.5rem 0 1.5rem; }
.hero-icon {
    font-size: 3.2rem;
    margin-bottom: 0.2rem;
    display: block;
    filter: none !important;
    -webkit-text-fill-color: initial !important;
}
.hero-title {
    font-size: 6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a855f7, #6366f1, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem;
    letter-spacing: -2px;
    line-height: 1;
}
.hero-sub {
    font-size: 0.82rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #555;
    margin: 0;
}

/* ── STAT CARDS ── */
.stats-row { display: flex; gap: 12px; margin-bottom: 2rem; }
.stat-card {
    flex: 1;
    background: #1a1828;
    border: 1px solid #2a2740;
    border-radius: 14px;
    padding: 14px 10px;
    text-align: center;
}
.stat-num { font-size: 1.6rem; font-weight: 700; color: #7c3aed; line-height: 1; }
.stat-lbl { font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase; color: #555; margin-top: 4px; }

/* ── FIELD LABEL ── */
.field-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #7c3aed;
    margin-bottom: 6px;
}

/* ── TEXTAREA ── */
textarea, .stTextArea textarea,
div[data-baseweb="textarea"] textarea {
    background-color: #1a1828 !important;
    color: #fffffe !important;
    border: 1.5px solid #2a2740 !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    caret-color: #7c3aed !important;
    resize: none !important;
}
textarea:focus, .stTextArea textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
    outline: none !important;
}
textarea::placeholder { color: #3a3850 !important; }

/* ── SELECTBOX ── */
div[data-baseweb="select"] > div,
.stSelectbox > div > div {
    background-color: #1a1828 !important;
    border: 1.5px solid #2a2740 !important;
    border-radius: 12px !important;
    color: #fffffe !important;
}
div[data-baseweb="select"] span { color: #fffffe !important; }
div[data-baseweb="popover"] {
    background: #1a1828 !important;
    border: 1px solid #2a2740 !important;
    border-radius: 12px !important;
}
ul[data-baseweb="menu"] { background: #1a1828 !important; }
li[role="option"] { color: #fffffe !important; background: transparent !important; }
li[role="option"]:hover { background: rgba(124,58,237,0.15) !important; }
li[aria-selected="true"] { background: rgba(124,58,237,0.2) !important; }

/* ── RESULT BOX ── */
.result-box {
    background: #1a1828;
    border: 1.5px solid rgba(124,58,237,0.4);
    border-radius: 12px;
    padding: 14px 16px;
    min-height: 152px;
    font-size: 1.05rem;
    color: #e9d5ff;
    line-height: 1.8;
    word-break: break-word;
}
.result-empty {
    background: #1a1828;
    border: 1.5px dashed #2a2740;
    border-radius: 12px;
    padding: 14px 16px;
    min-height: 152px;
    font-size: 0.92rem;
    color: #3a3850;
    font-style: italic;
}

/* ── CHAR COUNT ── */
.char-count {
    font-size: 0.7rem;
    color: #3a3850;
    text-align: right;
    margin-top: -6px;
    margin-bottom: 4px;
}

/* ── ALL BUTTONS — solid #7c3aed, visible everywhere ── */
.stButton > button {
    background-color: #7c3aed !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1rem !important;
    width: 100% !important;
    transition: background-color 0.2s, transform 0.15s !important;
    box-shadow: none !important;
}
.stButton > button:hover {
    background-color: #6d28d9 !important;
    transform: translateY(-2px) !important;
    color: #ffffff !important;
}
.stButton > button:active {
    background-color: #5b21b6 !important;
    transform: translateY(0) !important;
}

/* ── HISTORY CARDS ── */
.hist-card {
    background: #1a1828;
    border: 1px solid #2a2740;
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 8px;
}
.hist-langs {
    font-size: 0.62rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #7c3aed;
    margin-bottom: 6px;
}
.hist-orig { color: #888; font-size: 0.88rem; }
.hist-res  { color: #c4b5fd; font-size: 0.88rem; margin-top: 4px; }

hr { border-color: #1a1828 !important; margin: 1.5rem 0 !important; }

audio {
    width: 100%;
    border-radius: 8px;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

# ── LANGUAGES ─────────────────────────────────────────────────────────────────
LANGUAGES = {
    "English":"en",   "Hindi":"hi",     "Tamil":"ta",
    "Telugu":"te",    "Kannada":"kn",   "Malayalam":"ml",
    "Bengali":"bn",   "Marathi":"mr",   "Gujarati":"gu",
    "Punjabi":"pa",   "Urdu":"ur",      "French":"fr",
    "German":"de",    "Spanish":"es",   "Italian":"it",
    "Portuguese":"pt","Russian":"ru",   "Japanese":"ja",
    "Chinese (Simplified)":"zh-CN",     "Korean":"ko",
    "Arabic":"ar",    "Turkish":"tr",   "Dutch":"nl",
    "Polish":"pl",    "Swedish":"sv",   "Greek":"el",
    "Thai":"th",      "Vietnamese":"vi","Indonesian":"id",
}
LANG_NAMES = list(LANGUAGES.keys())

# ── SESSION STATE ──────────────────────────────────────────────────────────────
for k, v in [("result",""), ("inp",""), ("src_idx",0),
              ("tgt_idx",1), ("count",0), ("history",[])]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <span class="hero-icon">🌐</span>
  <p class="hero-title">LinguaFlow</p>
  <p class="hero-sub">AI Language Translator</p>
</div>
""", unsafe_allow_html=True)

# ── STATS ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stats-row">
  <div class="stat-card"><div class="stat-num">{len(LANGUAGES)}</div><div class="stat-lbl">Languages</div></div>
  <div class="stat-card"><div class="stat-num">{st.session_state.count}</div><div class="stat-lbl">Translated</div></div>
  <div class="stat-card"><div class="stat-num">{len(st.session_state.history)}</div><div class="stat-lbl">History</div></div>
</div>
""", unsafe_allow_html=True)

# ── MAIN PANEL ────────────────────────────────────────────────────────────────
col_l, col_r = st.columns(2)

with col_l:
    st.markdown('<p class="field-label">Source Language</p>', unsafe_allow_html=True)
    src_sel = st.selectbox(" ", LANG_NAMES,
                           index=st.session_state.src_idx,
                           key="src_box", label_visibility="collapsed")
    st.markdown('<p class="field-label" style="margin-top:1rem">Enter Text</p>', unsafe_allow_html=True)
    inp = st.text_area(" ", value=st.session_state.inp,
                        placeholder="Type or paste text here…",
                        height=152, key="inp_area", label_visibility="collapsed")
    wc = len(inp.split()) if inp.strip() else 0
    st.markdown(f'<p class="char-count">{len(inp)} / 5000 chars &nbsp;·&nbsp; {wc} words</p>',
                unsafe_allow_html=True)

with col_r:
    st.markdown('<p class="field-label">Target Language</p>', unsafe_allow_html=True)
    tgt_sel = st.selectbox("  ", LANG_NAMES,
                           index=st.session_state.tgt_idx,
                           key="tgt_box", label_visibility="collapsed")
    st.markdown('<p class="field-label" style="margin-top:1rem">Translation</p>', unsafe_allow_html=True)
    if st.session_state.result:
        st.markdown(f'<div class="result-box">{st.session_state.result}</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-empty">Translation will appear here after you click Translate…</div>',
                    unsafe_allow_html=True)

# ── TRANSLATE BUTTON ──────────────────────────────────────────────────────────
st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
_, bc, _ = st.columns([4, 6, 4])
with bc:
    clicked = st.button("✦  TRANSLATE", key="trans_btn", use_container_width=True)

# ── TRANSLATION LOGIC ─────────────────────────────────────────────────────────
if clicked:
    if not inp.strip():
        st.warning("⚠️  Please enter some text first.")
    else:
        with st.spinner("Translating…"):
            try:
                sc  = LANGUAGES[src_sel]
                tc  = LANGUAGES[tgt_sel]
                res = inp if sc == tc else GoogleTranslator(source=sc, target=tc).translate(inp)

                st.session_state.result  = res
                st.session_state.inp     = inp
                st.session_state.src_idx = LANG_NAMES.index(src_sel)
                st.session_state.tgt_idx = LANG_NAMES.index(tgt_sel)
                st.session_state.count  += 1

                entry = {
                    "src":  src_sel,
                    "tgt":  tgt_sel,
                    "orig": inp[:60] + ("…" if len(inp) > 60 else ""),
                    "res":  res[:60] + ("…" if len(res) > 60 else ""),
                }
                st.session_state.history.insert(0, entry)
                st.session_state.history = st.session_state.history[:10]

                st.rerun()
            except Exception as e:
                st.error(f"Translation failed: {e}")

# ── ACTION BUTTONS ────────────────────────────────────────────────────────────
if st.session_state.result:
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    st.markdown('<p class="field-label">Actions</p>', unsafe_allow_html=True)

    a1, a2, a3 = st.columns(3)

    with a1:
        if st.button("📋  COPY", key="copy_btn", use_container_width=True):
            st.code(st.session_state.result, language=None)
            st.success("✅  Select all text above → Ctrl+A → Ctrl+C")

    with a2:
        if st.button("🔊  SPEAK", key="speak_btn", use_container_width=True):
            try:
                tc  = LANGUAGES[LANG_NAMES[st.session_state.tgt_idx]]
                tts = gTTS(text=st.session_state.result, lang=tc, slow=False)
                buf = io.BytesIO()
                tts.write_to_fp(buf); buf.seek(0)
                b64 = base64.b64encode(buf.read()).decode()
                st.markdown(
                    f'<audio autoplay controls>'
                    f'<source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>',
                    unsafe_allow_html=True)
            except:
                st.error("TTS not available for this language.")

    with a3:
        if st.button("🗑️  CLEAR", key="clear_btn", use_container_width=True):
            st.session_state.result = ""
            st.session_state.inp    = ""
            st.rerun()

# ── HISTORY ───────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="field-label">Recent Translations</p>', unsafe_allow_html=True)
    for h in st.session_state.history:
        st.markdown(f"""
        <div class="hist-card">
          <div class="hist-langs">{h['src']} &nbsp;→&nbsp; {h['tgt']}</div>
          <div class="hist-orig">{h['orig']}</div>
          <div class="hist-res">↳ &nbsp;{h['res']}</div>
        </div>""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#2a2740;font-size:0.68rem;letter-spacing:3px'>"
    "CODEALPHA INTERNSHIP &nbsp;·&nbsp; TASK 1 &nbsp;·&nbsp; LINGUAFLOW</p>",
    unsafe_allow_html=True)
