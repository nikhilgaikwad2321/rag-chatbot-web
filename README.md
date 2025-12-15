# 🌐 RAG-Based Website Chatbot

## 📌 Project Overview

This project implements a **Retrieval-Augmented Generation (RAG) based chatbot** that enables users to ask natural-language questions about the content of **any public website URL**.

The system automatically crawls a website, builds a structured knowledge base from its content, and generates **accurate, context-grounded answers** using semantic retrieval combined with a Large Language Model (LLM).

The solution is designed to be:
- Accurate (answers grounded in website content)
- Explainable (retrieved chunks are visible)
- Cost-effective (uses a free AI model)
- Deployable (Streamlit Cloud ready)

---

## 🎯 Problem Statement

**Input:** Public website URL + User questions  
**Process:** Crawl → Clean → Chunk → Embed → Retrieve → Generate  
**Output:** A chatbot that answers questions strictly based on website content

---

## 🧠 System Architecture

```
User
 │
 ▼
Streamlit UI
 │
 ▼
URL Validation
 │
 ▼
Website Crawler
 │
 ▼
Text Cleaning & Chunking
 │
 ▼
TF-IDF Embeddings
 │
 ▼
Vector Store (Cosine Similarity)
 │
 ▼
LLM (Gemini Flash Lite)
 │
 ▼
Final Answer
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|------|-----------|
| Language | Python |
| UI | Streamlit |
| Crawling | Requests, BeautifulSoup |
| Embeddings | TF-IDF |
| Vector Search | Cosine Similarity |
| LLM | Gemini Flash Lite |
| Deployment | Render |

---

## 🧪 Example Queries

- What is this website about?
- What services are offered?
- Who is the target audience?
- Summarize the website content.

---

## ⚠️ Limitations

- JavaScript-heavy websites are not fully supported
- Crawl depth is limited
- In-memory vector storage only
- Free model rate limits

---

## 🚀 Future Enhancements

- Persistent vector database
- JavaScript rendering support
- PDF ingestion
- Multi-language support
- Hybrid search
- Answer citations

---

## 🌐 Deployment

Deployed using Render
