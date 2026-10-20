# Undetectable Humanize

A Codex skill that sends selected text to the Undetectable.AI API and saves the returned text in a Word document.

## Install

1. Open [the GitHub repository](https://github.com/bn7thebh/undetectable-humanize) and select **Code → Download ZIP**.
2. Extract the ZIP and rename the extracted folder to `undetectable-humanize`.
3. Copy that folder into your local Codex skills directory:
   - **Windows:** `%USERPROFILE%\.codex\skills\`
   - **macOS/Linux:** `~/.codex/skills/`
4. Check that `SKILL.md` is directly inside `undetectable-humanize`, with the helper at `undetectable-humanize/scripts/humanize.py`. Avoid an extra nested folder from the ZIP.
5. Restart Codex and start a new chat.

This skill expects a Python 3 runtime and the documents skill for Word output. PDF input also requires the PDF skill. Codex desktop provides a runtime discovery tool; in other environments, use your installed Python 3 runtime.

## Configure your own API key

Each user needs their own Undetectable.AI account, API key, and sufficient credits. The repository does not include a key or provide shared credits.

### Windows

1. Obtain your API key from your own Undetectable.AI account.
2. Search the Windows Start menu for **Edit environment variables for your account** and open it.
3. Under **User variables**, click **New**.
4. Set **Variable name** to `UNDETECTABLE_API_KEY`.
5. Set **Variable value** to your own API key.
6. Click **OK** to save and close the dialogs, then restart Codex.

The helper can also read this stored Windows user variable if the running app has not inherited it.

### macOS/Linux

Set `UNDETECTABLE_API_KEY` in the environment used to launch Codex. For a terminal session, the following prompts for the key without displaying it or placing the key itself in shell history:

```sh
printf 'Undetectable.AI API key: '
read -r -s UNDETECTABLE_API_KEY
printf '\n'
export UNDETECTABLE_API_KEY
```

Run these commands in Bash or Zsh, then launch Codex from that same terminal so it inherits the variable. This setting lasts for that shell session; an already-running desktop app will not inherit it.

Do not paste your key into chat, repository files, issues, or screenshots. The helper does not load `.env` files automatically.

## Use

1. Start a new Codex chat after installing the skill and configuring your key.
2. Attach your document or paste the text you want processed.
3. Send this request:

   > Use $undetectable-humanize to humanize this text and save the returned result as a Word document.

The helper uses your locally configured key. API usage consumes your own Undetectable.AI credits, not the repository owner's credits.

If Codex cannot find the skill, check the folder structure above and restart it. If the helper reports a missing key, check the variable name and the environment used to launch Codex. Do not paste your key into chat to troubleshoot.

Selected text is sent to Undetectable.AI and may consume credits. Input must contain at least 50 characters. Results are not guaranteed to evade detectors; review facts, citations, names, and numbers before use.

## Privacy

The helper reads credentials locally and sends the key only in the API authentication header. Keep input, output, and resumable job files outside this repository or inside the ignored `work/` and `outputs/` directories. Review files before publishing; `.gitignore` is only an accidental-commit safeguard.

API reference: <https://help.undetectable.ai/en/article/humanization-api-v2-p28b2n/>
