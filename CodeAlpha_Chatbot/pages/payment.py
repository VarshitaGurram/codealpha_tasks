import streamlit as st
import json, os, time

st.set_page_config(page_title="TechBot — Payment", page_icon="💳",
                   layout="centered", initial_sidebar_state="collapsed")

# ── Guard: must come from signup flow ─────────────────────────────────────────
for k, v in [("pending_user", ""), ("pending_pw_hash", ""), ("pending_plan", ""),
             ("logged_in", False), ("username", ""), ("plan", ""), ("guest", False),
             ("pay_step", "form")]:
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state.pending_user:
    st.switch_page("pages/login.py")

PLAN      = st.session_state.pending_plan
USERNAME  = st.session_state.pending_user
PRICES    = {"Pro": "₹299", "Ultra": "₹599"}
PRICE_INT = {"Pro": 299,    "Ultra": 599}
COLORS    = {"Pro": "#ec4899", "Ultra": "#8b5cf6"}
ICONS     = {"Pro": "⭐", "Ultra": "💎"}

PLAN_COLOR = COLORS.get(PLAN, "#ec4899")
PLAN_ICON  = ICONS.get(PLAN, "⭐")
PRICE_STR  = PRICES.get(PLAN, "₹299")

USERS_FILE = "users.json"
def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f: json.dump({}, f)
    with open(USERS_FILE) as f: return json.load(f)
def save_users(data):
    with open(USERS_FILE, "w") as f: json.dump(data, f, indent=2)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500&display=swap');
