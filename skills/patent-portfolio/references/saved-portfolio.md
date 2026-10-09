# Saved portfolio and families

## Read before deciding on updates

1. Use `search` with no `query`, first with `category: application` and then `category: patent`. Follow `nextCursor` while `hasMore` is true. These are accessible saved records, not public-corpus search results. Applications can include drafts and submitted cases as well as filed/imported applications.
2. Read `family` when returned. Group records by `family.groupingKey` for the current view; the key represents an accessible saved grouping and can change after links or permissions change. It is not a global or permanent patent-family identifier. Keep ungrouped records explicit when family information is unavailable.
3. Use `fetch` with member `documentId` values and no filtering options to inspect selected records and their family information. This also allows family readback after an update; focused section reads omit family and part listings. The available member/reference lists are bounded; check `membersTruncated` and `referencesTruncated`. Continue the portfolio listing rather than treating a partial list as complete.
4. Summarise families, member applications, jurisdictions, recorded statuses, priority dates and their provenance. Keep competitor references and the innovation pipeline separate unless the user requests them; family members may include an earlier priority case outside the application/patent search categories.

Count distinct saved groupings separately from application records and recorded publication numbers. `applicationCount` and `recordedPublicationCount` describe one accessible family, including its selected record; do not add those counts again for each search hit in the same family. Recorded publication counts do not include every historical publication or represent an invention count. Portfolio totals require completed pagination and deduplication. Incomplete visibility or differing member views prevents claiming an exact organisation-wide total.

A family overview describes connected, accessible saved records. `coverage: unverified` means it does not establish a complete public family, ownership or current legal status. An isolated saved application does not prove there are no relatives. `other_related` includes indirect ancestors and other connected filings; do not relabel all of them as siblings.

`priorityDateSource: imported` identifies the selected record's imported priority date. `earliest_saved_priority_filing` derives the date from the accessible family's saved priority filings. `unknown` leaves it unknown. Neither is a fresh verification of every priority claim.

If `family` is absent, continue the record review and state that family membership cannot be inspected through this connection. Do not invent groups from similar titles.

## Read selected patent sections

When the advertised `fetch` schema supports `include`, `mode` and `cursor`, use them for focused text questions. Keep the exact document or part ID returned by discovery, including its entity prefix and part/revision suffix. With a known ID, `mode: "outline"` reports native section availability without text; it does not accept a cursor. For content, supply a nonempty `include` selection from `claims`, `description` and `abstract`. Content mode is the default when `include` is supplied; explicit `mode: "content"` and pagination both require `include`.

Read `retrieval` for source/revision attribution, section status and page completeness. Follow `retrieval.next_cursor` with the same ID and selection until `retrieval.has_more` is false. If interrupted, report unread content rather than claiming a complete review. A stale cursor requires restarting; do not combine different `content_version` values. Oversized blocks can span pages: concatenate fragments with the same `block_id` directly, using `continued` and `continues` to preserve their boundaries and native claim numbering.

Distinguish `available`, `empty`, `unavailable` and `unknown` section statuses. Missing or unknown stored content is not evidence that a publication lacks that section. `import_status` and warnings describe stored import processing separately from pagination; finishing the pages does not repair a partial import. Section reads do not import, repair or query a patent provider.

Omit all options when full content, part discovery or family metadata is needed. If the connection lacks focused retrieval, explain that limit and use supported reads within the user's scope. An incompatible or oversized filtered response fails without truncated content; report the failed read rather than treating it as an empty section or claiming completeness.

## Decide whether refresh helps

`family.refresh` assesses the selected record's stored references, not the entire family or newer provider information. Reading it makes no provider call and performs no reconciliation.

| Assessment | Next step |
| --- | --- |
| `missing_links` | Stored references have accessible saved matches without the expected direct relationship. Inspect the returned references and record links; a refresh of this record can be appropriate within the user's authorised update scope. |
| `unresolved_references` | Inspect unmatched and ambiguous references. An unmatched reference means no accessible saved match, not proof that the organisation lacks it. Identify/import authorised missing publications or resolve ambiguity; repeated refresh alone is not a remedy. |
| `unknown` | Stored reference information is unavailable or unreadable. This is uncertainty, not evidence of a failed import or missing family. |
| `no_known_gap` | No gap was found in the stored references checked. This does not establish complete or current family coverage. Routine refresh is unnecessary. |
| `unsupported` | This record lacks a usable publication identifier for refresh. Explain the limit. |

`eligible` describes the record's identifier, not permission to write. `lastRefreshedAt` records an explicit family refresh when known; null does not mean that import failed or that references were never retrieved. A missing or old timestamp alone does not require refresh. An explicit request to check newer public family information can warrant refresh even when no stored gap is known.

## Update and verify

A read-only review stops with its findings. When updates are authorised, preserve that authorisation and avoid asking again for the same action. Read the affected records, compare saved facts with the requested change, import selected additions, and refresh selected existing records only when warranted. Follow [import and refresh](import-and-refresh.md) for retries and limitations.

After a write, `fetch` the affected record IDs and compare the family members and reference assessment with the baseline. Re-read a record with its own stored references when checking a particular missing relationship. Report what the readback verifies, what remains unresolved, and any limits from access or truncation. A successful write receipt and a verified resulting family are separate observations. If readback fails, preserve the write result and report verification as incomplete.
