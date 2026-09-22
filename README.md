# JobApplicationGenerator

> **Evidence-driven AI pipeline for tailoring resumes and cover letters to job offers.**

JobApplicationGenerator is an experimental Python project that uses retrieval-augmented generation (RAG) to create tailored job applications from a job description and a candidate's professional background.

Instead of giving an LLM an entire candidate profile and asking it to "write a good application", the project separates **requirement extraction, evidence retrieval, relevance assessment, and generation**.

The goal is simple:

> **Generate application documents from relevant candidate evidence rather than from unconstrained language-model generation.**

---

## Overview

A job application typically requires answering two questions:

1. **What does this company need?**
2. **What evidence does the candidate have that demonstrates a match?**

JobApplicationGenerator treats these as separate problems.

```text
                         Job Offer
                             │
                             ▼
                    ┌─────────────────┐
                    │ Offer Analyzer  │
                    └────────┬────────┘
                             │
                             ▼
                    Hiring Requirements
                             │
                             ▼
                    ┌─────────────────┐
                    │    Retrieval    │
                    │  Vector Search  │
                    └────────┬────────┘
                             │
                             ▼
                    Candidate Evidence
                             │
                             ▼
                    ┌─────────────────┐
                    │    Reranking    │
                    │   LLM-based     │
                    └────────┬────────┘
                             │
                             ▼
                    Relevant Evidence
                             │
                             ▼
                    ┌─────────────────┐
                    │ Writing Decision│
                    └────────┬────────┘
                             │
                 ┌───────────┴───────────┐
                 │                       │
                 ▼                       ▼
        ┌─────────────────┐     ┌─────────────────┐
        │ Resume Writer   │     │  Letter Writer  │
        └────────┬────────┘     └────────┬────────┘
                 │                       │
                 └───────────┬───────────┘
                             ▼
                  Tailored Application
```

The system therefore separates **matching** from **writing**.

---

## Why this approach?

A naive LLM-based workflow looks like this:

```text
Job description
       +
Full candidate profile
       ↓
      LLM
       ↓
Resume / cover letter
```

This is convenient, but it gives the model a large amount of information without explicitly determining which parts are relevant to the position.

JobApplicationGenerator instead uses:

```text
Job description
       ↓
What does the employer need?
       ↓
What evidence does the candidate have?
       ↓
Which evidence is actually relevant?
       ↓
Generate the application from that evidence
```

This architecture is designed to improve:

* relevance;
* traceability;
* control over candidate information;
* consistency between the job requirements and the generated documents;
* resistance to unsupported claims.

Retrieval and structured generation do **not** guarantee factual correctness. Generated documents should still be reviewed before being used in a real application.

---

# Features

## Job offer analysis

The system can work from:

* a job offer URL;
* raw job-offer text.

The offer is transformed into a structured representation before retrieval begins.

The analysis identifies requirements such as:

* technical skills;
* tools and technologies;
* responsibilities;
* domain knowledge;
* soft skills;
* experience requirements;
* other relevant hiring needs.

---

## Requirement-driven retrieval

The system converts identified hiring needs into search queries and uses them to retrieve relevant candidate experiences.

The current retrieval architecture is based on semantic vector search using:

* **Qdrant** as the vector database;
* **multilingual-e5-large** embeddings.

The objective of this stage is primarily **recall**:

> retrieve potentially relevant evidence before deciding what should actually be used.

---

## LLM-based experience reranking

Retrieved experiences are subsequently evaluated by an LLM.

The reranking stage produces structured information including:

* relevance score;
* rank;
* decision;
* reasoning.

The current decision categories are:

```text
reject
possible
strong_match
```

The reranker therefore acts as a second-stage relevance filter on top of vector search.

---

## Writing decision

Before generation, the pipeline evaluates whether enough relevant candidate evidence has been identified.

This creates an explicit separation between:

```text
"I found something vaguely related"
```

and:

```text
"I have enough relevant evidence to generate a tailored application."
```

This step is implemented by `WritingDecider`.

---

## Tailored resume generation

The selected candidate evidence is used to generate a resume tailored to the target position.

The goal is not to invent experience, but to emphasize and organize relevant existing evidence.

---

## Tailored cover letter generation

The same evidence-driven process is used to generate a personalized cover letter.

The cover letter generation is based on:

