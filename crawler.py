import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def is_valid_url(url, base_domain):
    parsed = urlparse(url)
    return parsed.netloc == base_domain and parsed.scheme in ["http", "https"]

def extract_text(soup):
    for tag in soup(["script", "style", "noscript", "img"]):
        tag.decompose()
    return " ".join(soup.stripped_strings)

def crawl_website(start_url, max_depth=2, max_pages=30):
    visited = set()
    results = []

    base_domain = urlparse(start_url).netloc

    def crawl(url, depth):
        if depth > max_depth or url in visited or len(visited) >= max_pages:
            return

        visited.add(url)

        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            if "text/html" not in response.headers.get("Content-Type", ""):
                return

            soup = BeautifulSoup(response.text, "lxml")

            title = soup.title.string if soup.title else ""
            text = extract_text(soup)

            results.append({
                "url": url,
                "title": title,
                "content": text
            })

            links = soup.find_all("a", href=True)
            for link in links:
                next_url = urljoin(url, link["href"])
                if is_valid_url(next_url, base_domain):
                    crawl(next_url, depth + 1)

        except Exception:
            pass

    crawl(start_url, 0)
    return results
