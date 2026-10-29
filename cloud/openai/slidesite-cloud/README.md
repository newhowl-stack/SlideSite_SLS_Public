# SlideSite+ for ChatGPT

Hosted-presentation connection.

This includes a portable plugin and setup guide. Downloading a ZIP does not install a ChatGPT app; use the custom MCP connection flow where available.

MCP endpoint: https://slidesite-backend-live-production.up.railway.app/api/llm/mcp

1. In ChatGPT Plugins, choose + → Add custom MCP server. Enter the Server URL below.

2. Choose OAuth with dynamic registration. Create and install the plugin; sign in to SlideSite and choose the presentation and edit permission.

3. Start a chat, select @SlideSite and attach the skill package.

After connecting, ask: “Read the presentation I authorized and summarize its slides. Then change a sentence I identify, using my selected editing permission.” Verify the resulting saved edit or review the pending proposal in SlideSite.

This download contains no API key, OAuth token or presentation content. Your provider subscription/installation rules and SlideSite presentation permissions apply separately. BYOK in-editor setup is a separate flow; do not put a provider API key into MCP OAuth fields.

## Documentation
- [ChatGPT connection instructions](https://developers.openai.com/plugins/deploy/connect-chatgpt)
- [Open ChatGPT Plugins](https://chatgpt.com/plugins)

## Source
Cloud skill/setup conventions adapted from [SlideSite AI packages](https://github.com/newhowl-stack/SlideSite_SLS_Public/tree/main/cloud), inspected 27 October 2026; permission/operation guidance updated for full hosted editing. No standalone draft package is included.
