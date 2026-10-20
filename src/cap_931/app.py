import streamlit as st
from urllib.parse import urlparse

def is_valid_url(text):
    parts = urlparse(text.strip())
    return parts.scheme in ("http", "https") and bool(parts.netloc)


st.title("Product Prospect Form")          # 1. title

with st.form("prospect_form"):            # 2. everything inside is one form
    product_name = st.text_input("Product name")                       # one-line box
    prospect_company_url = st.text_input("Company website")
    product_category = st.text_input("Product category")
    competitor_urls = st.text_area("Competitor URLs (one per line)")  # multi-line box
    value_proposition = st.text_area("Value Proposition (one sentence)")  # multi-line box
    target_customer = st.text_input("Name or role of target customer")
    product_overview = st.file_uploader("Product overview (PDF, TXT, or MD)", type=["txt", "md", "pdf"])
    submitted = st.form_submit_button("Submit")                # 3. the button

if submitted:                              # 4. runs only after clicking Submit
    errors = []                            # collect problems here
    if not product_name.strip():
        errors.append("Product name is required.")
    if not prospect_company_url.strip():
        errors.append("Company website is required.")
    elif not is_valid_url(prospect_company_url):
        errors.append("Please enter a valid company website URL.")
    if not product_category.strip():
        errors.append("Product category is required.")
    if not target_customer.strip():
        errors.append("Target customer is required.")
    if not value_proposition.strip():
        errors.append("Value proposition is required.")

    competitor_list = []
    lines = competitor_urls.splitlines()
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            competitor_list.append(stripped_line)
    if not competitor_list:
        errors.append("At least one competitor URL is required.")
    else:
        for url in competitor_list:
            if not is_valid_url(url):
                errors.append(f"Invalid competitor URL: {url}")
    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("Submitted!")
        st.write("Product:", product_name)
        st.write("Company website:", prospect_company_url)
        st.write("Product category:", product_category)
        for url in competitor_list:
            st.write("-", url)
        st.write("Value Proposition:", value_proposition)
        st.write("Target Customer:", target_customer)
        st.write("Product Overview:", product_overview.name if product_overview else "No file uploaded")

