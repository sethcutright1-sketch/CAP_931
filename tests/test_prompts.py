from prompts import build_summary_prompt, build_sections_prompt, system_prompt

def make_step1(product):
    return build_summary_prompt("https://a.com", "page text", ["https://c.com/"], product)

def make_step2(product):
    return build_sections_prompt("VP", "Acme", ["https://c.com/"], "A value proposition.", "SUMMARIES", "A category", product)

def test_step1_contains_product_name():
    assert "Aurora" in make_step1("Aurora")

def test_step2_contains_product_name():
    assert "Aurora" in make_step2("Aurora")

def test_no_hardcoded_product():
    text = make_step1("Aurora") + make_step2("Aurora") + system_prompt
    assert "Hestia" not in text

def test_no_unfilled_placeholders():
    text = make_step1("Aurora") + make_step2("Aurora")
    assert "{" not in text