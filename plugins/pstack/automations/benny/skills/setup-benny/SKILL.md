---
name: setup-benny
description: Prepare optional Benny triage and reproduction recipes for a Codex project; does not create schedules unless requested.
---

# Set up Benny for Codex

Read `../../FOR_AGENTS.md` and the plugin's CODEX.md. Resolve the target repository from the request. Inspect existing configuration before asking for missing values.

1. Copy the pack to `.agents/pstack/benny/` only when project setup is requested. Preserve destination-only files and local edits. Keep user configuration outside that folder, for example `.agents/benny/configuration.yaml`, with the feature map and routing map beside it. Use the bundled templates as examples, not finished configuration.
2. Verify pstack's shared skills are available in the execution environment. A user-level install works for local Codex; a remote runner needs its own installed copy or committed accessible instructions. Do not write Cursor settings or assume this computer's plugin cache exists remotely.
3. Configure the Slack source channel, immutable thread coordinates, trusted triage identity, tracker adapter, repository, feature map, control adapter, artifact retention, and bounded budgets. Keep credentials in the service's secret mechanism or an ignored local environment file. Never put them in chat or tracked files. Read the operational skills for required fields and failure behavior.
4. Discover actual Slack and tracker tools. Verify read and thread-reply capabilities without posting test messages unless the user requests a test post. Do not invent tool names. If child-agent tool isolation cannot exclude Slack credentials and write tools, run Benny in the coordinator instead of delegating.
5. Exercise the control adapter locally with a harmless scenario and save evidence. Missing channels, trusted identities, tracker access, or control capabilities block the corresponding workflow; report the exact missing configuration.
6. For a one-off requested run, read the selected operational skill and process only the supplied report. Source-channel writes must stay in its original thread. Publishing tickets, replies, or draft PRs must be included in the requested scope.
7. Only when asked to schedule, discover the supported Automations tools, inspect existing automations to avoid duplicates, and create or update the requested schedule using the concrete reviewed prompt and working directory. Use `../../templates/` as prompt material. Do not pass unsupported event-trigger fields. For Slack events, use an explicitly configured event service or report that integration is missing. Do not silently substitute polling for an event trigger.
8. Report which files were prepared, which one-off operations ran, and which schedules or event bindings the host actually confirmed. Setup alone does not activate a bot.
