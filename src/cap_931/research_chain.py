# imports
from web_research import fetch_page_text
from prompts import build_summary_prompt, build_sections_prompt
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

def build_report(results, company, customer_role, category, value_proposition, competitors):
    summaries_block = build_summaries_block(results, competitors)

    prompt = build_sections_prompt(company=company, customer_role=customer_role, category=category, value_proposition=value_proposition, competitors=competitors, summaries_block=summaries_block)
    return ask_llm(prompt)

def run_pipeline(company_urls, company, customer_role, category, value_proposition, competitors):
    allurls = company_urls + competitors
    results = summarize_sources(allurls, competitors)
    if all(summary.startswith("SOURCE UNAVAILABLE") for _, summary in results):
        return "All sources are unavailable."
    return build_report(results, company, customer_role, category, value_proposition, competitors)


if __name__ == "__main__":
    company_urls = [
        "https://corporate.bestbuy.com/executive-team/",
        "https://corporate.bestbuy.com/about-best-buy/",
    ]

    competitors = [
        "https://store.google.com/",
        "https://www.samsung.com/us/smart-home/"
    ]
    
    brief = run_pipeline(company_urls, "Best Buy", "VP of Product, Digital Experience", "household organization and smart-home software", "Hestia is a subscription-based household organizer that adds ongoing value for customers using their new or existing smart-home hardware through private, connected planning and management tools.", competitors)
    
    print(brief)