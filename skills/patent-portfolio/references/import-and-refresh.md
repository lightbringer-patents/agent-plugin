# Import and refresh

## Import publications

Call `import_patent` for each selected complete publication number with the agreed `purpose`. Use sequential calls or small batches, respecting rate limits. Record each result so interrupted work can resume without repeating the entire batch.

| Result | Interpretation |
| --- | --- |
| `imported` | The publication was saved. Retain `documentId`, `url` and the receipt. |
| `already_imported` | The existing record was returned. Its content has not been refreshed. |
| Receipt `complete` | Import processing completed. |
| Receipt `partial` | The record was saved with limitations described in the warnings. |
| Receipt `incomplete` | The record was saved, but import processing did not finish. This does not mean work is still running. |
| Null receipt | Completion details are unavailable. |
| Application or purpose conflict | Inspect the existing record identified by the error with `fetch` when an ID is available; report the conflict and retain its link. |

For a conflict, compare the existing publication and purpose with the request. If the existing record satisfies the user's goal, report it as already saved without claiming the requested import succeeded. Otherwise leave that item unresolved and continue the rest of the authorised batch. The import tool cannot change an existing record's purpose or replace its publication; direct the user to the Lightbringer platform or team for those changes. Do not alter identifiers or purpose to bypass a conflict.

A timed-out request may have saved the record. Retry the same publication and purpose to retrieve the outcome, with a bounded number of attempts and any advised delay. Stop retrying on persistent failures or errors requiring changed input or access. Retain successful results and identify the items still pending.

Repeating an import retrieves its saved outcome; it does not complete missing text, PDFs or images. Report these limitations from the receipt warnings and use the Lightbringer platform or team when further help is needed.

Use the returned document ID and link for readback. Saved-document search can lag behind imports; use `fetch` with the returned identity when available.

## Update patent families

A patent family groups related applications for the same or similar technical subject matter, often filed in different countries. Membership depends on the family definition and the applications' priority claims; see the [EPO introduction](https://www.epo.org/en/searching-for-patents/helpful-resources/first-time-here/patent-families). Each application remains a separate record.

Own-patent imports automatically attempt to group related saved applications into families. Import order does not require a separate refresh: later imports can establish relationships with earlier records.

Refresh is useful when:

- Available records or the user indicate that related saved own applications are missing a family relationship.
- An import or refresh result specifically reports that family grouping did not finish.
- The user asks to update saved families using newer public patent information.

Do not refresh routinely after each import or batch. A general warning that family coverage is unverified is not evidence of a failed update; a missing PDF or image is unrelated to family grouping. Similar titles or subject matter alone do not establish a missing family relationship. Use the structured family overview from `search` or `fetch` when returned; follow [saved portfolio and families](saved-portfolio.md) to assess gaps. If family information is absent, describe the limit instead of claiming to have inspected membership.

For a warranted refresh, call `refresh_patent_family` with the affected saved record's `documentId`. Use the ID returned by import or resolved from an existing saved record. If the request also includes importing identified related publications, finish those imports first and assess whether a separate refresh is still needed. Honour existing authorisation to update the selected families.

This tool updates family grouping among own patents already saved in the connected organisation. It does not import additional family members or update competitor records, patent text, PDFs, images or legal status. Importing an existing publication again returns its saved outcome; use the refresh tool for a family update.

Existing family relationships are retained. If the inconsistency is an incorrect relationship that needs removing or changing, explain that refresh cannot make that correction and direct the user to the Lightbringer platform or team.

Report the returned outcome and warnings. A partial result can mean that related applications are absent or the available family information is insufficient. If `links` is null, the family update did not finish; a bounded retry can attempt it again. Otherwise retry transient failures only. The result reports counts, not a list of family members: do not infer publication identities or a complete family from those counts.

When additional related publications have been identified from available sources and selected within the user's requested scope, import them and report the returned outcome. Their family grouping is attempted automatically. Report any missing members that could not be identified or imported.

After authorised imports or family refresh, fetch affected saved record IDs and compare their family overview with the baseline. Preserve returned receipts and warnings if readback is unavailable; describe verification as incomplete. Refresh counts alone do not identify or verify the resulting members.
