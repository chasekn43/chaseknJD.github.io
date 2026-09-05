# Non-Negotiable Project Rules & Execution Constraints

## 1. Target Environment & Authoritative Scopes
- **Primary Canonical Domain**: `https://kinslow-regulatory-archive.org`
  - Authoritative for CFPB Complaint #260717-35668593, Affirm dispute evidentiary archive, TILA / FCRA / UDAAP statutory teardowns, and forensic ledger analysis.
- **Sister Consumer Protection Domain**: `https://bypassbots.org`
  - Authoritative for AI model criticism, bot circumvention tools, and consumer self-help utilities.
- **Authoritative Remote Repositories**:
  - `chasekn43/regulatory-archive-2026` (Primary deployment branch: `main`, bound via CNAME to `kinslow-regulatory-archive.org`)
  - `charwiz43/BNPL-abuse-fintech-lies-regulatory` (Primary deployment branch: `main`, bound via CNAME to `bypassbots.org`)
  - `chasekn43/chasekn43.github.io` (Legacy GitHub Pages portfolio mirror)

## 2. The Verification Rule (Zero Shortcuts)
- No task or deployment is complete until an independent live `curl` / HTTP status code returns **200 OK** directly on the public internet.
- Internal assumptions, mock passes, or local server tests do NOT qualify as complete.
- Every release must verify:
  1. Live HTTP 200 OK status on apex and www domains.
  2. Live availability of `/sitemap.xml`, `/robots.txt`, `/dataset.json`, `/openapi.json`, and `/.well-known/security.txt`.
  3. Canonical header/tag consistency across all indexed paths.

## 3. Credential & Authentication Hygiene
- Never hardcode tokens, API keys, or private identifiers in git commits, markdown files, or workflow files.
- Never trigger interactive Git UI credential prompts.
- For local scripts, read credentials silently from Windows Credential Manager (`credential.helper=manager`) or environment variables (`$env:GITHUB_TOKEN`).
- In GitHub Actions CI/CD workflows, strictly use repository secrets (`${{ secrets.GITHUB_TOKEN }}` or user-managed repository secrets).

## 4. Pre-Flight Checklist Execution
Before any deployment or migration commit is published, the following sequence is mandatory:
1. **Permission Check**: Verify remote write access (`push: True`) before staging commits.
2. **Object Integrity Check**: Ensure full git tree depth to prevent shallow pack rejection errors (`index-pack failed`).
3. **MIME & Schema Validation**: Validate `sitemap.xml` against the official Sitemaps XML Schema and validate `dataset.json` / `openapi.json` against JSON-LD and OpenAPI 3.0 specifications.
4. **Live Edge Verification**: Run automated polling loops against the live edge server until the live hash or tag matches.

## 5. Local & Remote Write Boundary
- Unapproved arbitrary modifications outside the defined project scope are prohibited.
- All modifications must preserve existing valid evidence, citations, and regulatory dockets.
