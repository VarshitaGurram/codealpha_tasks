import streamlit as st

st.set_page_config(page_title="TechBot — AI FAQ Chatbot", page_icon="🤖",
                   layout="wide", initial_sidebar_state="collapsed")

for k, v in [("logged_in", False), ("username", ""), ("plan", ""), ("guest", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state.logged_in or st.session_state.guest:
    st.switch_page("pages/chat.py")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap');

html, body, .stApp, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #060610 !important;
    color: #ececff !important;
}
#MainMenu, footer, header, section[data-testid="stSidebar"],
.stDeployButton, div[data-testid="stToolbar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
[data-testid="stAppViewContainer"] > section { padding: 0 !important; }
[data-testid="stVerticalBlock"] { gap: 0rem !important; }
div[data-testid="column"] { padding: 0 0.3rem !important; }
.hero-section { margin: 0 auto !important; }

/* NAV */
.navbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.1rem 5rem; border-bottom: 1px solid #1a1a2e;
    background: rgba(6,6,16,0.97); position: sticky; top: 0; z-index: 999;
}
.nav-logo {
    font-size: 1.35rem; font-weight: 900;
    background: linear-gradient(135deg,#f97316,#ec4899,#8b5cf6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.nav-links { display: flex; gap: 2.5rem; align-items: center; }
.nav-link {
    font-size: 0.84rem; color: #6060a0; font-weight: 600;
    cursor: pointer; text-decoration: none; transition: color 0.2s;
}
.nav-link:hover { color: #ec4899; }

/* HERO */
.hero-section {
    text-align: center; padding: 7rem 2rem 1.5rem;
    background: radial-gradient(ellipse at 50% 0%, rgba(236,72,153,0.13) 0%, transparent 65%);
    width: 100%;
}
/* Hero background extends to button row */
[data-testid="stHorizontalBlock"] {
    background: radial-gradient(ellipse at 50% 100%, rgba(236,72,153,0.06) 0%, transparent 70%);
    justify-content: center !important;
    padding: 0 0 0.5rem 0 !important;
}
.hero-badge {
    display: inline-block; background: rgba(236,72,153,0.12);
    border: 1px solid rgba(236,72,153,0.3); border-radius: 20px;
    padding: 5px 18px; font-size: 0.7rem; color: #ec4899;
    letter-spacing: 2px; text-transform: uppercase; margin-bottom: 1.6rem; font-weight: 700;
}
.hero-title {
    font-size: 4.5rem; font-weight: 900; line-height: 1.05;
    background: linear-gradient(135deg,#fff 0%,#f97316 35%,#ec4899 65%,#8b5cf6 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    margin: 0 0 1.2rem; letter-spacing: -2px;
}
.hero-sub {
    font-size: 1.1rem; color: #6060a0; max-width: 560px;
    margin: 0 auto 2.5rem; line-height: 1.75;
}

/* STREAMLIT BUTTONS */
.stButton > button {
    background: linear-gradient(135deg,#f97316,#ec4899) !important;
    color: white !important; font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 0.92rem !important;
    border: none !important; border-radius: 12px !important;
    padding: 0.7rem 1.5rem !important; width: 100% !important;
    box-shadow: 0 4px 20px rgba(236,72,153,0.3) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-2px) !important; }

/* OUTLINE BUTTON variant */
.btn-outline-wrap .stButton > button {
    background: transparent !important;
    border: 1.5px solid #2a2a45 !important;
    box-shadow: none !important; color: #ececff !important;
}
.btn-outline-wrap .stButton > button:hover {
    border-color: #ec4899 !important; color: #ec4899 !important;
}

/* SECTION */
.section { padding: 4rem 5rem; }
.section-label {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: #ec4899; margin-bottom: 0.7rem;
}
.section-title { font-size: 2.5rem; font-weight: 800; margin: 0 0 0.5rem; letter-spacing: -0.5px; }
.section-sub { font-size: 0.95rem; color: #6060a0; margin-bottom: 2.5rem; }
.divider { border: none; border-top: 1px solid #1a1a2e; margin: 0; }

/* FEATURE CARDS */
.features-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1.2rem; }
.feature-card {
    background: #0d0d1a; border: 1px solid #1a1a2e; border-radius: 16px;
    padding: 1.6rem; transition: all 0.2s;
}
.feature-card:hover {
    border-color: rgba(236,72,153,0.4); transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(236,72,153,0.08);
}
.feature-icon { font-size: 2rem; margin-bottom: 0.8rem; }
.feature-title { font-size: 1rem; font-weight: 700; margin-bottom: 0.4rem; }
.feature-desc { font-size: 0.83rem; color: #5a5a90; line-height: 1.65; }

/* PRICING */
.pricing-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-top: 2rem; }
.plan-card {
    background: #0d0d1a; border: 1px solid #1a1a2e;
    border-radius: 18px; padding: 1.8rem 1.4rem; position: relative;
}
.plan-card.featured {
    border-color: rgba(236,72,153,0.5);
    background: linear-gradient(160deg,rgba(249,115,22,0.07),rgba(236,72,153,0.07));
    box-shadow: 0 0 50px rgba(236,72,153,0.1);
}
.plan-badge {
    position: absolute; top: -13px; left: 50%; transform: translateX(-50%);
    background: linear-gradient(135deg,#f97316,#ec4899); color: white;
    border-radius: 20px; padding: 3px 14px; font-size: 0.62rem; font-weight: 700;
    letter-spacing: 1px; text-transform: uppercase; white-space: nowrap;
}
.plan-name { font-size: 0.72rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #6060a0; margin-bottom: 0.5rem; }
.plan-price { font-size: 2.5rem; font-weight: 900; margin: 0 0 0.25rem; line-height: 1; color: #ececff; }
.plan-price span { font-size: 0.85rem; font-weight: 400; color: #6060a0; }
.plan-desc { font-size: 0.78rem; color: #6060a0; margin-bottom: 1.2rem; line-height: 1.5; }
.plan-features { list-style: none; padding: 0; margin: 0; }
.plan-features li {
    font-size: 0.8rem; color: #9090bb; padding: 6px 0;
    border-bottom: 1px solid #13131f; display: flex; align-items: center; gap: 6px;
}
.plan-features li::before { content: "✓"; color: #ec4899; font-weight: 700; flex-shrink: 0; }
.plan-features li.no { color: #2e2e4a; }
.plan-features li.no::before { content: "✗"; color: #2e2e4a; }

/* STEPS */
.steps-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 1.5rem; }
.step-card { text-align: center; padding: 1.5rem 1rem; }
.step-num {
    width: 46px; height: 46px; border-radius: 50%;
    background: linear-gradient(135deg,#f97316,#ec4899);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; font-weight: 900; color: white; margin: 0 auto 1rem;
}
.step-title { font-size: 0.95rem; font-weight: 700; margin-bottom: 0.4rem; }
.step-desc { font-size: 0.81rem; color: #5a5a90; line-height: 1.65; }

/* CTA */
.cta-section {
    text-align: center; padding: 4.5rem 2rem;
    background: radial-gradient(ellipse at 50% 100%,rgba(236,72,153,0.1) 0%,transparent 65%);
}
.cta-title { font-size: 2.6rem; font-weight: 900; margin: 0 0 0.8rem; letter-spacing: -0.5px; }
.cta-sub { color: #6060a0; font-size: 1rem; margin: 0 0 2rem; line-height: 1.7; }

/* FOOTER */
.footer {
    padding: 2rem 5rem; border-top: 1px solid #1a1a2e;
    display: flex; justify-content: space-between; align-items: center;
}
.footer-logo {
    font-size: 1.1rem; font-weight: 900;
    background: linear-gradient(135deg,#f97316,#ec4899);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.footer-copy { font-size: 0.72rem; color: #2a2a45; }

/* Anchor offset for sticky nav */
.anchor { display: block; position: relative; top: -80px; visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── NAVBAR ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <div class="nav-logo">🤖 TechBot</div>
  <div class="nav-links">
    <a class="nav-link" href="#features">Features</a>
    <a class="nav-link" href="#pricing">Pricing</a>
    <a class="nav-link" href="#howitworks">How it works</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
  <div class="hero-badge">✦ AI FAQ Chatbot</div>
  <h1 class="hero-title">Your AI Tech<br>FAQ Assistant</h1>
  <p class="hero-sub">Ask anything about AI, Machine Learning, Python, Cloud Computing, and more.
  Get instant smart answers in your own language.</p>
</div>
<div style="height:0.5rem"></div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns([2, 1.5, 0.3, 1.5, 2])
with col2:
    if st.button("🚀  Get Started — Free", key="gs", use_container_width=True):
        st.switch_page("pages/login.py")
with col4:
    st.markdown('<div class="btn-outline-wrap">', unsafe_allow_html=True)
    if st.button("👤  Login to Account", key="li", use_container_width=True):
        st.switch_page("pages/login.py")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:2.5rem;background:radial-gradient(ellipse at 50% 0%,rgba(236,72,153,0.13) 0%,transparent 65%)"></div>', unsafe_allow_html=True)

# ── FEATURES ──────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider"><span class="anchor" id="features"></span>', unsafe_allow_html=True)
st.markdown("""
<div class="section">
  <p class="section-label">✦ What TechBot offers</p>
  <h2 class="section-title">Packed with smart features</h2>
  <p class="section-sub">Everything you need to explore Tech &amp; AI — beautifully designed.</p>
  <div class="features-grid">
    <div class="feature-card"><div class="feature-icon">🧠</div><div class="feature-title">NLP Answer Matching</div><div class="feature-desc">TF-IDF cosine similarity matches your question even with typos or short queries like "what is ai".</div></div>
    <div class="feature-card"><div class="feature-icon">🌐</div><div class="feature-title">11 Languages</div><div class="feature-desc">Get answers in Hindi, Tamil, Telugu, French, Spanish, Japanese, Arabic, Korean, Chinese, German, and English.</div></div>
    <div class="feature-card"><div class="feature-icon">⌨️</div><div class="feature-title">Typing Animation</div><div class="feature-desc">Answers appear word by word with a live blinking cursor — feels like a real AI typing back to you.</div></div>
    <div class="feature-card"><div class="feature-icon">🔁</div><div class="feature-title">Follow-up Suggestions</div><div class="feature-desc">After every answer, TechBot recommends 3 related questions to deepen your learning.</div></div>
    <div class="feature-card"><div class="feature-icon">⭐</div><div class="feature-title">Save Favourites</div><div class="feature-desc">Bookmark answers you love into your personal Saved tab, always accessible.</div></div>
    <div class="feature-card"><div class="feature-icon">🔊</div><div class="feature-title">Text-to-Speech</div><div class="feature-desc">Listen to answers read aloud in your chosen language using Google TTS.</div></div>
    <div class="feature-card"><div class="feature-icon">📤</div><div class="feature-title">Export Chat</div><div class="feature-desc">Download your entire conversation as a clean .txt file — perfect for study notes.</div></div>
    <div class="feature-card"><div class="feature-icon">🌙</div><div class="feature-title">Dark / Light Mode</div><div class="feature-desc">Toggle between themes. Every element adapts perfectly.</div></div>
    <div class="feature-card"><div class="feature-icon">🔐</div><div class="feature-title">User Accounts</div><div class="feature-desc">Sign up with username and password. Your plan is saved securely.</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── PRICING ───────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider"><span class="anchor" id="pricing"></span>', unsafe_allow_html=True)
st.markdown("""
<div class="section">
  <p class="section-label">✦ Plans &amp; Pricing</p>
  <h2 class="section-title">Start free. Upgrade anytime.</h2>
  <p class="section-sub">Pick the plan that fits you best.</p>
  <div class="pricing-grid">
    <div class="plan-card">
      <div class="plan-name">Guest</div><div class="plan-price">Free<span> / no login</span></div>
      <div class="plan-desc">Try TechBot without an account.</div>
      <ul class="plan-features">
        <li>5 questions per session</li><li>English only</li><li>All FAQ answers</li><li>Follow-up suggestions</li>
        <li class="no">Save favourites</li><li class="no">Export chat</li><li class="no">Multilingual replies</li><li class="no">Text-to-speech</li><li class="no">Dark / Light mode</li>
      </ul>
    </div>
    <div class="plan-card">
      <div class="plan-name">Basic</div><div class="plan-price">Free<span> / signup</span></div>
      <div class="plan-desc">Great for beginners starting out.</div>
      <ul class="plan-features">
        <li>20 questions per session</li><li>English only</li><li>All 34 FAQs</li><li>Follow-up suggestions</li><li>Save up to 5 favourites</li>
        <li class="no">Export chat</li><li class="no">Multilingual replies</li><li class="no">Text-to-speech</li><li class="no">Dark / Light mode</li>
      </ul>
    </div>
    <div class="plan-card featured">
      <div class="plan-badge">⭐ Most Popular</div>
      <div class="plan-name">Pro</div><div class="plan-price">₹299<span> / month</span></div>
      <div class="plan-desc">For learners who want the full experience.</div>
      <ul class="plan-features">
        <li>Unlimited questions</li><li>11 languages</li><li>All 34 FAQs</li><li>Follow-up suggestions</li>
        <li>Unlimited favourites</li><li>Export chat (.txt)</li><li>Text-to-speech</li><li>Dark / Light mode</li>
        <li class="no">Early access features</li>
      </ul>
    </div>
    <div class="plan-card">
      <div class="plan-name">Ultra</div><div class="plan-price">₹599<span> / month</span></div>
      <div class="plan-desc">Every feature. Nothing held back.</div>
      <ul class="plan-features">
        <li>Unlimited questions</li><li>11 languages</li><li>All 34 FAQs</li><li>Follow-up suggestions</li>
        <li>Unlimited favourites</li><li>Export chat (.txt)</li><li>Text-to-speech</li><li>Dark / Light mode</li><li>Early access features</li>
      </ul>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── HOW IT WORKS ──────────────────────────────────────────────────────────────
st.markdown('<hr class="divider"><span class="anchor" id="howitworks"></span>', unsafe_allow_html=True)
st.markdown("""
<div class="section">
  <p class="section-label">✦ Simple process</p>
  <h2 class="section-title">How it works</h2>
  <p class="section-sub">Up and chatting in under 30 seconds.</p>
  <div class="steps-grid">
    <div class="step-card"><div class="step-num">1</div><div class="step-title">Sign up or Login</div><div class="step-desc">Create a free account in seconds, or continue as a guest without signing up.</div></div>
    <div class="step-card"><div class="step-num">2</div><div class="step-title">Choose your plan</div><div class="step-desc">Pick Guest, Basic, Pro, or Ultra.</div></div>
    <div class="step-card"><div class="step-num">3</div><div class="step-title">Ask your question</div><div class="step-desc">Type anything about AI, ML, Python, or Cloud. Even short queries like "what is ai" work perfectly.</div></div>
    <div class="step-card"><div class="step-num">4</div><div class="step-title">Learn and explore</div><div class="step-desc">Follow-ups, save favourites, switch language, listen to answers, export your chat.</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── CTA ───────────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<div class="cta-section">
  <h2 class="cta-title">Ready to explore AI &amp; Tech?</h2>
  <p class="cta-sub">Join TechBot for free. No credit card. No setup. Just ask.</p>
</div>
""", unsafe_allow_html=True)

_, cc, _ = st.columns([3, 2, 3])
with cc:
    if st.button("🚀  Start for Free", key="cta", use_container_width=True):
        st.switch_page("pages/login.py")

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div class="footer-logo">🤖 TechBot</div>
  <div class="footer-copy">TechBot — AI FAQ Chatbot</div>
</div>
""", unsafe_allow_html=True)