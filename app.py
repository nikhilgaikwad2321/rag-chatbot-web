

import streamlit as st
import re
import requests

from crawler import crawl_website
from preprocess import prepare_chunks
from embeddings import generate_embeddings, embed_query
from vector_store import VectorStore
from rag import generate_answer

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="RAG Website Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- URL VALIDATION ----------------
def is_valid_url(url: str):
    regex = re.compile(
        r'^(https?:\/\/)'
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,})'
        r'(\/.*)?$'
    )
    if not re.match(regex, url):
        return False, "Invalid URL format. Please include http:// or https://"

    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        if response.status_code >= 400:
            return False, "Website is not reachable (4xx/5xx error)."
    except requests.exceptions.Timeout:
        return False, "Website timed out. Please try another URL."
    except requests.exceptions.RequestException:
        return False, "Unable to connect to the website."

    return True, ""

# ---------------- ADVANCED CSS + ANIMATIONS ----------------
# ---------------- CUSTOM CSS FOR DISTINCT UI ----------------
st.markdown("""
<style>
body {
    background: #f3f4f6;  /* light gray background for contrast */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* HEADER */
.center-title {
    font-size: 48px;
    font-weight: 900;
    text-align: center;
    color: #1f2937;
    background: linear-gradient(90deg, #f97316, #3b82f6, #10b981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}
.subtitle {
    text-align: center;
    color: #374151;
    font-size: 20px;
    margin-bottom: 30px;
}

/* MAIN CARD CONTAINERS */
.card {
    background: white;
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.1);
}

/* METRIC CARDS */
.metric {
    font-size: 28px;
    font-weight: 700;
    color: #ef4444; /* red-ish for differentiation */
}

/* CHAT BUBBLES */
.user {
    background: #3b82f6;
    color: white;
    padding: 15px;
    border-radius: 20px 20px 0px 20px;
    max-width: 70%;
    margin-left: auto;
    margin-bottom: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.bot {
    background: #f9fafb;
    color: #111827;
    padding: 15px;
    border-radius: 20px 20px 20px 0px;
    max-width: 70%;
    margin-right: auto;
    margin-bottom: 12px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

/* CHAT CONTAINER */
.chat-container {
    max-height: 450px;
    overflow-y: auto;
    padding: 20px;
    background: #e0f2fe; /* light blue background for chat */
    border-radius: 25px;
    margin-bottom: 20px;
}

/* BUTTON */
.stButton > button {
    border-radius: 12px;
    font-weight: bold;
    transition: all 0.3s ease-in-out;
    background: linear-gradient(90deg, #f97316, #3b82f6);
    color: white;
}
.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 12px rgba(0,0,0,0.2);
}

/* INPUT BOX */
input[type="text"] {
    border-radius: 15px;
    border: 1px solid #9ca3af;
    padding: 12px;
}

/* EXPANDER STYLE */
.stExpander {
    background: #fef3c7;
    border-radius: 15px;
    padding: 10px;
    margin-bottom: 10px;
}

/* TOAST / ALERTS */
#toplobcomp, #toplobcomp2, #leadtoast, #leadtoastpdp, #leadtoastpdp2 {
    border-radius: 12px;
    padding: 12px;
    background: #f87171;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- WRAPPER FOR CHAT ----------------
st.markdown("""

    <div class="chat-container">
    <!-- Existing chat will render inside here -->
    </div>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='center-title'>🤖 RAG Website Chatbot</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ask intelligent questions about any website using AI-powered retrieval</div>", unsafe_allow_html=True)

st.markdown(
    ""
    "👋 <b>Welcome!</b><br>"
    "Enter a website URL, build a knowledge base, and start asking questions. "
    "Answers are generated strictly from website content."
    ,
    unsafe_allow_html=True
)

st.divider()

# ---------------- SESSION STATE ----------------
for key in ["vector_store", "pages", "chunks", "stats", "history"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key in ["pages", "chunks", "history"] else None

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🧭 User Guide")
    st.markdown("""
    **1️⃣ Enter Website URL**  
    **2️⃣ Build Knowledge Base**  
    **3️⃣ Ask Questions**  
    """)

# ---------------- STEP 1 ----------------
st.markdown("### 🔹 Step 1: Enter Website URL")
url = st.text_input("", placeholder="https://example.com")

# ---------------- STEP 2 ----------------
st.markdown("### 🔹 Step 2: Build Knowledge Base")

if st.button("🚀 Crawl Website & Build Knowledge Base", use_container_width=True):
    if not url:
        st.error("❌ Please enter a website URL.")
    else:
        valid, error_msg = is_valid_url(url)
        if not valid:
            st.error(f"❌ {error_msg}")
        else:
            st.success("✅ URL validated successfully!")

            try:
                with st.spinner("🔍 Crawling website..."):
                    pages = crawl_website(url)

                if not pages:
                    st.error("❌ No readable content found on this website.")
                    st.stop()

                with st.spinner("🧹 Processing content..."):
                    chunks = prepare_chunks(pages)

                with st.spinner("🧠 Creating embeddings..."):
                    texts = [c["text"] for c in chunks]
                    embeddings = generate_embeddings(texts)
                    vs = VectorStore(len(embeddings[0]))
                    vs.add(embeddings, chunks)

                st.session_state.vector_store = vs
                st.session_state.pages = pages
                st.session_state.chunks = chunks
                st.session_state.stats = {
                    "Pages Crawled": len(pages),
                    "Chunks Created": len(chunks),
                    "Embedding Dimension": len(embeddings[0])
                }

                st.success("✅ Knowledge Base Ready")

            except Exception:
                st.error("❌ Failed to crawl the website. The site may block bots or be unavailable.")

# ---------------- DASHBOARD ----------------
if st.session_state.vector_store:
    st.markdown("### 📊 Knowledge Base Overview")
    cols = st.columns(len(st.session_state.stats))
    for col, (k, v) in zip(cols, st.session_state.stats.items()):
        col.markdown(
            f"<div style='color:#9ca3af'>{k}</div><div class='metric'>{v}</div>",
            unsafe_allow_html=True
        )

st.divider()

# ---------------- STEP 3 ----------------
st.markdown("### 💬 Ask a Question")
question = st.text_input("", placeholder="What is this website about?")

if st.button("Ask Question", use_container_width=True):
    if not st.session_state.vector_store:
        st.warning("Please build the knowledge base first.")
    elif not question:
        st.warning("Please enter a question.")
    else:
        q_emb = embed_query(question)
        top_chunks = st.session_state.vector_store.search(q_emb, k=5)
        answer = generate_answer(question, top_chunks)

        st.session_state.history.append({
            "question": question,
            "answer": answer,
            "chunks": top_chunks
        })

# ---------------- CHAT HISTORY ----------------
for item in reversed(st.session_state.history):
    st.markdown(f"<div class='user'><b>You:</b> {item['question']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='bot'><b>Answer:</b><br>{item['answer']}</div>", unsafe_allow_html=True)

    with st.expander("🔍 View Retrieval Details"):
        for i, ch in enumerate(item["chunks"], 1):
            st.markdown(f"**Rank {i} | Source:** `{ch['source']}`")
            st.write(ch["text"][:400] + "...")

st.caption("⚡ Powered by a transparent Retrieval-Augmented Generation (RAG) architecture")

