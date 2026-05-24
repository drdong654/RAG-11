# Project Vision

| | |
|---|---|
| Name | |
| Username | |
| Project name | |
| Product owner | *Your name, or company name + contact person* |
| Tech stack | |

## Problem and target audience

*What problem does your app solve? Who is it for? Be specific — "young adults" is too vague, "university students who need to track shared expenses" is useful.*

## Market and similar solutions

*What similar apps already exist? What do they do well, what do they lack? If nothing is exactly the same, how do users solve this problem today?*

## Base requirements

*What must the system do to solve the problem? Focus on value, not obvious things like "users can log in". Aim for 3–5 requirements. Full requirements with acceptance criteria go in [Requirements](requirements.md).*

- BR-1:
- BR-2:
- BR-3:

## Tech stack

*What technologies are you planning to use and why? Motivation can be prior experience, wanting to learn something, or industry relevance. Detailed architectural decisions — component breakdown, deployment diagram, data model — go in [Architecture](architecture.md).*

| Part | Technology | Why |
|---|---|---|
| Frontend | | |
| Backend | | |
| Database | | |
| Deployment | | |

## How the documentation connects

Each artefact builds on the previous one:

```
Project Vision            high-level goals and base requirements
  ├─ Project Plan         milestones, scope, risks
  ├─ Architecture         how the system is structured
  └─ Design               user personas, wireframes, user flows
       └─ Requirements         one requirement per user flow (BR-X)
```

Fill these in roughly in order — you don't need everything upfront, but Vision should exist before you write Design, and Requirements before Architecture stabilises.

**These are living documents.** Return to them as your understanding of the problem and solution evolves. A requirement you wrote early on may need updating later — that is expected, not a mistake.
