# Production Deployment Plan

## 1. Overview

The app is a Streamlit web page that researches web pages and extracts relevant information. In production, it would be used by a sales representative preparing to pitch a product to a prospect company.

## 2. Hosting

For a demo, I would use Streamlit Community Cloud because it is easy to deploy and share quickly, though it has limitations such as being public by default and having restricted resources. For production, I would use a service like Google Cloud Run. This would allow the app to run in a containerized environment that scales automatically to handle concurrent users while maintaining better security and infrastructure.

## 3. Scalability

One report is currently slow because the bot must fetch several pages and make multiple model calls to synthesize the final report. To handle more users, I would implement a task queue to manage request volume and use a smaller, faster model for the initial page summarization (Step 1) to control costs. I would also implement a caching system for page summaries (rather than whole reports) with a 24-hour expiration to ensure that repeated requests for the same data do not require new model calls.

## 4. Security

The API key would be stored in a production secret store (such as Google Secret Manager), not in the repository. Users would sign in to provide access control and to manage individual API costs, while also personalizing their experience. Web pages are untrusted; therefore, I use strict honesty rules in the system prompt—such as treating page text strictly as data and using specific markers to prevent prompt injection. I also require the model to cite specific source URLs to prevent hallucinations. I would add robots.txt checks and a request delay, which the current scraper does not do. During testing, one site (the Best Buy investor page) returned a 403 error to the default request headers and returned content once I sent a browser-style User-Agent header.

## 5. Maintenance

Pages change frequently; for example, the Best Buy executive team page may be updated. I would monitor the system for specific triggers, such as "SOURCE UNAVAILABLE" results, pages returning very little text, or the Best Buy careers page which is currently inaccessible due to JavaScript rendering. Additionally, because the same prompt can yield slightly different results on different runs, I would monitor for output quality shifts rather than just hard failures. Models can be retired or updated; I would pin specific model versions and run a regular suite of "honesty tests"—running the system against a fixed set of pages with known facts to ensure accuracy after any prompt or model change. I would monitor key metrics such as failure rates and the cost per report.

## 6. Cost & Budget

Each report requires several LLM calls. I measured one report (about five model calls: a summary for each page plus one merge) on 2026-10-28, at Anthropic's prices checked on 2026-10-26. It cost about $0.005 (half a cent) with the small model (claude-haiku-5-5) and about $0.09 with the larger model (claude-sonnet-5-5). Using the small model for the summaries and the larger one for the merge cost about $0.03. At 100 reports a month, that is roughly $0.54 with the small model and $9 with the larger one. I would implement a monthly spending cap via the model provider’s billing console to ensure costs remain within a predictable budget.

## 7. First three steps I'd take

1. Build and polish the Streamlit UI to ensure the user experience is smooth and intuitive, and the final report display is easy to understand.
2. Implement a logging and error-handling system to track specific issues (like 403 errors or JS-rendered pages) and improve reliability.
3. Conduct a final "honesty audit" to ensure the system adheres to the strict honesty rules and accurately cites sources.
