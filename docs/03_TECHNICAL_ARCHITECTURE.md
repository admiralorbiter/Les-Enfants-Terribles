---
title: "Technical Architecture"
project: "Les Enfants Terribles"
project_code: "LET"
status: "planning_baseline"
version: "0.1"
owner: "Jonathan Lane"
created: "2026-08-13"
last_reviewed: "2026-08-13"
---


# Technical Architecture

## 1. Architecture objective

Build a local-first, desktop-first experimental substrate that preserves raw episodes, supports replaceable processors, and makes new hypotheses cheap to test.

The architecture should remain useful even if:

- no generative model is available;
- a transcription engine changes;
- subscription workflows remain manual;
- the twin concept fails;
- the user stops active experimentation.

## 2. Current stack decision

### Locked for the first field period

- **Platform:** Windows desktop.
- **Application:** local browser application.
- **Backend:** Python + Flask.
- **Frontend:** Jinja templates + HTMX; Alpine.js only where local state is helpful.
- **Capture:** browser `getUserMedia()` + `MediaRecorder`.
- **Metadata:** SQLite.
- **Search:** SQLite FTS5 for transcripts and text.
- **Raw media:** filesystem, outside Git.
- **Derived media/text:** filesystem plus SQLite metadata.
- **Processing:** asynchronous local worker.
- **Speech-to-text:** replaceable transcriber interface; local `faster-whisper` is the provisional default.
- **Media normalization:** FFmpeg or PyAV behind a small adapter.
- **Version control:** Git for code, schemas, prompts, fixtures, and planning—not raw media.
- **Recurring external API cost:** zero by default.

### Provisional

- SQLAlchemy 2 for persistence.
- Pydantic or JSON Schema for processor and event contracts.
- A database-backed job queue rather than Redis/Celery.
- A CLI entry point such as `let`.
- Localhost-only networking for the first field period.

### Deferred

- mobile-native application;
- multi-device sync;
- cloud backend;
- graph database;
- vector database;
- fine-tuning;
- continuous screen capture;
- wearable ingestion;
- multi-user collaboration.

## 3. High-level system

```text
BROWSER / IMPORT / SENSOR
          │
          ▼
    CAPTURE SERVICE
          │
          ├── save raw artifact atomically
          ├── compute hash
          ├── create event
          └── attach/create episode
          │
          ▼
      LOCAL STORE
   files + SQLite metadata
          │
          ▼
      JOB QUEUE
          │
    ┌─────┼─────────────┐
    ▼     ▼             ▼
normalize transcribe  processors
    │     │             │
    └─────┼─────────────┘
          ▼
   DERIVED ARTIFACTS
          │
          ▼
      REPLAY ENGINE
          │
    ┌─────┼───────────────┐
    ▼     ▼               ▼
  local manual bridge  future API
  model  subscription   provider
          │
          ▼
      DEBRIEF / FEEDBACK
```

## 4. Core components

### Capture service

Responsibilities:

- request browser microphone access;
- record audio;
- receive uploads;
- accept text;
- accept MARK events;
- save raw bytes before any processor runs;
- generate stable IDs;
- return an unambiguous success state.

Invariant:

> If Stop reports success, the raw artifact exists durably and can be recovered independently of all downstream processing.

### Episode service

Responsibilities:

- create and update meaningful episode containers;
- attach multiple artifacts and events;
- preserve natural boundaries;
- allow later merge/split without changing raw artifact identity;
- store domain and declared cognitive mode.

### Artifact store

Responsibilities:

- filesystem path management;
- content hashes;
- MIME/type metadata;
- immutable raw namespace;
- derived namespace;
- export and backup manifests.

Suggested local layout:

```text
LET_DATA/
├── let.sqlite
├── raw/
│   ├── audio/
│   ├── video/
│   ├── image/
│   └── text/
├── derived/
│   ├── normalized/
│   ├── transcripts/
│   ├── thumbnails/
│   ├── analyses/
│   └── exports/
├── backups/
└── temp/
```

### Job worker

Responsibilities:

- claim queued work;
- record processor/version/configuration;
- retry safely;
- avoid duplicate outputs;
- expose failure without blocking capture;
- support replay.

The initial queue can be a SQLite table with leases and statuses:

```text
queued → running → succeeded
                 ↘ failed → retry/dead
```

Do not introduce Redis or Celery before local concurrency requires them.

### Processor registry

A processor is any versioned transformation:

- audio normalization;
- transcription;
- transcript cleanup;
- episode segmentation;
- Liquid candidate generation;
- manual external model result;
- Solid state estimate;
- evidence comparison.

Initial implementation may use ordinary Python classes registered in code. A dynamic plug-in marketplace is unnecessary.

Conceptual interface:

```python
class Processor:
    name: str
    version: str

    def supports(self, inputs) -> bool: ...
    def run(self, context) -> list[DerivedArtifact]: ...
```

### Replay engine

Replay is a core multiplier.

It should be possible to:

- select an existing episode;
- choose a processor and version;
- run it again;
- preserve prior output;
- compare results;
- mark one result as preferred without erasing others.

