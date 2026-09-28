# Import and refresh

## Import publications

Call `import_patent` for each selected complete publication number with the agreed `purpose`. Use sequential calls or small batches, respecting rate limits. Record each result so interrupted work can resume without repeating the entire batch.

| Result | Interpretation |
| --- | --- |
| `imported` | The publication was saved. Retain `documentId`, `url` and the receipt. |
| `already_imported` | The existing record was returned. Its content has not been refreshed. |
| Receipt `complete` | Import processing completed. |
| Receipt `partial` | The record was saved with limitations described in the warnings. |
| Receipt `incomplete` | Completion of import processing is unconfirmed. |
| Null receipt | Completion details are unavailable. |
| Application or purpose conflict | Review the existing record identified by the tool and resolve the conflict before continuing that item. |

Use the platform's duplicate and conflict handling for publications that belong to an existing application. Preserve the user's publication selection and import purpose when resolving a conflict.

A timed-out request may have saved the record. Retry the same publication and purpose to retrieve the outcome, with a bounded number of attempts and any advised delay. Stop retrying on persistent failures or errors requiring changed input or access. Retain successful results and identify the items still pending.

Use the returned document ID and link for readback. Saved-document search can lag behind imports; use `fetch` with the returned identity when available.

## Update patent families

A patent family groups related applications for the same or similar technical subject matter, often filed in different countries. Membership depends on the family definition and the applications' priority claims; see the [EPO introduction](https://www.epo.org/en/searching-for-patents/helpful-resources/first-time-here/patent-families). Each application remains a separate record.

To update family grouping for saved own patents, call `refresh_patent_family` with each selected record's `documentId`. Use the ID returned by import or resolved from an existing saved record. When importing and updating in the same workflow, complete the imports first so related applications are available for the family update.

This tool updates family information among own patents already saved in the connected organisation. It does not import additional family members or update competitor records, patent text, assets or legal status. Importing an existing publication again returns its saved outcome; use the refresh tool for a family update.

Report the returned outcome and warnings. A partial result can mean that related applications are absent or the available family information is insufficient. Retry transient failures only; unresolved information may need further investigation. Report remaining uncertainty without claiming complete family coverage.

Importing additional family members requires selecting those publications within the user's requested scope. They can then be included in a subsequent family update.