html,body,.stApp,[class*="css"]{{font-family:'Plus Jakarta Sans',sans-serif !important;background-color:#060610 !important;color:#ececff !important;}}
#MainMenu,footer,header,section[data-testid="stSidebar"]{{display:none !important;}}
.block-container{{padding:2rem 1rem 4rem !important;max-width:520px !important;}}

.pay-card{{background:#0d0d1a;border:1px solid #1a1a2e;border-radius:20px;padding:2.2rem 2rem;}}
.pay-header{{text-align:center;margin-bottom:1.8rem;}}
.pay-icon{{font-size:2.4rem;margin-bottom:0.4rem;}}
.pay-title{{font-size:1.4rem;font-weight:900;background:linear-gradient(135deg,#f97316,#ec4899,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}}
.pay-sub{{font-size:0.8rem;color:#6060a0;margin-top:0.2rem;}}

.order-box{{background:#13131f;border:1px solid #1e1e35;border-radius:14px;padding:1.2rem 1.4rem;margin-bottom:1.5rem;}}
.order-row{{display:flex;justify-content:space-between;align-items:center;padding:5px 0;}}
.order-label{{font-size:0.82rem;color:#6060a0;}}
.order-value{{font-size:0.88rem;font-weight:700;color:#ececff;}}
.order-total{{border-top:1px solid #1e1e35;margin-top:8px;padding-top:10px;}}
.order-total .order-label{{font-size:0.88rem;font-weight:700;color:#ececff;}}
.order-total .order-value{{font-size:1.3rem;font-weight:900;color:{PLAN_COLOR};}}

.plan-pill{{display:inline-block;background:{PLAN_COLOR}22;border:1px solid {PLAN_COLOR}55;border-radius:20px;padding:3px 14px;font-size:0.65rem;font-weight:700;color:{PLAN_COLOR};letter-spacing:1px;text-transform:uppercase;}}

.section-label{{font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#6060a0;margin:1.2rem 0 0.6rem;}}

.card-input-wrap{{position:relative;margin-bottom:0.8rem;}}
.card-icon{{position:absolute;right:12px;top:50%;transform:translateY(-50%);font-size:1rem;pointer-events:none;}}

input[type="text"],input[type="password"],input[type="number"],
.stTextInput input{{
    background-color:#13131f !important;color:#ececff !important;
    border:1.5px solid #1e1e35 !important;border-radius:10px !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;font-size:0.92rem !important;
    padding:10px 14px !important;
}}
input:focus,.stTextInput input:focus{{border-color:{PLAN_COLOR} !important;box-shadow:0 0 0 3px {PLAN_COLOR}22 !important;outline:none !important;}}
.stTextInput label{{font-size:0.72rem !important;font-weight:600 !important;color:#8888aa !important;letter-spacing:0.5px !important;}}
.stTextInput>div>div{{background:transparent !important;}}

.stButton>button{{background:linear-gradient(135deg,#f97316,#ec4899) !important;color:white !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;font-weight:700 !important;font-size:0.92rem !important;
    border:none !important;border-radius:10px !important;padding:0.65rem 1rem !important;width:100% !important;
    transition:all 0.18s !important;box-shadow:0 4px 18px rgba(236,72,153,0.28) !important;}}
.stButton>button:hover{{opacity:0.88 !important;transform:translateY(-1px) !important;}}

.back-link{{font-size:0.75rem;color:#6060a0;cursor:pointer;margin-bottom:1.2rem;display:inline-flex;align-items:center;gap:5px;}}
.back-link:hover{{color:#ec4899;}}

.secure-badge{{display:flex;align-items:center;justify-content:center;gap:6px;font-size:0.7rem;color:#3a3a55;margin-top:1rem;}}

.success-wrap{{text-align:center;padding:2rem 1rem;}}
.success-icon{{font-size:3.5rem;margin-bottom:1rem;}}
.success-title{{font-size:1.4rem;font-weight:900;margin-bottom:0.4rem;}}
.success-sub{{font-size:0.85rem;color:#6060a0;line-height:1.6;}}
</style>
""", unsafe_allow_html=True)

# ── Back button ───────────────────────────────────────────────────────────────
if st.button("← Back to Signup", key="back"):
    st.switch_page("pages/login.py")

# ════════════════════════════════════════════════════════════════════════════
# SUCCESS SCREEN
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.pay_step == "success":
    st.markdown(f"""
    <div class="pay-card">
      <div class="success-wrap">
        <div class="success-icon">🎉</div>
        <div class="success-title">Payment Successful!</div>
        <div class="success-sub">
          Welcome to <b style="color:{PLAN_COLOR}">{PLAN_ICON} TechBot {PLAN}</b>, <b>{USERNAME}</b>!<br><br>
          Your account is active. Enjoy unlimited access to all {PLAN} features.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    if st.button("🚀  Go to TechBot", key="go_chat", use_container_width=True):
        st.switch_page("pages/chat.py")
    st.stop()

# ════════════════════════════════════════════════════════════════════════════
# PAYMENT FORM
# ════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="pay-card">
  <div class="pay-header">
    <div class="pay-icon">💳</div>
    <div class="pay-title">Complete Your Order</div>
    <div class="pay-sub">You're subscribing to <span class="plan-pill">{PLAN_ICON} {PLAN}</span></div>
  </div>

  <div class="order-box">
    <div class="order-row">
      <span class="order-label">Plan</span>
      <span class="order-value">{PLAN_ICON} TechBot {PLAN}</span>
    </div>
    <div class="order-row">
      <span class="order-label">Billing</span>
      <span class="order-value">Monthly</span>
    </div>
    <div class="order-row">
      <span class="order-label">Features</span>
      <span class="order-value">{"Unlimited · 11 langs · TTS · Export" if PLAN == "Pro" else "All Pro features + Early Access"}</span>
    </div>
    <div class="order-row order-total">
      <span class="order-label">Total due today</span>
      <span class="order-value">{PRICE_STR}</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── Card details form ─────────────────────────────────────────────────────
st.markdown('<p class="section-label">💳 Card Details</p>', unsafe_allow_html=True)

card_name = st.text_input("Name on Card", placeholder="John Doe", key="card_name")
card_num  = st.text_input("Card Number", placeholder="1234  5678  9012  3456", max_chars=19, key="card_num")

col1, col2 = st.columns(2)
with col1:
    expiry = st.text_input("Expiry Date", placeholder="MM / YY", max_chars=7, key="expiry")
with col2:
    cvv = st.text_input("CVV", placeholder="•••", max_chars=4, type="password", key="cvv")

st.markdown('<p class="section-label" style="margin-top:1.2rem">🏠 Billing Info</p>', unsafe_allow_html=True)

billing_email = st.text_input("Email Address", placeholder="you@example.com", key="billing_email")
billing_phone = st.text_input("Phone Number", placeholder="+91 98765 43210", key="billing_phone")

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# ── Pay button ────────────────────────────────────────────────────────────
if st.button(f"💳  Pay {PRICE_STR} & Activate {PLAN}", key="pay_btn", use_container_width=True):
    # Validation
    err = None
    clean_num = card_num.replace(" ", "").replace("-", "")
    if not card_name.strip():
        err = "Please enter the name on your card."
    elif not clean_num.isdigit() or len(clean_num) not in (15, 16):
        err = "Please enter a valid 15 or 16-digit card number."
    elif not expiry.strip() or "/" not in expiry:
        err = "Please enter a valid expiry date (MM / YY)."
    elif not cvv.strip() or not cvv.strip().isdigit() or len(cvv.strip()) < 3:
        err = "Please enter a valid CVV."
    elif not billing_email.strip() or "@" not in billing_email:
        err = "Please enter a valid email address."
    elif not billing_phone.strip():
        err = "Please enter your phone number."

    if err:
        st.error(f"⚠️ {err}")
    else:
        # Simulate payment processing
        with st.spinner("🔒 Processing payment securely..."):
            time.sleep(2)

        # Save account to users.json
        users = load_users()
        users[USERNAME] = {
            "password": st.session_state.pending_pw_hash,
            "plan": PLAN
        }
        save_users(users)

        # Activate session
        st.session_state.logged_in      = True
        st.session_state.username       = USERNAME
        st.session_state.plan           = PLAN
        st.session_state.pending_user   = ""
        st.session_state.pending_pw_hash = ""
        st.session_state.pending_plan   = ""
        st.session_state.pay_step       = "success"
        st.rerun()

st.markdown("""
<div class="secure-badge">🔒 256-bit SSL encrypted &nbsp;·&nbsp; Your card data is never stored</div>
""", unsafe_allow_html=True)