### Manual AI bridge

Because subscription access is abundant and API spending is undesirable, human-mediated processing is a first-class path.

#### Export

Generate a bounded **Mission Brief** containing:

- episode purpose;
- selected transcript/media references;
- declared mode;
- requested processor behavior;
- provenance;
- exact return schema.

Copy it to clipboard or save Markdown/JSON.

#### External run

Jonathan uses Antigravity, ChatGPT, Claude, Gemini, or another subscribed interface.

#### Import

Paste or upload the response.

LET records:

- provider/model if known;
- prompt packet hash;
- response;
- time;
- parser version;
- output type;
- human notes.

Manual transport does not weaken provenance if it is recorded explicitly.

### Feedback and experiment service

Store:

- whether an intervention was shown;
- the selected stance;
- user response;
- right/wrong/partly;
- useful/irrelevant/intrusive;
- novelty;
- joy effect;
- follow-up action;
- experiment condition.

## 5. Browser recording

The browser MediaStream Recording API is sufficient for the first capture experience.

Design requirements:

- large record/stop control;
- timer;
- visible microphone status;
- browser-supported MIME negotiation;
- safe cancellation;
- chunk handling for longer recordings if necessary;
- confirmation only after server persistence;
- local playback.

The application should not require real-time transcription.

## 6. Transcription

Use a provider interface:

```text
Transcriber
├── FasterWhisperTranscriber
├── WhisperCppTranscriber
├── CloudTranscriber
└── ManualTranscriptImporter
```

Initial decision:

- local transcription;
- timestamps;
- preserve raw unedited transcript;
- optional human-corrected transcript as another version;
- never overwrite.

Do not analyze acoustic features as psychological truth. Voice-prosody analysis is experimental and requires separate validation.

## 7. SQLite use

SQLite stores:

- episodes;
- artifacts;
- events;
- derivations;
- jobs;
- transcript segments;
- processor runs;
- interventions;
- feedback;
- experiments;
- model snapshots.

Use:

- WAL mode if concurrent browser/worker access requires it;
- foreign keys;
- transactions;
- schema versioning;
- FTS5 for searchable text;
- integrity checks.

Binaries remain on disk unless a later experiment demonstrates a compelling reason to use BLOBs.

## 8. Reliability invariants

1. Raw save precedes processing.
2. Raw artifacts are immutable.
3. Every artifact has a content hash.
4. Derived artifacts declare processor version and source.
5. Jobs are idempotent or produce distinct versioned results.
6. Retries never duplicate canonical identity.
7. A database rebuild does not alter event times.
8. Backup manifests can be verified.
9. Restore is rehearsed.
10. Temporary files are never mistaken for durable capture.
11. External model outputs are imports, not facts.
12. No recurring paid call happens without an explicit policy.

## 9. Sensor adapter model

Future sources should enter as adapters, not core rewrites.

Conceptual event API:

```python
let.observe(...)
let.capture(...)
let.mark(...)
let.attach(...)
```

Candidate sensors:

- Git;
- Plex webhooks;
- ActivityWatch;
- screenpipe;
- Omi;
- MIDI;
- game recordings;
- browser extensions;
- phone capture.

Rule:

> A hypothesis pulls in a sensor. A sensor does not invent its own justification.

Example:

- Question: “Do interruptions change programming review quality?”
- Sensor candidate: ActivityWatch window/AFK events.
- Only then integrate.

## 10. Fast experimental path

The fastest useful system is:

```text
browser audio capture
        ↓
raw file + SQLite episode
        ↓
local transcription
        ↓
Mission Brief export
        ↓
subscription model via Antigravity
        ↓
response import
        ↓
voice follow-up
```

This path can test sophisticated Liquid ideas before provider APIs, passive sensors, or autonomous agents exist.

## 11. Suggested repository shape

```text
les-enfants-terribles/
├── README.md
├── AGENTS.md
├── pyproject.toml
├── .gitignore
├── docs/
├── schemas/
├── templates/
├── src/
│   └── let/
│       ├── capture/
│       ├── episodes/
│       ├── artifacts/
│       ├── jobs/
│       ├── processors/
│       ├── replay/
│       ├── feedback/
│       ├── experiments/
│       ├── web/
│       └── cli.py
├── tests/
│   ├── fixtures/
│   └── synthetic_corpus/
└── instance/
    └── local configuration only
```

The actual data root should be separately configured and ignored.

## 12. Developer multipliers to build early

These are more valuable than early feature breadth:

- stable capture/artifact API;
- episode abstraction;
- processor interface;
- replay;
- derivation/provenance;
- durable job queue;
- synthetic corpus;
- manual AI bridge;
- feedback primitive;
- doctor;
- backup/restore;
- export.

## 13. What not to decide yet

- final database schema;
- final transcript model;
- final UI design;
- embeddings;
- graph representation;
- learned intervention policy;
- clone ontology;
- long-term storage provider;
- passive capture platform;
- phone implementation.

The first-use evidence should shape these decisions.
