# Hestia Sales Research Assistant

A Streamlit app that helps a sales representative prepare to pitch **Hestia** (a household organizer with budgeting, meal planning, pantry tracking, grocery ordering, and a chore chart with rewards for kids) to a prospect company. The rep enters the prospect and its competitors, and the app reads their public web pages and writes a short account brief in which every fact points back to its source page.

> **AI assistance note:** this README was drafted by Claude (Anthropic's AI assistant) at the student's request. The application code in `src/cap_931/` was written by the student. Claude was used to explain concepts, review code and help debug.

CAP 931 capstone project, UCI 3025.1 (Per Scholas).

## What it does

1. **Form:** the rep enters the product, the company name and website, the product category, competitor URLs (one per line), a one-sentence value proposition, and the target customer. Required fields and URLs are validated.
2. **Fetch:** the app downloads each page and strips the scripts and styles, leaving the readable text.
3. **Summarize:** Claude summarizes each page into short labeled notes (strategy, competitors, leadership, product/technology).
4. **Merge:** a second prompt combines the notes into one brief with these sections: Company Strategy, Competitor Mentions, Leadership, Product/Strategy Summary, Article Links and Limitations. Every bullet ends with `(Source: <url>)`. Pages that could not be read are listed under Limitations.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/) (the Python package and project manager)
- An Anthropic API key. Each report makes about five model calls (one summary per page plus one merge). With the default model a report costs about half a cent; see [Model](#model).

## Setup

```bash
git clone https://github.com/sethcutright1-sketch/CAP_931.git
cd CAP_931
uv sync
```

Create a file named `.env` in the project folder (next to `pyproject.toml`) with one line:

```
ANTHROPIC_API_KEY=your-key-here
```

The key must never be committed. `.env` is listed in `.gitignore`.

## Run

From the project folder (the one that contains `pyproject.toml`):

```bash
uv run streamlit run src/cap_931/app.py
```

Streamlit prints a local address, usually http://localhost:8501. A report takes about 30 to 45 seconds.

Example values to try:

| Field | Value |
|---|---|
| Product name | Hestia |
| Company name | Best Buy |
| Company website | `https://corporate.bestbuy.com/executive-team/` |
| Product category | Household organization and smart-home software |
| Competitor URLs (one per line) | `https://store.google.com/` and `https://www.samsung.com/us/smart-home/` |
| Value proposition | Hestia is a subscription-based household organizer that adds ongoing value for customers using their new or existing smart-home hardware through private, connected planning and management tools. |
| Target customer | VP of Product, Digital Experience |

## Project layout

| File | What it does |
|---|---|
| `src/cap_931/app.py` | The Streamlit form, input validation, and the display of the brief |
| `src/cap_931/web_research.py` | Fetches a page and returns clean text, or a clear failure message |
| `src/cap_931/llm_client.py` | Sends a prompt to Claude, with error handling and an optional system prompt |
| `src/cap_931/prompts.py` | The step 1 and step 2 prompt builders and the system prompt |
| `src/cap_931/research_chain.py` | The pipeline: summarize each page, build the summaries block, build the brief |

## How it stays accurate and on topic

- **Sources on every fact.** Each summary and each bullet carries the URL it came from.
- **Use only the page text.** The prompts forbid inventing names, dates or figures. Empty categories say so ("No relevant information on this page." / "No information available").
- **Page text is data, not instructions.** Page content is placed between markers and treated as data; the system prompt tells the model to ignore instructions found there.
- **System prompt guardrail.** The model is limited to sales account research. Off-topic requests are declined.
- **Failures are reported.** A page that cannot be fetched, or has no readable text, is listed under Limitations and not guessed at.
- **Relevance and length.** The brief keeps facts that matter for a household-management pitch and limits each section to 10 bullets.

## How it was tested

- The form validation was exercised with eight automated cases (empty fields, invalid URLs, a competitor list with blank lines).
- The prompt builders were checked offline, without calling the model, so that every value lands in the right place.
- The request that `llm_client.py` sends to the API was checked with a stand-in client, with and without a system prompt.
- The briefs were checked by comparing every name, title, date and product mentioned against the real page text.
- The guardrail was tried with an off-topic request typed into a form field and with a hidden instruction placed inside a fake page. Neither was obeyed.

The model comparison script is `tests/compare_models.py`. It calls the real API, so it prints the number of calls it will make and waits for you to type `yes`. Run it from the project folder with `uv run python tests/compare_models.py`. The other check scripts are not included in this repository.

## Known limitations

- Pages that build their content with JavaScript (for example the Best Buy careers page) return almost no text to a plain HTTP request, so they cannot be read.
- Some sites block automated requests. A blocked page is reported under Limitations.
- The form takes one company page. Leadership and strategy coverage depends on which page is given.
- Results vary slightly from run to run. In some runs the model changed a tense (a future departure written in the past tense) or repeated a word.
- The optional product-overview upload is accepted by the form but not yet used in the brief.
- The system prompt is a guardrail, not a security guarantee.

## Model

The default model is `claude-haiku-5-5`, set in `src/cap_931/llm_client.py` (a small, fast, low-cost model). I compared it with `claude-sonnet-5-5` and with a mix (Haiku for the page summaries, Sonnet for the final brief) on the same Best Buy report, using `tests/compare_models.py`. One run each on 2026-10-28; prices from Anthropic's pricing page, checked 2026-10-26.

| Setup | Time | Cost per report | What I saw |
|---|---|---|---|
| Haiku for both steps | 34.8 s | $0.0054 | Accurate, but did not mention that Best Buy's CEO leaves on Oct. 31 |
| Sonnet for both steps | 41.7 s | $0.0926 | Accurate and more complete (the CEO and CFO changes, more executives); about 17 times the cost |
| Haiku summaries, Sonnet merge | 31.1 s | $0.0284 | Also missed the CEO change: the merge step cannot use facts the summaries dropped |

I checked the facts in all three briefs by hand against the page text, and they were correct. Haiku is the default because it is accurate, fast and costs about half a cent per report. Sonnet is the better choice when a complete brief matters more than the cost. These are single runs on one example, so the differences are observations, not guarantees. The full write-up, including the decision rule and the limits of the test, is in [docs/model-comparison.md](docs/model-comparison.md).

## More documentation

- [Alert system design](docs/alert-system-design.md)
- [Production deployment plan](docs/deployment-plan.md)
- [Other model types](docs/other-model-types.md)
- [Model comparison](docs/model-comparison.md)
