# Undetectable Humanize

A Codex skill that sends selected text to the Undetectable.AI API and saves the returned text in a Word document.

## Install

Download this repository and copy the folder containing `SKILL.md` and `scripts/` into your local Codex skills directory as `undetectable-humanize` (normally `~/.codex/skills/undetectable-humanize`). Restart Codex if needed to discover it.

This skill expects a Python 3 runtime and the documents skill for Word output. PDF input also requires the PDF skill. Codex desktop provides a runtime discovery tool; in other environments, use your installed Python 3 runtime.

## Configure your own API key

Each user needs their own Undetectable.AI account, API key, and sufficient credits. The repository does not include a key or provide shared credits.

Set `UNDETECTABLE_API_KEY` locally. On Windows, open **Edit environment variables for your account**, add a user variable named `UNDETECTABLE_API_KEY`, and paste your own key as its value. The helper can read that stored user value even if Codex has not inherited it. On macOS or Linux, set the variable in the environment used to launch Codex.

Do not paste your key into chat, repository files, issues, or screenshots. The helper does not load `.env` files automatically.

## Use

Ask Codex: “Use $undetectable-humanize to process this text and save the result in a Word document,” then supply your text or file.

Selected text is sent to Undetectable.AI and may consume credits. Input must contain at least 50 characters. Results are not guaranteed to evade detectors; review facts, citations, names, and numbers before use.

## Privacy

The helper reads credentials locally and sends the key only in the API authentication header. Keep input, output, and resumable job files outside this repository or inside the ignored `work/` and `outputs/` directories. Review files before publishing; `.gitignore` is only an accidental-commit safeguard.

API reference: <https://help.undetectable.ai/en/article/humanization-api-v2-p28b2n/>
