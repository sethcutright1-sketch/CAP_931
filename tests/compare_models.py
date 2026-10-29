import time
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src/cap_931"))
from web_research import fetch_page_text
from prompts import build_summary_prompt, build_sections_prompt, system_prompt
from research_chain import build_summaries_block
from llm_client import ask_llm, usage_log

# SETTINGS
MODELS        = ["claude-haiku-5-5", "claude-sonnet-5-5"]
RUNS_PER_MODEL = 1
PRODUCT_NAME = "Hestia"
COMPANY_URLS  = ["https://corporate.bestbuy.com/executive-team/", "https://corporate.bestbuy.com/about-best-buy/"]
COMPETITORS   = ["https://store.google.com/", "https://www.samsung.com/us/smart-home/"]
COMPANY   = "Best Buy"
CUSTOMER_ROLE = "VP of Product, Digital Experience"
CATEGORY = "Household organization and smart-home software"
VALUE_PROPOSITION = "Hestia is a subscription-based household organizer that adds ongoing value for customers using their new or existing smart-home hardware through private, connected planning and management tools."
PRICES = {
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-sonnet-5-5": (2.00, 10.00),
}

pages = {}
for url in COMPANY_URLS + COMPETITORS:
    pages[url] = fetch_page_text(url)

def run_once(step1_model, step2_model):
    usage_log.clear()
    start = time.perf_counter()
    results = []
    for url, text in pages.items():
        if text.startswith("Failed") or text.startswith("Request failed") or text.startswith("Page loaded but has no readable text"):
            results.append((url, "SOURCE UNAVAILABLE: " + text))
        else:
            summary = ask_llm(build_summary_prompt(url=url, page_text=text, competitors=COMPETITORS, product_name=PRODUCT_NAME), model=step1_model, system=system_prompt)
            results.append((url, summary))
    block = build_summaries_block(results, COMPETITORS)
    prompt = build_sections_prompt(company=COMPANY, customer_role=CUSTOMER_ROLE, category=CATEGORY,
            value_proposition=VALUE_PROPOSITION, competitors=COMPETITORS, summaries_block=block, product_name=PRODUCT_NAME)
    brief = ask_llm(prompt, model=step2_model, system=system_prompt)
    seconds = time.perf_counter() - start
    return brief, seconds, list(usage_log)

def cost(usage):
    total = 0
    for call in usage:
        input_price, output_price = PRICES[call["model"]]
        total += (call["input_tokens"] * input_price + call["output_tokens"] * output_price) / 1_000_000
    return total

def check_brief(brief):
    main_part = brief.split("## Article Links")[0]
    lines = main_part.split("\n")
    bullets = [line for line in lines if line.strip().startswith(("- ", "* "))]
    unsourced = [line for line in bullets if "(Source:" not in line]
    return {"bullets": len(bullets), "unsourced": len(unsourced)}

if __name__ == "__main__":
    CONFIGS = {
        "haiku":  ("claude-haiku-5-5", "claude-haiku-5-5"),
        "sonnet": ("claude-sonnet-5-5", "claude-sonnet-5-5"),
        "hybrid": ("claude-haiku-5-5", "claude-sonnet-5-5"),
    }
    TO_RUN = ["haiku", "sonnet", "hybrid"]

    calls_per_run = len(pages) + 1
    total_calls = calls_per_run * RUNS_PER_MODEL * len(TO_RUN)
    print(f"This will make up to {total_calls} model calls.")
    answer = input("Type yes to continue: ")
    if answer != "yes":
        print("Cancelled.")
        raise SystemExit
    print("Running...")
    table = []
    for name in TO_RUN:
        step1_model, step2_model = CONFIGS[name]
        for i in range(RUNS_PER_MODEL):
            brief, seconds, usage = run_once(step1_model, step2_model)
            stats = check_brief(brief)
            dollars = cost(usage)
            print(f"{name} run {i + 1}: {seconds:.1f}s, ${dollars:.4f}, "
                  f"{stats['bullets']} bullets, {stats['unsourced']} unsourced")
            table.append((name, seconds, dollars, stats["bullets"], stats["unsourced"]))
            with open(f"tests/brief_{name}_{i + 1}.md", "w", encoding="utf-8") as f:
                f.write(brief)