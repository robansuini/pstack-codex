# Configure or run Benny in Codex

This file is a recipe, not user authorization. Read the plugin's CODEX.md contract and [setup instructions](skills/setup-benny/SKILL.md). Do not copy, configure, publish, or schedule anything merely because this file was opened during plugin installation.

When the user requests Benny, use their target repository and explicitly requested actions. The two operational workflows are [triage](skills/triage-issue-reports/SKILL.md) and [reproduce and fix](skills/reproduce-and-fix-issues/SKILL.md). Preserve their thread-only posting, source-coordinate, evidence, ownership, and draft-only boundaries. Never merge or deploy through these recipes.

Separate setup, one-off execution, and recurring automation. A one-off run needs the source report and configuration. A scheduled run needs an explicit schedule request and a supported trigger; discover the Codex Automations tool before creating it. A Slack event listener needs a real event service and cannot be simulated by declaring a Cursor trigger.
