import os

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-not-real")

from research_chain import build_summaries_block

COMPETITORS = ["https://c.com/"]
DIVIDER =  "\n-------------------------------------------\n"

def test_company_page_is_tagged():
    block = build_summaries_block([("https://a.com/", "A summary")], COMPETITORS)
    assert "(company page)" in block

def test_competitor_page_is_tagged():
    block = build_summaries_block([("https://c.com/", "C summary")], COMPETITORS)
    assert "(competitor page)" in block

def test_two_results_have_one_divider():
    results = [("https://a.com/", "A"), ("https://c.com/", "C")]
    block = build_summaries_block(results, COMPETITORS)
    assert block.count(DIVIDER) == 1

def test_single_result_has_no_divider():
    block = build_summaries_block([("https://a.com/", "A")], COMPETITORS)
    assert block.count(DIVIDER) == 0

def test_unavailable_source_is_kept():
    results = [("https://a.com/", "SOURCE UNAVAILABLE: Failed to fetch")]
    block = build_summaries_block(results, COMPETITORS)
    assert "SOURCE UNAVAILABLE" in block

def test_exact_output_for_two_results():
    results = [("https://a.com/", "A"), ("https://c.com/", "C")]
    block = build_summaries_block(results, COMPETITORS)
    expected = (
        "Source: https://a.com/ (company page)\nSummary: A"
        + DIVIDER
        + "Source: https://c.com/ (competitor page)\nSummary: C"
    )
    assert block == expected   