* the job requirements;
* selected candidate evidence;
* candidate information;
* a structured writing plan.

---

# Architecture

The project is organized around application services and infrastructure components.

At a high level:

```text
JobOfferInput
      │
      ▼
OfferAnalyzer
      │
      ▼
ExperienceRetriever
      │
      ▼
ExperienceReranker
      │
      ▼
WritingDecider
      │
      ▼
OfferEnricher
      │
      ├───────────────┐
      ▼               ▼
ResumeWriter     LetterWriter
      │               │
      └───────┬───────┘
              ▼
       Generated Documents
```

The main responsibilities are separated as follows.

### `OfferAnalyzer`

Transforms the raw job offer into a structured analysis.

### `ExperienceRetriever`

Uses the analyzed hiring needs to retrieve candidate experiences from the vector store.

### `ExperienceReranker`

Evaluates the relevance of retrieved experiences using an LLM.

### `WritingDecider`

Determines whether the available evidence is sufficient for generation.

### `OfferEnricher`

Combines the analyzed offer, selected evidence, and candidate information required by downstream writers.

### `ResumeWriter`

Generates a tailored resume from the selected candidate information.

### `LetterWriter`

Creates a structured writing plan and generates the corresponding cover letter.

---

# Data flow

The pipeline progressively enriches the representation of a job application.

Conceptually:

```text
Job Offer
   │
   ├── Raw content
   │
   ▼
Offer Analysis
   │
   ├── Requirements
   ├── Hiring needs
   └── Search queries
   │
   ▼
Retrieval
   │
   ├── Candidate experiences
   ├── Retrieval scores
   └── Source information
   │
   ▼
Reranking
   │
   ├── Relevance score
   ├── Rank
   ├── Decision
   └── Reason
   │
   ▼
Selected Evidence
   │
   ├── Resume generation
   └── Letter generation
```

This staged representation is important because each component has a clearly defined responsibility.

---

# Evidence before generation

One of the central design principles of the project is that **generation should happen after evidence selection**.

The intended flow is:

```text
Requirements
      ↓
Evidence retrieval
      ↓
Evidence evaluation
      ↓
Evidence selection
      ↓
Language generation
```

rather than:

```text
Requirements
      ↓
Language generation
      ↓
Hope that the generated content is accurate
```

This does not eliminate hallucinations, but it reduces the amount of unsupported information available to the generation stage.

---

# Retrieval architecture

The current retrieval system uses semantic embeddings.

```text
Hiring Need
     ↓
Search Query
     ↓
Embedding
     ↓
Qdrant
     ↓
Top-K candidate chunks
```

The project currently uses the `multilingual-e5-large` embedding model.

This choice is useful for multilingual semantic retrieval, particularly when job descriptions and candidate experiences may not use exactly the same vocabulary.

For example:

```text
Job requirement:
"Build automated reporting pipelines"

Candidate evidence:
"Developed scheduled data-processing workflows
and automated recurring business reports."
```

A purely lexical search may miss part of this relationship.

Semantic retrieval can identify the underlying similarity.

---

# Retrieval vs. reranking

Retrieval and reranking deliberately serve different purposes.

### Retrieval

The vector search stage is optimized for finding potentially relevant evidence.

```text
Goal: high recall
```

### Reranking

The LLM then evaluates whether the retrieved evidence is actually useful for the specific requirement.

```text
Goal: improve relevance
```

Conceptually:

```text
                    Candidate experience database
                              │
                              ▼
                        Vector search
                              │
                              ▼
                         Top-K chunks
                              │
                              ▼
                         LLM reranker
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
              reject       possible    strong_match
```

This two-stage design is intended to avoid relying on a single retrieval mechanism.

---

# Candidate data

Candidate information is intentionally treated as **local application data**, rather than as part of the public source tree.

A typical local setup can contain:

```text
Docs/
├── experiences.json
└── personal_facts.json
```

These files may contain personal and professional information and should **not be committed to a public repository**.

For an open-source distribution, use anonymized examples such as:

```text
Docs/
├── experiences.example.json
└── personal_facts.example.json
```

The example files should contain entirely fictional data.

The real candidate files should remain local and be excluded through `.gitignore`.

---

# Configuration

Configuration is managed through environment variables.

Create a local `.env` file from the example configuration:

