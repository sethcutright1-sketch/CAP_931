# imports
from web_research import fetch_page_text
from prompts import build_summary_prompt
from llm_client import ask_llm


def summarize_sources(urls, competitors):
    """Takes a list of URLs and the competitor URLs.
       Returns a list of (url, summary) pairs."""

    results = []

    for url in urls:
        page = fetch_page_text(url)

        if page.startswith(("Failed", "Request failed", "Page loaded but has no readable text")):
            results.append((url, "SOURCE UNAVAILABLE: " + page))
            continue

        prompt = build_summary_prompt(url, page, competitors)
        summary = ask_llm(prompt)
        results.append((url, summary))

    return results

def build_summaries_block(results, competitors):
    pieces = []
    for url, summary in results:
        if url in competitors:
            page_type = "competitor page"
        else:
            page_type = "company page"
        pieces.append(f"Source: {url} ({page_type})\nSummary: {summary}")
    return "\n-------------------------------------------\n".join(pieces)

if __name__ == "__main__":
    test_urls = [
        "https://corporate.bestbuy.com/executive-team/",
        "https://investors.bestbuy.com/",
        "https://corporate.bestbuy.com/careers/"  # Added the jobs page
    ]

    competitors = [
        "https://store.google.com/",
        "https://www.samsung.com/us/smart-home/"
    ]

    results = summarize_sources(test_urls, competitors)

    for url, summary in results:
        print(f"URL: {url}")
        print(f"SUMMARY: {summary}")
        print("-" * 30)

    summaries_block = build_summaries_block(results, competitors)
    print("\n" + "=" * 50)
    print("COMBINED SUMMARIES")
    print("=" * 50)
    print(summaries_block)
