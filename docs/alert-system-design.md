# Alert System Design

## 1. Purpose

The purpose of the alert system is to provide timely visibility into changes at the prospect (such as a new executive hire or a pivot in public strategy) and at its competitors. By monitoring for specific keywords—such as "smart home," "subscription," "membership," and "family"—the system ensures that the rep is notified of relevant news without needing to perform constant manual checks. This allows the rep to react quickly and reach out at the right moment.

## 2. What it watches

The system monitors the prospect’s own pages (specifically the executive team and newsroom pages) alongside the primary competitor pages on a 24-hour schedule. It is important to note that some career portals and complex interactive pages may not be accessible because they are built with JavaScript, which the current scraper cannot read; therefore, the focus remains on the core content pages.

## 3. How it detects something new

The system detects changes by generating a hash (fingerprint) of specific, meaningful sections of a page, such as the newsroom headlines and links, rather than the entire page. This prevents the system from flagging minor, irrelevant updates like footer timestamps or social media feeds. To manage costs and noise, the system follows a two-step verification: it first checks for a keyword match; if a match is found, it then uses a model to confirm if the change is significant. This ensures that expensive model calls are only made when a potentially important change has already been identified.

## 4. How it sends the alert

When there is a match, it would send an email containing the title of the page or post, a link to it, the specific keyword that matched, and a one- or two-sentence summary written by the model. It would send the email using an email service's API or a standard SMTP library. The login for it would be stored in an environment variable, the same way the API key is stored, and never in the code or the repo. To avoid flooding the inbox, it would send a single daily digest of all matches.

## 5. What the user controls

In the Streamlit app, the rep could set the target keywords, their preferred email address, which sources to watch, and an on/off switch to activate the alert system. These settings would be stored in a small JSON file. Because this file contains the rep's email address, it would be excluded from the repository using .gitignore, just like the .env file.

## 6. Risks and limits

Some pages are built with JavaScript and cannot be read by the current scraper; a site could block frequent requests, so checks stay at a daily frequency and follow robots.txt; a page can change in ways that do not matter (such as a timestamp in a footer), which is why the system only fingerprints meaningful parts—such as newsroom headlines and links—and uses a keyword/model check to confirm the change is relevant; and there is a risk of prompt injection if a monitored page contains text designed to manipulate the model's output; however, the model check would use the same protections as the report by treating page text as data and utilizing a strict system prompt. Because each model check costs money, it runs only when there is both a text change and a keyword match.

## 7. What I would build first

1. A script that scrapes one source, stores a fingerprint of the newsroom headlines, and prints "changed" or "same" to the console.
2. Add the keyword match and the model check to filter for meaningful changes. Then, build the email notification system and the Streamlit settings interface.