```bash
cp .env.example .env
```

Never commit the real `.env` file.

A typical configuration includes:

```env
OPENAI_API_KEY=
LLM_BASE_URL=

QDRANT_URL=
QDRANT_API_KEY=

COMPLETE_EXPERIENCES_FILEPATH=Docs/experiences.json
PERSONAL_FACTS_FILEPATH=Docs/personal_facts.json
```

The exact configuration required depends on the environment in which the pipeline is executed.

---

# Requirements

The project currently relies on:

* Python;
* an OpenAI-compatible LLM endpoint;
* Qdrant;
* embedding/model infrastructure;
* the Python dependencies listed in `requirements.txt`.

The repository should be considered **experimental** rather than production-ready.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/ArthurCoquet/JobApplicationGenerator.git
cd JobApplicationGenerator
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the local configuration:

```bash
cp .env.example .env
```

Then configure the required LLM and Qdrant settings.

---

# Running the pipeline

The main application pipeline is responsible for orchestrating the different stages:

```text
OfferAnalyzer
      ↓
ExperienceRetriever
      ↓
ExperienceReranker
      ↓
WritingDecider
      ↓
OfferEnricher
      ↓
ResumeWriter
      ↓
LetterWriter
```

The pipeline can operate from a job offer URL or from supplied job-offer content, depending on the configured entry point.

---

# Project structure

The repository is organized approximately as follows:

```text
JobApplicationGenerator/
│
├── Docs/
│   ├── experiences.example.json
│   └── personal_facts.example.json
│
├── Offers/
│
├── Prompts/
│
├── Src/
│   ├── Application/
│   ├── Infrastructure/
│   ├── Schemas/
│   ├── Services/
│   └── ...
│
├── Templates/
│
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

The exact internal organization may evolve as the project moves toward stronger domain models and clearer separation between application state and persistence.

---

# Design principles

## 1. Separate retrieval from generation

Retrieval answers:

> What candidate evidence might be relevant?

Generation answers:

> How should that evidence be expressed in an application?

These are intentionally separate problems.

---

## 2. Prefer structured intermediate representations

LLM calls are not treated as free-form text whenever structured output is possible.

Pydantic schemas are used to constrain intermediate representations such as:

* offer analysis;
* reranking results;
* writing plans;
* generated document structures.

This improves consistency between pipeline stages.

---

## 3. Keep candidate evidence explicit

The system should be able to distinguish between:

```text
Candidate evidence
```

and:

```text
LLM interpretation
```

The long-term goal is to make candidate evidence the authoritative source for factual claims.

---

## 4. Generate only after relevance has been assessed

The pipeline should not immediately generate a document from every piece of candidate information.

Instead:

```text
Retrieve
   ↓
Rank
   ↓
Select
   ↓
Generate
```

This reduces irrelevant information entering the generation context.

---

## 5. Human verification remains necessary

The system is an application-generation assistant, not an authoritative source of truth.

Even with retrieval, structured generation, and relevance filtering, generated documents can contain:

* incorrect interpretations;
* unsupported wording;
* omissions;
* accidental exaggeration.

Generated resumes and cover letters should therefore be reviewed before being submitted.

---

# Example

Suppose a job description contains:

```text
Looking for a Data Analyst with experience in:

- SQL
- dashboarding
- automated reporting
- business stakeholders
```

The pipeline can transform this into structured needs:

```text
SQL
Dashboarding
Reporting automation
Stakeholder communication
```

It then searches the candidate's experience database.

For example:

```text
Experience A
Built SQL-based reporting workflows
→ strong_match

Experience B
Created business dashboards
→ strong_match

