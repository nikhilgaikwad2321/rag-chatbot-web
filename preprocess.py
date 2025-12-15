def clean_text(text):
    return " ".join(text.split())

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks

def prepare_chunks(pages):
    all_chunks = []

    for page in pages:
        clean = clean_text(page["content"])
        chunks = chunk_text(clean)

        for chunk in chunks:
            all_chunks.append({
                "text": chunk,
                "source": page["url"]
            })

    return all_chunks
