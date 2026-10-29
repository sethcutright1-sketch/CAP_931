# Model Comparison

## 1. What I tested

I ran the same report three ways using Best Buy as the prospect. For every run, I used the same four pages (two Best Buy pages, Google Store, and Samsung SmartThings) and the same prompts. I tested three different model configurations: Haiku/Haiku, Sonnet/Sonnet, and a hybrid (Haiku for summaries, Sonnet for the merge). Each run was performed on 2026-10-28, using price points from 2026-10-26.

Note on methodology: I fetched the pages only once and reused them across all three runs to ensure that every model was reading identical text. This eliminates "web scraping variance" as a factor and ensures that any difference in the output is due to the model's processing, not a change in the source data.

## 2. Results

| Setup | Time | Cost | Bullets | Corie Barry mentioned | Leadership bullets |
|---|---|---|---|---|---|
| Haiku / Haiku | 34.8 s | $0.0054 | 18 | No | 5 |
| Sonnet / Sonnet | 41.7 s | $0.0926 | 23 | Yes | 7 |
| Haiku summaries, Sonnet merge | 31.1 s | $0.0284 | 18 | No | 4 |

(Note: Corie Barry is Best Buy’s CEO, who leaves on Oct. 31).

## 3. What I saw

All three briefs were accurate, but they were not equally complete; Haiku and the hybrid left out the critical CEO transition. When I checked the claims against the pages by hand, all three were factually correct. However, Sonnet successfully identified the CEO and CFO changes and also named Neal Sample and Jennie Weber, which the others didn't. In terms of style, Sonnet produces a denser report, packing several distinct facts into a single bullet point.

## 4. The tradeoff

Sonnet cost 17 times as much and took about 20% longer to process. The core question is whether that extra cost is worth it. For a sales rep, missing a major leadership transition (like a CEO departure) could result in an awkward reach-out or a missed opportunity to pivot the conversation.

The most surprising result was the hybrid model. Even though it used Sonnet for the "merging" step, it still missed the CEO change. My explanation for why the hybrid failed is that the merge step only sees the information the summary phase kept. Because I did not save the Step 1 summaries, I cannot confirm exactly what Haiku dropped, but this is the most likely reason. Essentially, the hybrid model provided no more detail than Haiku.

Ultimately, Sonnet cost about 17 times as much, and what that bought was a more complete brief.

## 5. My decision

Rule: Haiku by default, Sonnet when specific facts matter.

Use Haiku when: Performing high-volume, general research, such as summarizing broad product features or general market sentiment where a missing executive name won't derail the strategy.

Use Sonnet when: Preparing a high-stakes pitch or a "deep dive" executive briefing where leadership changes and specific organizational shifts are critical to the sales strategy.

The Hybrid Model: I would not use the hybrid model. It is an inefficient middle ground; it costs 5x more than Haiku but fails to provide the extra information that Sonnet captures. You are paying a premium for a "merger" of information that has already been filtered out by the cheaper model.

Cost Analysis: At 100 reports, the cost difference is roughly $0.54 for Haiku versus $9.00 for Sonnet. For a sales tool, I think if one more complete report helps a rep land a contract, the $9.00 spend is negligible compared to the potential deal value.

## 6. Limits of this test

Sample Size: This test involved only one run per setup, one prospect, and one set of pages.

Non-determinism: Two separate Haiku runs of the same setup produced slightly different briefs, meaning a single run is an observation of a single moment in time.

Manual Verification: Accuracy was checked by hand, which is subject to human error and not a scalable automated check.

Price Fluctuations: Prices were pulled from 2026-10-26; actual costs may vary slightly by the time of execution.

Cost/Data Variance: Haiku’s own cost varied slightly between runs (e.g., $0.0056 vs $0.0054), and I did not save the Step 1 summaries, which limits the ability to pinpoint exactly what data was lost during the hybrid summary phase.

Prompting Issue: Sonnet added a bullet point about features the Google page lacks (budgeting, meal planning). This information came from my own product’s feature list provided in the prompt, not from the source pages. This is a prompt-engineering issue to be fixed, rather than a failure of the Sonnet model itself.
