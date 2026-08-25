# Project Vision

| | |
|---|---|
| Name | Ivan |
| Username | drdong654 |
| Project name | RAG-11 |
| Product owner | Ivan Vanichkin (drdong654@gmail.com|
| Tech stack | Python, SQLite, Docker, RAG, MCP, Hybrid Search |

## Problem and target audience

*If we talk about the target audience, then these are novice programmers at school and their teachers. Our main goal is to make it convenient to interact with the school using the latest technologies in the IT world.*

## Market and similar solutions

*At the moment, there is a weak range of RAG systems for schools on the market. In most cases, this principle is used by large companies to improve their business processes, as well as to improve the service.*

## Base requirements

*What must the system do to solve the problem? Focus on value, not obvious things like "users can log in". Aim for 3–5 requirements. Full requirements with acceptance criteria go in [Requirements](requirements.md).*

- BR-1: The system must provide accurate answers to students’ questions using the programming school’s internal knowledge base, including educational materials, FAQ, documentation, and internal instructions.

- BR-2: The system must use a RAG pipeline with Hybrid Search, combining semantic search and keyword search to retrieve the most relevant context before generating an answer.

- BR-3: The system must support both Telegram and Discord bot interfaces, allowing students and school staff to interact with the assistant from their preferred platform.

- BR-4: The system must provide source-based responses, showing which document or knowledge base fragment was used to generate the answer.

- BR-5: The system must support MCP-based integration, allowing the assistant to connect external tools, services, and knowledge sources in a scalable way.

## Tech stack

*What technologies are you planning to use and why? Motivation can be prior experience, wanting to learn something, or industry relevance. Detailed architectural decisions — component breakdown, deployment diagram, data model — go in [Architecture](architecture.md).*

| Part | Technology | Why |
|---|---|---|
| Frontend | Telegram Bot + Discord Bot | Users interact with the system directly inside familiar messengers without needing a separate web interface. |
| Backend | Python + aiogram + discord.py + RAG pipeline | Python is well suited for bot development, AI integrations, embeddings, search logic, and rapid MVP development. |
| Database | PostgreSQL/Sqlite + pgvector | Stores project data and vector embeddings for semantic search in one reliable database. |
| Search | Hybrid Search: pgvector + PostgreSQL Full-Text Search / BM25 | Combines semantic search by meaning with keyword search for exact technical terms, code names, and documentation phrases. |
| AI Layer | LLM + MCP | The LLM generates contextual answers, while MCP allows the system to connect external tools, knowledge sources, and services. |
| Deployment | Docker + Docker Compose + VPS | Docker makes deployment reproducible, Compose helps run the bot, database, and search services together, and VPS gives full control over the environment. |

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
