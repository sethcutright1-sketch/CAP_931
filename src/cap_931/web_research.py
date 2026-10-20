import requests
from bs4 import BeautifulSoup


def fetch_page_text(url: str, max_chars: int = 6000) -> str:
    """
    Fetches the content of a URL and returns the cleaned text.
    Returns an error message if the request fails or the page content is insufficient.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    try:
        # Perform the request with a timeout and browser-like headers
        response = requests.get(url, timeout=30, headers=headers)
        
        # Check if the status code is 200
        if response.status_code != 200:
            return f"Failed to fetch {url}: Received status code {response.status_code}"

    except requests.exceptions.RequestException as e:
        # Catches timeouts, DNS errors, SSL errors, etc.
        return f"Request failed for {url}: {str(e)}"

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove non-content tags
    for tag in soup(["script", "style"]):
        tag.decompose()

    # Extract text with spacing and strip whitespace
    text = soup.get_text(" ", strip=True)

    trimmed_text = text[:max_chars]

    # Detect short/empty pages likely JavaScript-rendered
    if len(trimmed_text) < 200:
        return f"Page loaded but has no readable text (probably JavaScript-rendered) at {url}"
    return trimmed_text
if __name__ == "__main__":
    test_urls = [
        "corporate.bestbuy.com/executive-team/",
        "investors.bestbuy.com/",
        "jobs.bestbuy.com/bby?id=all_jobs",
        "not-a-url" 
    ]

    for url in test_urls:
        print(f"--- Testing: {url} ---")
        result = fetch_page_text(url)
        print(result)
        print("-" * 30)