Experience C
Participated in a software migration
→ reject
```

Only the relevant evidence is passed to the downstream generation process.

The resulting application can therefore emphasize the candidate's SQL, reporting, dashboarding, and stakeholder experience without treating every historical experience as equally relevant.

---

# Current limitations

This project is currently experimental.

Important limitations include:

### Semantic retrieval

The current retrieval architecture relies primarily on vector similarity.

Exact keyword and technical-term matching can still be important for technologies such as:

```text
SQL
SAP
Power BI
CRM
ERP
AWS
Kubernetes
```

A hybrid lexical + semantic retrieval architecture is therefore a planned improvement.

---

### LLM-based reranking

The reranking stage currently relies on an LLM.

This introduces:

* latency;
* cost;
* model dependence;
* potential variability;
* the need for evaluation.

A cross-encoder reranker is a possible future alternative or complement.

---

### No formal retrieval benchmark

The project currently does not provide a mature evaluation dataset for measuring:

* Recall@K;
* Precision@K;
* MRR;
* reranking accuracy;
* factual grounding.

Without such a benchmark, architectural changes cannot yet be compared systematically.

---

### Generation grounding

Retrieval reduces the amount of unsupported information available to the writer, but it does not provide a formal guarantee that every generated claim is supported.

Automated claim/evidence validation is therefore part of the planned roadmap.

---

### File-based state

The current application relies substantially on JSON-based state and persistence.

This is convenient for experimentation, inspection, and debugging, but a more strongly typed domain model would provide better guarantees as the project grows.

---

### External dependencies

The pipeline depends on external infrastructure such as:

* an LLM provider;
* Qdrant;
* embedding models.

These dependencies affect reproducibility, cost, latency, and availability.

---

# Roadmap

## Retrieval

* [ ] Hybrid BM25 + vector retrieval
* [ ] Improved chunking strategy
* [ ] Cross-encoder reranking
* [ ] Retrieval evaluation dataset
* [ ] Recall@K / Precision@K / MRR benchmarks

## Grounding

* [ ] Claim-to-evidence validation
* [ ] Automatic factual consistency checks
* [ ] Explicit provenance for generated claims
* [ ] Better separation between facts and LLM interpretations

## Architecture

* [ ] Stronger domain models
* [ ] Typed pipeline state instead of generic JSON dictionaries
* [ ] Dedicated `ResumePlan`
* [ ] Shared evidence model for resume and cover-letter generation
* [ ] More explicit stage boundaries
* [ ] Better failure and retry handling

## Engineering

* [ ] Automated unit tests
* [ ] Integration tests
* [ ] End-to-end evaluation
* [ ] Reproducible benchmark dataset
* [ ] Better observability and logging

## Product

* [ ] CLI
* [ ] API
* [ ] Multiple candidate profiles
* [ ] Application history
* [ ] Additional document formats

---

# Target architecture

The long-term architecture is moving toward a more explicit **evidence-centric application generation pipeline**:

```text
                        ┌─────────────────┐
                        │    Job Offer    │
                        └────────┬────────┘
                                 │
                                 ▼
                       ┌──────────────────┐
                       │ Requirements     │
                       │ Extraction       │
                       └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Evidence         │
                       │ Retrieval        │
                       └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Evidence         │
                       │ Reranking        │
                       └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Evidence         │
                       │ Selection        │
                       └────────┬─────────┘
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼                             ▼
        ┌─────────────────┐           ┌─────────────────┐
        │  Resume Plan    │           │  Letter Plan    │
        └────────┬────────┘           └────────┬────────┘
                 │                             │
                 ▼                             ▼
        ┌─────────────────┐           ┌─────────────────┐
        │ Resume Writer   │           │ Letter Writer   │
        └────────┬────────┘           └────────┬────────┘
                 │                             │
                 └──────────────┬──────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │ Generated Documents │
                    └─────────────────────┘
```

The key architectural principle is:

> **Evidence should be authoritative; the LLM should primarily transform evidence into language.**

---

# Development status

**Status: Experimental / research-oriented prototype**

The project is primarily intended to explore:

* RAG architectures for job applications;
* semantic retrieval;
* LLM-based reranking;
* structured generation;
* evidence-driven document generation;
* grounding and factual consistency.

It should not currently be considered a production-grade automated recruitment system.

---

# License

This project is distributed under the MIT License.

See [`LICENSE`](LICENSE) for details.

---

# Author

Developed by **Arthur Coquet**.

---

## Final note

JobApplicationGenerator is an experiment in treating job-application generation as an **evidence selection problem followed by a language-generation problem**.

The objective is not simply to ask an LLM to write a better application.

It is to build a pipeline that can answer:

```text
What does this job require?
        ↓
What evidence does the candidate have?
        ↓
Which evidence is relevant?
        ↓
Is there enough evidence to write?
        ↓
How should that evidence be expressed?
```

That separation between **requirements, evidence, relevance, and generation** is the central design principle of the project.
