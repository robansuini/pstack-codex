# Codex runtime contract

Read this once when using any pstack skill. It supplies the host conventions for the bundled workflows.

## Scope and invocation

pstack is an on-demand toolkit. Installing it does not activate poteto-mode, change project instructions, create schedules, or authorize publishing. `$pstack` routes a request; `$poteto-mode` explicitly adopts the broader workflow for the current task. Read sibling skills by their paths relative to the loaded SKILL.md. A named workflow or principle is a reference to that sibling, not a requirement that it appear in the skill picker.

Follow the user's requested scope and the project's AGENTS.md. A playbook's commit, PR, merge, deployment, communication, or cleanup step applies only when authorized for this task. Do the preparatory work before asking for genuinely missing authorization. Never reset a dirty worktree, discard unrelated changes, or rewrite published history just to follow a playbook. Preserve configured Git identities and run the repository's identity checks before commits and GitHub writes. Skill installation grants none of those external actions.

## Delegation and models

Use the available Codex subagent tools when a selected workflow calls for delegates and session rules permit them. On the desktop these may be `collaboration.spawn_agent`, `send_message`, `followup_task`, and `wait_agent`; other Codex hosts expose their own schemas. Inspect the current tool schema. Do not send Cursor-only arguments such as `subagent_type`, `environment`, `cloud_base_branch`, `readonly`, or `run_in_background`.

Subagents share the filesystem. Give writers disjoint files or separate worktrees and exact base SHAs. Cloud VMs are not implied by a spawn. Queue excess work within the actual concurrency limit. Give read-only reviewers an explicit no-edits brief; it is a task constraint, not a tool flag. Supply the goal, scope, absolute instruction paths, expected output, and verification criteria in every brief. Read the resulting artifacts yourself.

Default every role to the parent model. Optional choices live in `${CODEX_HOME:-~/.codex}/pstack/models.json`, written by setup-pstack and loaded only during pstack work. Omit model and reasoning overrides unless explicitly configured and supported by the current spawn tool. With desktop collaboration, an override requires `fork_turns: "none"`; include a complete standalone brief. Never infer a valid model from a different provider's slug. If a configured model is unavailable, disclose it and inherit the parent. Independent runs of the same model are not multi-model evidence.

The files in `agents/` are prompt templates, not registered Codex agent types. For a poteto delegate, give it `agents/poteto-agent.md` and the absolute poteto-mode SKILL.md path. For a comment review, give it `agents/comment-sicko.md`. If delegation is unavailable or prohibited, perform the phases sequentially and report the loss of independent review. Do not launch nested `codex exec` sessions as a workaround.

## Host tools and durable work

- Use current shell, patch, plan, and clarification tools. A checklist in a task-local artifact can replace a missing plan tool. Ask for product choices only when evidence cannot resolve them.
- Discover connected tools through the host's tool catalog. Do not assume an MCP directory, Cursor team kit, browser controller, or secret-request API exists. Use an available matching skill, a project harness, or direct CLI/browser tools. Use Codex's skill-creator for skill authoring when available.
- Project skills belong in `.agents/skills/<name>/`; personal skills belong in `${CODEX_HOME:-~/.codex}/skills/<name>/`. Explicit-only skills use `agents/openai.yaml` with `policy.allow_implicit_invocation: false`.
- For a bounded task, keep working and poll the actual process or CI watcher in the current chat. Use goal tools only when the user requests a goal. A recurring future task requires the supported Automations tool and a user request for a schedule. Never turn a current PR watch into a scheduled automation. A durable progress file is evidence, not an automatic wake mechanism.
- Use `list_threads` and `read_thread` for Codex chat history, scoped to the active project and requested time window. Prefer the current conversation when it contains enough evidence. If those tools are absent, use a user-supplied export or clearly report the missing history; do not scan all private Codex sessions or guess transcript paths. Pass a scoped digest to delegates. Use `wait_threads` for existing user chats, and collaboration tools for subagents.
- If a long workflow mentions a Project tracker/store or an event subscription absent in this host, keep a task-local progress document and use available waits. Do not pretend background execution survives a stopped chat.
- A custom webhook UI needs a real supplied or provisioned endpoint. Codex does not gain Cursor webhook routines or secret cards through this plugin. `make-bot-ui` describes the supported alternative. The optional Benny recipes under `automations/benny/` are reference material, not installed schedules; start with their FOR_AGENTS.md only when requested.

## Bundled helpers

Run helpers from the installed skill's absolute path, with the target project as the working directory. The PR watcher uses `gh` and Node.js 22.18+ (or 23.6+). Its first run installs its locked npm runtime dependencies beside the helper. `--status-only` makes one read-only status pass. The plan checker runs with Node.js. The decision log and worktree audit use shell tools. The worktree audit does not mine private chat storage and never proves deletion safe from merge status alone.

Statechart retains the upstream Node/Bun/Deno launcher. Parsing and rendering need no model checker; live TLA+ checks also need Java and TLC, resolved by the helper through `mise` or explicit `JAVA` and `TLA2TOOLS` settings. Report unavailable optional dependencies when that workflow is requested. Do not claim verification that was not run.
