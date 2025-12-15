# import streamlit as st
# from crawler import crawl_website
# from preprocess import prepare_chunks
# from embeddings import generate_embeddings, embed_query
# from vector_store import VectorStore
# from rag import generate_answer

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(
#     page_title="RAG Website Chatbot",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ---------------- ADVANCED CSS + ANIMATIONS ----------------
# st.markdown("""
# <style>

# /* BACKGROUND */
# body {
#     background: linear-gradient(135deg, #020617, #0f172a);
# }

# /* CENTERED HEADER */
# .center-title {
#     text-align: center;
#     font-size: 46px;
#     font-weight: 900;
#     background: linear-gradient(90deg, #22c55e, #38bdf8, #a855f7);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     animation: fadeIn 1.2s ease-in-out;
# }

# .subtitle {
#     text-align: center;
#     color: #cbd5f5;
#     font-size: 18px;
#     margin-bottom: 20px;
#     animation: fadeIn 1.6s ease-in-out;
# }

# /* FADE IN */
# @keyframes fadeIn {
#     from { opacity: 0; transform: translateY(12px); }
#     to { opacity: 1; transform: translateY(0); }
# }

# /* CARD */
# .card {
#     background: rgba(17, 24, 39, 0.85);
#     padding: 18px;
#     border-radius: 16px;
#     border: 1px solid rgba(255,255,255,0.08);
#     animation: fadeIn 0.8s ease-in-out;
# }

# /* METRIC */
# .metric {
#     font-size: 30px;
#     font-weight: 800;
#     color: #22c55e;
# }

# /* CHAT BUBBLES */
# .user {
#     background: linear-gradient(135deg, #2563eb, #1d4ed8);
#     color: white;
#     padding: 14px;
#     border-radius: 18px;
#     margin-bottom: 10px;
#     animation: fadeIn 0.5s ease-in-out;
# }

# .bot {
#     background: #020617;
#     padding: 14px;
#     border-radius: 18px;
#     border: 1px solid #1e293b;
#     animation: fadeIn 0.7s ease-in-out;
# }

# /* BUTTON HOVER */
# .stButton > button {
#     border-radius: 12px;
#     transition: all 0.3s ease-in-out;
# }

# .stButton > button:hover {
#     transform: scale(1.03);
# }

# </style>
# """, unsafe_allow_html=True)

# # ---------------- HEADER ----------------
# st.markdown("<div class='center-title'>🤖 RAG Website Chatbot</div>", unsafe_allow_html=True)
# st.markdown("<div class='subtitle'>Ask intelligent questions about any website using AI-powered retrieval</div>", unsafe_allow_html=True)

# st.markdown(
#     "<div class='card'>"
#     "👋 <b>Welcome!</b><br>"
#     "Enter a website URL, build a knowledge base, and start asking questions. "
#     "All answers are generated using retrieved website content for accuracy."
#     "</div>",
#     unsafe_allow_html=True
# )

# st.divider()

# # ---------------- SESSION STATE ----------------
# for key in ["vector_store", "pages", "chunks", "stats", "history"]:
#     if key not in st.session_state:
#         st.session_state[key] = [] if key in ["pages", "chunks", "history"] else None

# # ---------------- SIDEBAR ----------------
# with st.sidebar:
#     st.markdown("## 🧭 User Guide")
#     st.markdown("""
#     **1️⃣ Enter Website URL**  
#     **2️⃣ Build Knowledge Base**  
#     **3️⃣ Ask Questions**  

#     🔹 Designed for smooth and intuitive usage  
#     🔹 Powered by a Retrieval-Augmented Generation pipeline  
#     """)

# # ---------------- STEP 1 ----------------
# st.markdown("### 🔹 Step 1: Enter Website URL")
# url = st.text_input("", placeholder="https://example.com")

# # ---------------- STEP 2 ----------------
# st.markdown("### 🔹 Step 2: Build Knowledge Base")

# if st.button("🚀 Crawl Website & Build Knowledge Base", use_container_width=True):
#     if not url:
#         st.warning("Please enter a valid website URL.")
#     else:
#         with st.spinner("🔍 Crawling website..."):
#             pages = crawl_website(url)
#             st.session_state.pages = pages

#         with st.spinner("🧹 Processing content..."):
#             chunks = prepare_chunks(pages)
#             st.session_state.chunks = chunks

#         with st.spinner("🧠 Creating embeddings..."):
#             texts = [c["text"] for c in chunks]
#             embeddings = generate_embeddings(texts)
#             vs = VectorStore(len(embeddings[0]))
#             vs.add(embeddings, chunks)
#             st.session_state.vector_store = vs

#         st.session_state.stats = {
#             "Pages Crawled": len(pages),
#             "Chunks Created": len(chunks),
#             "Embedding Dimension": len(embeddings[0]),
#         }

#         st.success("✅ Knowledge Base Ready")

# # ---------------- DASHBOARD ----------------
# if st.session_state.vector_store:
#     st.markdown("### 📊 Knowledge Base Overview")
#     cols = st.columns(len(st.session_state.stats))
#     for col, (k, v) in zip(cols, st.session_state.stats.items()):
#         col.markdown(
#             f"<div class='card'><div style='color:#9ca3af'>{k}</div><div class='metric'>{v}</div></div>",
#             unsafe_allow_html=True
#         )

# st.divider()

# # ---------------- STEP 3 ----------------
# st.markdown("### 💬 Ask a Question")
# question = st.text_input("", placeholder="What is this website about?")

# if st.button("Ask Question", use_container_width=True):
#     if not st.session_state.vector_store:
#         st.warning("Please build the knowledge base first.")
#     elif not question:
#         st.warning("Please enter a question.")
#     else:
#         q_emb = embed_query(question)
#         top_chunks = st.session_state.vector_store.search(q_emb, k=5)
#         answer = generate_answer(question, top_chunks)

#         st.session_state.history.append({
#             "question": question,
#             "answer": answer,
#             "chunks": top_chunks
#         })

# # ---------------- CHAT HISTORY ----------------
# for item in reversed(st.session_state.history):
#     st.markdown(f"<div class='user'><b>You:</b> {item['question']}</div>", unsafe_allow_html=True)
#     st.markdown(f"<div class='bot'><b>Answer:</b><br>{item['answer']}</div>", unsafe_allow_html=True)

#     with st.expander("🔍 View Retrieval Details"):
#         for i, ch in enumerate(item["chunks"], 1):
#             st.markdown(f"**Rank {i} | Source:** `{ch['source']}`")
#             st.write(ch["text"][:400] + "...")

# st.caption(
#     "⚡ Powered by a transparent Retrieval-Augmented Generation (RAG) architecture"
# )

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
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #020617, #0f172a);
}
.center-title {
    text-align: center;
    font-size: 46px;
    font-weight: 900;
    background: linear-gradient(90deg, #22c55e, #38bdf8, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fadeIn 1.2s ease-in-out;
}
.subtitle {
    text-align: center;
    color: #cbd5f5;
    font-size: 18px;
    margin-bottom: 20px;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
.card {
    background: rgba(17, 24, 39, 0.85);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
}
.metric {
    font-size: 30px;
    font-weight: 800;
    color: #22c55e;
}
.user {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    padding: 14px;
    border-radius: 18px;
    margin-bottom: 10px;
}
.bot {
    background: #020617;
    padding: 14px;
    border-radius: 18px;
    border: 1px solid #1e293b;
}
.stButton > button {
    border-radius: 12px;
    transition: all 0.3s ease-in-out;
}
.stButton > button:hover {
    transform: scale(1.03);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='center-title'>🤖 RAG Website Chatbot</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ask intelligent questions about any website using AI-powered retrieval</div>", unsafe_allow_html=True)

st.markdown(
    "<div class='card'>"
    "👋 <b>Welcome!</b><br>"
    "Enter a website URL, build a knowledge base, and start asking questions. "
    "Answers are generated strictly from website content."
    "</div>",
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
            f"<div class='card'><div style='color:#9ca3af'>{k}</div><div class='metric'>{v}</div></div>",
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

