import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-lite-latest")

def generate_answer(question, context_chunks):
    if not context_chunks:
        return "No relevant information found from the website."

    context = "\n\n".join(
        [chunk["text"][:800] for chunk in context_chunks]
    )

    prompt = f"""
You are an AI assistant answering questions using ONLY the content below.

Content:
{context}

Question:
{question}

Provide a helpful, summarized answer based strictly on the content.
"""

    response = model.generate_content(prompt)
    return response.text.strip()
