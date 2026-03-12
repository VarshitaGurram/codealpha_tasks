# 🚀 CodeAlpha AI Internship — Python Projects

This repository contains two fully deployed AI-powered web applications built with **Python + Streamlit** as part of the **CodeAlpha AI Internship**.

---

## 📌 Projects at a Glance

| # | Project | Live Demo | Description |
|---|---|---|---|
| Task 2 | 🤖 TechBot — AI FAQ Chatbot | [Open App](https://codealphachatbot-dghxzbayvypgyr32slekrj.streamlit.app) | NLP-powered chatbot answering Tech & AI questions |
| Task 3 | 🌐 Language Translator | [Open App](https://codealphalanguagetranslator-4izttzry2fnid6yyvfd6bq.streamlit.app) | Multilingual text translator with 100+ languages |

---

## 📁 Repository Structure

```
codealpha-internship/
│
├── task2_techbot/
│   ├── app.py                  # Landing page
│   ├── requirements.txt
│   └── pages/
│       ├── login.py            # Login & signup
│       ├── chat.py             # Chatbot interface
│       └── payment.py          # Pro/Ultra payment
│
├── task3_translator/
│   ├── app.py                  # Main translator app
│   └── requirements.txt
│
└── README.md
```

---

---

# 🤖 Task 2 — TechBot: AI FAQ Chatbot

> **Live Demo** → https://codealphachatbot-dghxzbayvypgyr32slekrj.streamlit.app

TechBot is an AI-powered FAQ chatbot that answers questions about Artificial Intelligence, Machine Learning, Python, Data Science, Cloud Computing, and APIs — with typing animations, multilingual replies, text-to-speech, and a full user account system.

---

### ✨ Features

#### 🧠 AI & NLP
- **TF-IDF Cosine Similarity** via `scikit-learn` — accurate matching even with typos or short queries like `"what is ml"`
- **Query expansion** — abbreviations like `ml`, `nlp`, `llm`, `iot`, `gpu` are auto-expanded before matching
- **34 built-in FAQs** across 4 categories: 🧠 AI · 🐍 Python · 📊 Data Science · ☁️ Cloud

#### 💬 Chat Experience
- ⌨️ Word-by-word **typing animation** with blinking cursor
- 🔁 **Follow-up suggestions** — 3 related questions after every answer
- ⭐ **Save favourites** — bookmark answers, view in Saved tab
- 📤 **Export chat** — download as `.txt`
- 🔊 **Text-to-speech** — listen to answers via `gTTS`
- 🌙 **Dark / Light mode** toggle

#### 🔐 User Accounts
- SHA-256 hashed passwords, stored in `users.json` (auto-created on first run)
- Login, signup, or **Guest mode** (5 questions, no account needed)

---

### 💳 Plans & Pricing

| Plan | Price | Questions | Languages | Favourites | Export | TTS | Theme |
|---|---|---|---|---|---|---|---|
| **Guest** | Free | 5 / session | English | ✗ | ✗ | ✗ | ✗ |
| **Basic** | Free | 20 / session | English | Up to 5 | ✗ | ✗ | ✗ |
| **Pro** | ₹299 / mo | Unlimited | 11 | Unlimited | ✓ | ✓ | ✓ |
| **Ultra** | ₹599 / mo | Unlimited | 11 | Unlimited | ✓ | ✓ | ✓ |

> Payment is simulated — no real transaction is processed.

---

### 🌐 Supported Languages (Chat Replies)
`English · Hindi · Tamil · Telugu · French · Spanish · German · Japanese · Arabic · Korean · Chinese`

---

### 🗂️ Pages

| File | Role |
|---|---|
| `app.py` | Landing page — navbar, hero, features, pricing, how it works |
| `pages/login.py` | Login + signup with plan selection; Basic → chat, Pro/Ultra → payment |
| `pages/payment.py` | Order summary, card form, validation, simulated checkout |
| `pages/chat.py` | Chat tab, Saved tab, Export tab; plan limits enforced live |

---

### 📦 Requirements — Task 2

```
streamlit
scikit-learn
numpy
deep-translator
gTTS
```

---

### 🚀 Run Locally — Task 2

```bash
cd task2_techbot
pip install -r requirements.txt
streamlit run app.py
```

---

---

# 🌐 Task 1 — Language Translator

> **Live Demo** → https://codealphalanguagetranslator-4izttzry2fnid6yyvfd6bq.streamlit.app

A clean, fast multilingual text translator supporting 100+ languages, built with `deep-translator` and Streamlit.

---

### ✨ Features

- 🌍 Translate text across **100+ languages**
- ⚡ Instant translation powered by **Google Translate** via `deep-translator`
- 📋 One-click **copy to clipboard**
- 🔄 **Swap languages** button to reverse translation direction
- 🌙 Clean dark UI with custom styling

---

### 📦 Requirements — Task 1

```
streamlit
deep-translator
```

---

### 🚀 Run Locally — Task 1

```bash
cd task3_translator
pip install -r requirements.txt
streamlit run app.py
```

---

---

## 🧰 Tech Stack — Both Projects

| Layer | Technology |
|---|---|
| Frontend | Streamlit + custom CSS |
| NLP Matching | scikit-learn (TF-IDF + cosine similarity) |
| Translation | deep-translator (Google Translate) |
| Text-to-Speech | gTTS (Google TTS) |
| Auth | SHA-256 via Python `hashlib` |
| Hosting | Streamlit Community Cloud |

---

## 🔐 Security Notes

- Passwords hashed with **SHA-256** — never stored in plain text
- `users.json` is auto-created at runtime — excluded from version control via `.gitignore`
- Payment form is a **UI prototype** — no real gateway connected

---

## 📄 License

Open source — free for personal and educational use.
