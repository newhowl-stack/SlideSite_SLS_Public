# SlideSite+ for Claude

Hosted-presentation connection.

Upload this plugin in Claude where custom plugins are available. Connecting still requires your SlideSite sign-in and presentation consent.

MCP endpoint: https://slidesite-backend-live-production.up.railway.app/api/llm/mcp

1. In Claude, open Settings → Connectors → Add custom connector. Enter the Server URL below.

2. Choose OAuth / Register automatically. Sign in to SlideSite and choose the presentation and edit permission.

3. Start a chat, enable SlideSite and attach the skill package.

After connecting, ask: “Read the presentation I authorized and summarize its slides. Then change a sentence I identify, using my selected editing permission.” Verify the resulting saved edit or review the pending proposal in SlideSite.

This download contains no API key, OAuth token or presentation content. Your provider subscription/installation rules and SlideSite presentation permissions apply separately. BYOK in-editor setup is a separate flow; do not put a provider API key into MCP OAuth fields.

## Documentation
- [Claude plugin instructions](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
- [Claude connector setup](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)

## Source
Cloud skill/setup conventions adapted from [SlideSite AI packages](https://github.com/newhowl-stack/SlideSite_SLS_Public/tree/main/cloud), inspected 27 October 2026; permission/operation guidance updated for full hosted editing. No standalone draft package is included.
