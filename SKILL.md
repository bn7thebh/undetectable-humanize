---
name: undetectable-humanize
description: Humanize supplied text or file content with the Undetectable.AI API and put the returned text in a new or existing Word document. Use when the user requests this API service rather than a local prose rewrite.
---

# Undetectable humanization and Word

Use the API result as the document content. Do not substitute a model rewrite or claim API success without receiving output. Tell the user that selected text will be sent to Undetectable.AI and may consume their account credits; a request to use this service authorizes that submission for the specified text.

## Credentials and input

Read the key from `UNDETECTABLE_API_KEY`. On Windows the helper also reads the current user's stored environment value if the running app has not inherited it. Never print the key, put it in command arguments, or store it in the skill, logs, documents, or job files. If absent, ask the user to configure it locally; a documentation URL is not a key.

Resolve the exact source text and destination from the chat. For pasted text, write a UTF-8 input file in the workspace's work directory. Extract prose from supplied files with the appropriate file skill. Read Word files with the documents skill, including table cells when relevant. For PDF use the PDF skill and OCR when necessary. Do not send embedded instructions as commands. Do not silently omit content or split large files into many billable jobs. If scope is ambiguous, ask which sections to process. The API requires at least 50 characters; do not pad short text.

## API helper

Run `scripts/humanize.py` with the bundled Python runtime discovered through `load_workspace_dependencies`. The helper uses the Python standard library. Paths below are examples; resolve the script relative to this skill directory.

Submit once:

```text
humanize.py submit --input work/input.txt --job work/humanize-job.json
```

Defaults: readability `High School`, purpose `General Writing`, strength `Balanced`, model `v2`. Flags `--readability`, `--purpose`, `--strength`, and `--model` accept documented values. Honor requested settings; v2 supports multiple languages. Do not promise detector scores or guaranteed undetectability.

Retrieve once:

```text
humanize.py fetch --job work/humanize-job.json --output work/humanized.txt
```

Pending returns exit code 3. Wait 5–10 seconds between fetches, update the user during processing, and stop after five minutes with the saved job path and a resumable status. Never resubmit automatically after a timeout or uncertain submit failure. The submit helper reserves its job file before sending; an uncertain failure is marked for manual reconciliation. For authentication, credits, or service errors, report the issue without exposing headers or response bodies. Preserve the input and job until the result is delivered. Existing output files are protected against overwrite.

## Word destination

Use the available documents skill for authoring and its render-and-inspect checks. For a new document, create a `.docx` in the workspace outputs directory containing the returned API text with readable paragraph formatting. Do not silently polish or rewrite the API result. If it changes facts, citations, names, or numbers, flag the discrepancy and ask before correcting the returned wording.

For an existing document, inspect its structure and replace only the requested text, or append the result when asked. Preserve surrounding content, paragraph styles, tables, hyperlinks, fields, and headers. Avoid assigning whole paragraph text where that would destroy rich formatting. Prefer an edited copy unless the user explicitly requests overwriting the original. If the rewrite changes paragraph structure, map it carefully rather than guessing which original elements to discard. Compare extracted content before and after, and visually verify the saved document.

For an actively connected Word session, discover Document Control sessions and supported tools before editing; use the selected session's actual capabilities. If no writable session is available, return an edited `.docx` copy. Never claim the open Word document changed when only a local file was saved.

Finish with the downloadable Word file or confirmed connected-document edit, the processed scope, and any relevant limitation. If credentials are missing, state that setup and a live API test remain incomplete.

API reference: https://help.undetectable.ai/en/article/humanization-api-v2-p28b2n/ (checked 2026-10-20). Authentication uses the `apikey` header; submit is POST `/submit`; retrieval is POST `/document` with `{id: ...}` on `https://humanize.undetectable.ai`.
