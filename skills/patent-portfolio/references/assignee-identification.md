# Assignee identification

Use this guidance when discovering a portfolio by company, applicant or assignee name. `search_public_patents` searches patent publications by assignee; it does not resolve company identities.

## Choose names to search

Start with the legal names supplied by the user. An organisation's display name or trading brand may differ from the names used in patent filings. Known publications and other available sources can help identify relevant filing names.

Include supported spelling variants, transliterations and former names. Establish whether subsidiaries or acquired companies belong in the requested portfolio before expanding to them. Keep uncertain entities separate and clarify those that would materially change the import scope.

Retain the names searched and the evidence for including them, so the same scope can be used for subsequent updates.

## Search and select publications

Pass one name at a time through the `assignee` field using simple text. The tool does not accept provider-specific query syntax. Follow the returned `nextPage`, even when a page contains no matches; note `truncated` or other coverage limits.

Assess returned assignee values and source information against the intended company. Similar names can identify different entities, and filings can list historical or joint applicants. Use known publications or technical context to resolve ambiguity. Keep unsupported matches out of the import set.

The user determines whether selected publications belong in their own portfolio or are third-party references. An applicant or assignee name in a publication does not, by itself, establish current ownership.

## No matches or incomplete results

If there are no matches, check supported name variants and report the names searched. Say that the search returned no matching publications; this does not establish that the company has no patents. Keep any broader discovery within the user's intended company scope.

Distinguish an empty result from an incomplete search caused by a provider error or a coverage limit. Report the unfinished portion so the user can decide whether further discovery is needed.
