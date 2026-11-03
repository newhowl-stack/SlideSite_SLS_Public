# Make slides with ChatGPT

Use a session that supports uploaded files and downloadable output. Availability depends on your account and mode. No SlideSite+ account or hosted connector is needed.

1. [Download the starter ZIP](https://github.com/newhowl-stack/SlideSite_SLS_Public/raw/refs/heads/main/downloads/SlideSite_Starter.zip) and unzip it.
2. Start a fresh ChatGPT chat. Upload the ZIP if the session can inspect archives. Otherwise upload `starter.html` and `skills/slidesite/SKILL.md` from the extracted folder.
3. Send the prompt below, replacing the topic and audience.

> Read skills/slidesite/SKILL.md and the SLS_AGENT_README and SLS_AGENT_INDEX embedded in starter.html. Create three editable slides about urban gardening for beginners: why it matters, three ways to start, and a one-week plan. Use the supplied canonical HTML as the base. Edit only deck-source JSON, retain supported Theme bindings and preserve the runtime scripts, CSP, fonts, assets and libraries. Return a downloadable presentation.html and a ZIP containing that same HTML. Check the model and render it if your tools allow; report any checks you could not perform.

4. Download the generated HTML or ZIP. Unzip if needed. **Open the HTML directly in a browser before editing and saving locally.** Review every slide and manually edit a headline. Use **Download HTML copy** in the editor’s save controls; use this download action if Save As is unavailable.
5. Close the original tab and reopen the exact newly downloaded copy. Check the edited headline and slide count. Disconnect networking and reopen again to verify the deck works offline.
6. For another AI edit, upload your **latest saved HTML**, then request the change. Do not restart from the original starter or an older attachment.

This is an attachment workflow; downloading the ZIP does not install a persistent ChatGPT plugin.

If the AI cannot read the file or return a real download, use a session with file tools. Do not copy partial code into an empty file or accept a replacement editor built from scratch. Keep the original until the new copy reopens successfully.

[Known limitations/test status](../KNOWN_LIMITATIONS.md) · [Feedback](https://github.com/newhowl-stack/SlideSite_SLS_Public/issues/new). Hosted SlideSite+ uses a separate preview setup linked from the main README.
