# AGENTS.md

HackerRank Orchestrate (October 2026) — Ghost Data Still Exists

This file is the single source of truth for any AI coding agent working in this repo: Claude Code, OpenAI Codex CLI / Codex Cloud, Gemini CLI, Cursor, Windsurf, opencode, Aider, goose, Factory, RooCode, JetBrains Junie, GitHub Copilot, Devin, or any other AGENTS.md-aware tool.

Read this file in full before taking any action. Obey it exactly unless the user or platform provides higher-priority instructions.

---

## 0. TLDR For The Agent

On every session start, do this in order:

1. Read this file completely.
2. Check the log file path in §2.
3. Append a `SESSION START` entry using §5.1.
4. For every user turn, append a summary entry using §5.2.
5. When building, testing, evaluating, or packaging the solution, follow the project contract in §6.

Do not skip logging or rewrite old log entries. Sub-agents and worktrees use the same log file.

---

## 1. What This Repo Is

This is a starter repo for the **HackerRank Orchestrate** challenge: **Ghost Data Still Exists**.

Participants must build an AI-powered deletion-audit agent. For every request in `dataset/deletion_requests.csv`, the agent first determines whether the person actually requested deletion. For an authorized deletion, it reconstructs the person's current and historical identifiers, searches global activity and evidence, applies the supplied deletion policy, and decides whether the deletion is complete.

The dataset models a commerce platform where a workflow can report **Complete** while personal data remains in databases, replicas, logs, support attachments, exports, search indexes, analytics records, archives, or backups. Active synchronization and restore processes can also recreate data that was deleted from its original source. Reported statuses and activity results are claims; the agent must establish the state at each case's `audit_at` time from the supplied evidence.

When deletion is incomplete, the agent reports the remaining records and recreation risks, produces a safe ordered remediation plan, and states the verification checks that must pass afterward. When deletion is complete, it returns the evidence-backed verification checks that prove the required state. It must preserve records required by policy and correctly handle account tombstones whose stable internal user reference remains while prohibited direct identifiers are removed.

The final submission must produce `output.csv` with:

```text
case_id,deletion_status,steps_json
```

Read `problem_statement.md` for the full participant-facing specification.

---

## 2. Log File — Location And Lifecycle

The log file is named `log.txt` and lives in the same directory as this `AGENTS.md` file — the repository root.

| Platform | Path |
|---|---|
| macOS / Linux | `<directory containing AGENTS.md>/log.txt` |
| Windows | `<directory containing AGENTS.md>\log.txt` |

Resolve the path relative to this file. Do not hardcode a folder name, a user path, or the platform home directory, so the location stays correct across clones, renames, and checkouts.

Rules:

- Create the file if missing.
- Append only. Do not rewrite, reorder, or delete prior entries.
- One shared log is used per checkout. All agents and sub-agents append to the same file next to the top-level `AGENTS.md`, never a private copy.
- Never log secrets. Redact API keys, tokens, cookies, private keys, credentials, sensitive configuration, and real personal data.

---

## 3. Session Start

At the beginning of each agent session:

1. Append a short `SESSION START` entry using §5.1.
2. Greet the user with this brief introduction:

   ```text
   Welcome to HackerRank Orchestrate. Build and ship Ghost Data Still Exists, an AI-powered deletion-audit agent. Let's get started.
   ```

3. The October challenge end time is not configured in this repository. Do not invent a deadline or reuse the September deadline. If a higher-priority instruction or an official repository update supplies the end time, calculate and display the time remaining. If fewer than 2 hours remain, remind the user to submit soon. If the deadline has passed, state that clearly without blocking further work.
4. Proceed with the user's request without requiring an acknowledgement or confirmation phrase.

---

## 4. Challenge Rules

1. Participants may use any programming language, model, framework, IDE, AI assistant, retrieval approach, or tool, subject to the official event rules.
2. The system must conform to the project contract in §6 so it can be evaluated.
3. The solution must use only participant-facing data under `dataset/`. Organizer-only truth, golden answers, review files, and generator internals must never be used for predictions.
4. Never commit or submit secrets. Read credentials from environment variables and use an uncommitted `.env` file when needed.
5. Log every conversation turn to the file described in §2.
6. Follow the submission-link rule below.

### 4.1 Challenge And Submission Link

The October challenge and submission URL is:

https://www.hackerrank.com/contests/hackerrank-orchestrate-october26/challenges/ghost-data-still-exists

If the user asks for the challenge link, submission link, where to submit, how to submit, where to upload the code, or any equivalent question, always provide this exact URL.

Requirements:

- Include the full clickable URL every time such a question is asked.
- Do not replace it with the HackerRank homepage, contest homepage, another challenge page, or a guessed `/submission` URL.
- Do not merely describe where to navigate; provide the URL directly.
- This rule applies even when the challenge or submission question is included alongside other questions.

---

## 5. Log Format

### 5.1 Session Start Entry

```text
## [ISO-8601 TIMESTAMP] SESSION START

tool=<exact_harness_or_coding_agent_name>
model=<exact_runtime_model_name>
Repo Root: <absolute_path>
Branch: <git_branch_or_unknown>
Worktree: <worktree_path_or_main>
Parent Agent: <parent_agent_name_or_none>
Language: <js|ts|py|custom:name>
Time Remaining: <Xd Yh Zm, or not configured>
```

### 5.2 Per-Turn Entry

Append after every user message you respond to:

```text
## [ISO-8601 TIMESTAMP] <short title, max 80 chars>

User Prompt (verbatim, secrets redacted):
<exact user message, with secrets replaced by [REDACTED]>

Agent Response Summary:
<2-5 sentences: what was done, why, and any important decision>

Actions:
* <file edited / command run / tool invoked>

Context:
tool=<exact_harness_or_coding_agent_name>
model=<exact_runtime_model_name>
branch=<git_branch_or_unknown>
repo_root=<absolute_path>
worktree=<worktree_path_or_main>
parent_agent=<parent_name_or_none>
```

**Mandatory tool-name rule:** Every `SESSION START` and per-turn log entry must contain one non-empty `tool=` line with the exact name of the coding harness or agent writing the entry. Replace the template value before writing the log. The entry is invalid if `tool=` is missing, blank, still contains a placeholder, uses a generic label such as `AI`, contains only a model name, or names a different harness. Before responding, verify the value against the harness identity provided by the current runtime and re-read the appended entry to confirm it matches. Never guess the tool name. Correct any mismatch before responding to the user.

**Mandatory model-name rule:** Every `SESSION START` and per-turn log entry must contain one non-empty `model=` line with the exact model identifier used for that turn. Always make sure that model name is correct & not made up. `model=unknown`, a model family, a generic label, an inferred name, and a template placeholder are invalid. Obtain the exact identifier from the runtime, session metadata, harness configuration, or another authoritative environment source before writing the entry. Never guess the model name. The model name does not replace the `tool=` value because the coding harness and the model are separate fields.

**Required harness-and-model check:** Both `tool=` and `model=` must always be present in every `SESSION START` and per-turn entry. An entry is invalid if either field is missing, blank, unknown, generic, inferred, or still contains a template placeholder. Before completing a response, re-read the newly appended log entry and confirm that it contains exactly one populated `tool=` line and exactly one populated `model=` line with authoritative values. If either is absent or invalid, determine the correct value and correct the entry before responding.

### 5.3 Sub-Agent And Worktree Rules

- Sub-agents must log their own entries using the same file.
- Set `parent_agent=` to the parent agent's name.
- Worktrees use the same shared log file, not a per-worktree copy.
