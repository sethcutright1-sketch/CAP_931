# Hestia Sales Research Assistant

A Streamlit app that helps a sales representative prepare to pitch a product to a prospect company. The rep enters the product (name, category and a one-sentence value proposition), the prospect and its competitors, and the app reads their public web pages and writes a short account brief in which every fact points back to its source page. Nothing in the prompts is tied to one product: the project was built around a household organizer called Hestia, and the same code was also tested with a second, unrelated product.

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
- **Relevance and length.** The brief keeps facts that help pitch the product described by the category and value proposition the rep entered, and limits each section to 10 bullets. Leadership is exempt from the relevance rule, because a rep needs to know who the decision makers are. Relevance works best when the product and the prospect's business overlap; for an unrelated product the model has less to latch onto.

## How it was tested

Run the automated tests from the project folder. They never call the model and cost nothing:

```bash
uv run pytest -v
```

There are 14 tests in `tests/`:

- `test_prompts.py` checks that the product name reaches both prompts, that no product name is hard-coded, and that no `{placeholder}` is left unfilled.
- `test_research_chain.py` checks the summaries block: company and competitor pages are tagged correctly, the divider appears only between items, unavailable sources are kept, and the full output matches the expected text.
- `test_llm_client.py` uses a stand-in client to check that several text blocks are joined, thinking blocks are ignored, a reply with no text returns a fallback message, and the system prompt is sent only when given.

I also broke the code on purpose (for example swapping the page tags or joining text blocks with a space) to confirm each test fails when it should.

Other checks, done by hand or with scripts that are not in this repository:

- The form validation was exercised with eight automated cases (empty fields, invalid URLs, a competitor list with blank lines).
- The briefs were checked by comparing every name, title, date and product mentioned against the real page text.
- The guardrail was tried with an off-topic request typed into a form field and with a hidden instruction placed inside a fake page. Neither was obeyed.

The model comparison script is `tests/compare_models.py`. It calls the real API, so it prints the number of calls it will make and waits for you to type `yes`. Run it from the project folder with `uv run python tests/compare_models.py`.

## Implemented and planned

| Feature | Status |
|---|---|
| Form with required-field and URL validation | Implemented |
| Page fetching with clear failure messages | Implemented |
| Two-step prompt chain (summarize each page, then merge) | Implemented |
| Source URL on every fact; unreadable pages listed under Limitations | Implemented |
| Guardrail system prompt and prompt-injection handling | Implemented |
| Product-neutral prompts (any product, not only Hestia) | Implemented |
| Cost and token logging per call | Implemented |
| Model comparison (Haiku, Sonnet, mixed) with documented results | Implemented |
| Automated tests (14, offline) | Implemented |
| Product overview upload used in the brief | Planned (the form accepts it, the brief ignores it) |
| Splitting the work across several agents (one per competitor, plus a reviewer) | Planned, not built |
| Pages that need JavaScript to load | Planned, not built |
| Alert system for changes on a watched company | Design only, see [docs/alert-system-design.md](docs/alert-system-design.md) |
| Production deployment | Design only, see [docs/deployment-plan.md](docs/deployment-plan.md) |
| Other model types | Design only, see [docs/other-model-types.md](docs/other-model-types.md) |

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
