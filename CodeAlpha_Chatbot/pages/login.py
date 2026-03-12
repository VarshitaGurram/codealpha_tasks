import streamlit as st
import json, os, hashlib, re

st.set_page_config(page_title="TechBot — Login", page_icon="🤖",
                   layout="centered", initial_sidebar_state="collapsed")

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f: json.dump({}, f)
    with open(USERS_FILE) as f: return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w") as f: json.dump(data, f, indent=2)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def validate_username(u):
    return re.match(r'^[a-zA-Z0-9_]{3,20}$', u) is not None

def validate_password(p):
    return len(p) >= 6

for k,v in [("logged_in",False),("username",""),("plan",""),
            ("guest",False),("auth_tab","login")]:
    if k not in st.session_state: st.session_state[k] = v

if st.session_state.logged_in or st.session_state.guest:
    st.switch_page("pages/chat.py")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500&display=swap');
html,body,.stApp,[class*="css"]{font-family:'Plus Jakarta Sans',sans-serif !important;background-color:#060610 !important;color:#ececff !important;}
#MainMenu,footer,header,section[data-testid="stSidebar"]{display:none !important;}
.block-container{padding:2rem 1rem 4rem !important;max-width:480px !important;}

.back-btn{font-size:0.78rem;color:#6060a0;cursor:pointer;margin-bottom:1.5rem;display:inline-flex;align-items:center;gap:6px;}
.back-btn:hover{color:#ec4899;}

.auth-card{background:#0d0d1a;border:1px solid #1a1a2e;border-radius:20px;padding:2.4rem 2rem;}
.auth-logo{text-align:center;margin-bottom:1.5rem;}
.auth-logo-icon{font-size:2.8rem;}
.auth-logo-text{font-size:1.6rem;font-weight:900;background:linear-gradient(135deg,#f97316,#ec4899,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.auth-title{font-size:1.35rem;font-weight:800;text-align:center;margin-bottom:0.3rem;}
.auth-sub{font-size:0.83rem;color:#6060a0;text-align:center;margin-bottom:1.8rem;line-height:1.6;}

.plan-select-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-bottom:1rem;}
.plan-opt{background:#13131f;border:2px solid #1e1e35;border-radius:12px;padding:10px 14px;cursor:pointer;transition:all 0.15s;}
.plan-opt.selected{border-color:#ec4899;background:rgba(236,72,153,0.08);}
.plan-opt-name{font-size:0.78rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#ec4899;margin-bottom:2px;}
.plan-opt-desc{font-size:0.7rem;color:#5a5a90;line-height:1.4;}

.divider-line{display:flex;align-items:center;gap:10px;margin:1.2rem 0;}
.divider-line hr{flex:1;border:none;border-top:1px solid #1e1e35;}
.divider-line span{font-size:0.72rem;color:#3a3a55;font-weight:600;}

.guest-card{background:#13131f;border:1px solid #1e1e35;border-radius:14px;padding:14px 16px;text-align:center;cursor:pointer;transition:all 0.15s;}
.guest-card:hover{border-color:rgba(236,72,153,0.3);}
.guest-title{font-size:0.88rem;font-weight:700;margin-bottom:3px;}
.guest-sub{font-size:0.74rem;color:#5a5a90;}

/* inputs */
input[type="text"], input[type="password"],
.stTextInput input{
    background-color:#13131f !important;color:#ececff !important;
    border:1.5px solid #1e1e35 !important;border-radius:10px !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;font-size:0.92rem !important;
    padding:10px 14px !important;
}
input:focus,.stTextInput input:focus{border-color:#ec4899 !important;box-shadow:0 0 0 3px rgba(236,72,153,0.1) !important;outline:none !important;}
.stTextInput label{font-size:0.78rem !important;font-weight:600 !important;color:#8888aa !important;letter-spacing:0.5px !important;margin-bottom:4px !important;}
.stTextInput>div>div{background:transparent !important;}

/* tabs */
.stTabs [data-baseweb="tab-list"]{background:#13131f !important;border-radius:10px !important;padding:4px !important;border:1px solid #1e1e35 !important;gap:4px !important;}
.stTabs [data-baseweb="tab"]{color:#6060a0 !important;border-radius:8px !important;font-size:0.82rem !important;font-weight:600 !important;padding:7px 20px !important;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#f97316,#ec4899) !important;color:white !important;}
.stTabs [data-baseweb="tab-panel"]{padding:1.2rem 0 0 !important;}

/* buttons */
.stButton>button{background:linear-gradient(135deg,#f97316,#ec4899) !important;color:white !important;font-family:'Plus Jakarta Sans',sans-serif !important;font-weight:700 !important;font-size:0.9rem !important;border:none !important;border-radius:10px !important;padding:0.6rem 1rem !important;width:100% !important;transition:all 0.18s !important;box-shadow:0 4px 18px rgba(236,72,153,0.28) !important;}
.stButton>button:hover{opacity:0.88 !important;transform:translateY(-1px) !important;}
</style>
""", unsafe_allow_html=True)

# Back button
if st.button("← Back to Home", key="back_home"):
    st.switch_page("app.py")

# Logo
st.markdown("""
<div class="auth-card">
  <div class="auth-logo">
    <div class="auth-logo-icon">🤖</div>
    <div class="auth-logo-text">TechBot</div>
  </div>
""", unsafe_allow_html=True)

tab_login, tab_signup = st.tabs(["🔐  Login", "✨  Sign Up"])

# ── LOGIN ─────────────────────────────────────────────────────────────────────
with tab_login:
    st.markdown('<p style="font-size:0.78rem;color:#6060a0;text-align:center;margin-bottom:1.2rem">Welcome back! Login to your TechBot account.</p>', unsafe_allow_html=True)
    l_user = st.text_input("Username", key="l_user", placeholder="Enter your username")
    l_pass = st.text_input("Password", key="l_pass", placeholder="Enter your password", type="password")

    if st.button("🔐  Login to TechBot", key="login_btn", use_container_width=True):
        if not l_user or not l_pass:
            st.error("Please fill in all fields.")
        else:
            users = load_users()
            if l_user in users and users[l_user]["password"] == hash_pw(l_pass):
                st.session_state.logged_in = True
                st.session_state.username  = l_user
                st.session_state.plan      = users[l_user].get("plan","Basic")
                st.success(f"✅ Welcome back, {l_user}! Redirecting...")
                st.switch_page("pages/chat.py")
            else:
                st.error("❌ Incorrect username or password.")

    st.markdown('<div class="divider-line"><hr><span>OR</span><hr></div>', unsafe_allow_html=True)

    if st.button("👻  Continue as Guest (5 questions)", key="guest_login", use_container_width=True):
        st.session_state.guest    = True
        st.session_state.plan     = "Guest"
        st.session_state.username = "Guest"
        st.switch_page("pages/chat.py")

# ── SIGNUP ────────────────────────────────────────────────────────────────────
with tab_signup:
    st.markdown('<p style="font-size:0.78rem;color:#6060a0;text-align:center;margin-bottom:1.2rem">Create your free TechBot account in seconds.</p>', unsafe_allow_html=True)

    s_user = st.text_input("Choose a Username", key="s_user", placeholder="3–20 chars, letters/numbers/_")
    s_pass = st.text_input("Choose a Password", key="s_pass", placeholder="Min. 6 characters", type="password")
    s_pass2= st.text_input("Confirm Password",  key="s_pass2",placeholder="Repeat your password", type="password")

    # Plan picker
    st.markdown('<p style="font-size:0.78rem;font-weight:600;color:#8888aa;margin:0.8rem 0 0.5rem">Select your plan</p>', unsafe_allow_html=True)
    if "selected_plan" not in st.session_state:
        st.session_state.selected_plan = "Pro"

    # Plan cards with pricing
    st.markdown("""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:1rem">
      <div style="background:#13131f;border:2px solid #1e1e35;border-radius:12px;padding:10px 14px">
        <div style="font-size:0.7rem;font-weight:700;color:#06b6d4;letter-spacing:1px;text-transform:uppercase">Basic</div>
        <div style="font-size:1.3rem;font-weight:900;color:#ececff;margin:2px 0">Free</div>
        <div style="font-size:0.7rem;color:#5a5a90">20 questions · English only</div>
      </div>
      <div style="background:#13131f;border:2px solid rgba(236,72,153,0.4);border-radius:12px;padding:10px 14px;position:relative">
        <div style="position:absolute;top:-9px;left:50%;transform:translateX(-50%);background:linear-gradient(135deg,#f97316,#ec4899);color:white;border-radius:10px;padding:1px 10px;font-size:0.55rem;font-weight:700;white-space:nowrap">⭐ POPULAR</div>
        <div style="font-size:0.7rem;font-weight:700;color:#ec4899;letter-spacing:1px;text-transform:uppercase">Pro</div>
        <div style="font-size:1.3rem;font-weight:900;color:#ececff;margin:2px 0">₹299<span style="font-size:0.7rem;font-weight:400;color:#6060a0">/mo</span></div>
        <div style="font-size:0.7rem;color:#5a5a90">Unlimited · 11 languages</div>
      </div>
      <div style="background:#13131f;border:2px solid rgba(139,92,246,0.4);border-radius:12px;padding:10px 14px">
        <div style="font-size:0.7rem;font-weight:700;color:#8b5cf6;letter-spacing:1px;text-transform:uppercase">Ultra</div>
        <div style="font-size:1.3rem;font-weight:900;color:#ececff;margin:2px 0">₹599<span style="font-size:0.7rem;font-weight:400;color:#6060a0">/mo</span></div>
        <div style="font-size:0.7rem;color:#5a5a90">All features unlocked</div>
      </div>
      <div style="background:#13131f;border:1.5px solid #1e1e35;border-radius:12px;padding:10px 14px">
        <div style="font-size:0.7rem;font-weight:700;color:#3a3a55;letter-spacing:1px;text-transform:uppercase">Guest</div>
        <div style="font-size:1.3rem;font-weight:900;color:#3a3a55;margin:2px 0">Free</div>
        <div style="font-size:0.7rem;color:#2a2a40">No account needed</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    p1, p2 = st.columns(2)
    with p1:
        sel_basic = "✓ " if st.session_state.selected_plan == "Basic" else ""
        if st.button(f"{sel_basic}Basic — Free", key="pb"):
            st.session_state.selected_plan = "Basic"
            st.rerun()
    with p2:
        sel_pro = "✓ " if st.session_state.selected_plan == "Pro" else ""
        if st.button(f"{sel_pro}⭐ Pro — ₹299/mo", key="pp"):
            st.session_state.selected_plan = "Pro"
            st.rerun()
    p3, p4 = st.columns(2)
    with p3:
        sel_ultra = "✓ " if st.session_state.selected_plan == "Ultra" else ""
        if st.button(f"{sel_ultra}💎 Ultra — ₹599/mo", key="pu"):
            st.session_state.selected_plan = "Ultra"
            st.rerun()
    with p4:
        st.markdown('<div style="background:#13131f;border:1.5px solid #1e1e35;border-radius:10px;padding:8px 12px;font-size:0.75rem;color:#3a3a55;text-align:center">Guest mode<br>No account needed</div>', unsafe_allow_html=True)

    plan_tag_colors = {"Basic": "#06b6d4", "Pro": "#ec4899", "Ultra": "#8b5cf6"}
    tag_color = plan_tag_colors.get(st.session_state.selected_plan, "#ec4899")
    plan_suffix = {"Basic": "— Free", "Pro": "— ₹299/mo", "Ultra": "— ₹599/mo"}.get(st.session_state.selected_plan, "")
    st.markdown(f'<p style="font-size:0.75rem;color:{tag_color};margin:6px 0 12px;font-weight:600">Selected: {st.session_state.selected_plan} {plan_suffix}</p>', unsafe_allow_html=True)

    btn_label = "✨  Create Account — Free" if st.session_state.selected_plan == "Basic" else f"💳  Continue to Payment"
    if st.button(btn_label, key="signup_btn", use_container_width=True):
        if not s_user or not s_pass or not s_pass2:
            st.error("Please fill in all fields.")
        elif not validate_username(s_user):
            st.error("Username: 3–20 characters, letters, numbers, or _ only.")
        elif not validate_password(s_pass):
            st.error("Password must be at least 6 characters.")
        elif s_pass != s_pass2:
            st.error("Passwords do not match.")
        else:
            users = load_users()
            if s_user in users:
                st.error("❌ Username already taken. Try another.")
            elif st.session_state.selected_plan == "Basic":
                # Free plan — create account and go straight to chat
                users[s_user] = {"password": hash_pw(s_pass), "plan": "Basic"}
                save_users(users)
                st.session_state.logged_in = True
                st.session_state.username  = s_user
                st.session_state.plan      = "Basic"
                st.success(f"🎉 Account created! Welcome, {s_user}!")
                st.switch_page("pages/chat.py")
            else:
                # Pro / Ultra — go to payment page
                st.session_state.pending_user    = s_user
                st.session_state.pending_pw_hash = hash_pw(s_pass)
                st.session_state.pending_plan    = st.session_state.selected_plan
                st.switch_page("pages/payment.py")

st.markdown("</div>", unsafe_allow_html=True)