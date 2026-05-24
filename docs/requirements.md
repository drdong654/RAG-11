# Requirements

A flat list of everything the system must do or be. One row per requirement. Add new ones to the bottom — don't renumber.

## Functional requirements

What the system does.

| ID | Title | Description | Priority | Status |
|---|---|---|---|---|
| BR-1 | | | must / nice | ☐ Planned · ☐ In progress · ☐ Done |
| BR-2 | | | must / nice | ☐ Planned · ☐ In progress · ☐ Done |
| BR-3 | | | must / nice | ☐ Planned · ☐ In progress · ☐ Done |

## Non-functional requirements

Quality, performance, security, accessibility, GDPR, anything that isn't a feature.

| ID | Category | Description | Status |
|---|---|---|---|
| NFR-1 | Performance | | ☐ Planned · ☐ In progress · ☐ Done |
| NFR-2 | Security | | ☐ Planned · ☐ In progress · ☐ Done |
| NFR-3 | Accessibility | | ☐ Planned · ☐ In progress · ☐ Done |

---

## How this connects to GitHub Issues

This document is the **canonical list**. It answers "what does the system have to do?" at a glance.

The day-to-day work of implementing each requirement happens in GitHub Issues:

- One or more Issues per `BR-N` / `NFR-N`, broken down into pieces of work
- Reference the requirement ID in the Issue title or body (e.g. `[BR-1] Add registration form`)
- When all linked Issues for a requirement are closed, mark its status here as Done

Don't duplicate descriptions between this file and Issues. The file is the *what*, the Issues are the *how*.

For concrete examples of well-written Issues, see [Issues — how to write them](issues.md).
