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

if __name__ == "__main__":
    fake_results = [
        ("https://corporate.bestbuy.com/executive-team/",
         "- [Strategy] Four priorities: advance as a retail, media and advertising, and technology company; expand and grow reach; elevate the customer experience; and be a human-powered, customer-focused company.\n"
         "- [Leadership] Jason Bonfig, incoming chief executive officer\n"
         "- [Leadership] Frank Bedo, chief strategy and growth officer"),
        ("https://corporate.bestbuy.com/about-best-buy/",
         "- [Strategy] Best Buy's stated purpose is \"to enrich lives through technology.\"\n"
         "- [Competitors] No relevant information on this page."),
        ("https://store.google.com/",
         "- [Product/Technology] Google Home app lets users control smart home devices from anywhere."),
        ("https://www.samsung.com/us/smart-home/",
         "- [Product/Technology] SmartThings app lets users connect, control and automate their smart home from one app."),
        ("https://corporate.bestbuy.com/careers/",
         "SOURCE UNAVAILABLE: Failed to fetch https://corporate.bestbuy.com/careers/: Received status code 404"),
    ]

    competitors = [
        "https://store.google.com/",
        "https://www.samsung.com/us/smart-home/"
    ]
    
    brief = build_report(
        results=fake_results,
        company="Best Buy",
        customer_role="VP of Product, Digital Experience",
        category="household organization and smart-home software",
        value_proposition="Hestia is a subscription-based household organizer that adds ongoing value for customers using their new or existing smart-home hardware through private, connected planning and management tools.",
        competitors=competitors,
    )
    print(brief)