---
name: poteto-help
description: Explain pstack for Codex, choose a workflow, and give invocation examples without starting work when the user only asks for help.
---

# pstack help

Read [the Codex runtime contract](../../CODEX.md) once. Answer help questions directly. If the user requests action, route to the relevant skill and perform it.

## Use it

Invoke `$pstack` with a task for routing, or choose a skill below. `$poteto-mode` adopts the full playbook for the requested task. Every skill is explicit-only; installation adds no project instructions, Custom Modes, schedules, or automatic behavior. In a picker that namespaces plugins, select the pstack entry for the named skill.

No model setup is required. All roles inherit the active Codex model. `$setup-pstack` can configure optional supported per-role choices, read only during pstack work. Independent parent-model reviews are not multi-model reviews. Available subagent slots bound parallelism; writers need separate worktrees or disjoint files.

Use [the runtime contract](../../CODEX.md) for host differences and optional helper requirements. Read the actual linked skill before answering detailed questions about it. Link local installed files for Codex-specific behavior; upstream URLs describe the original plugin and may differ.

## Skills

| The user wants to | Skill |
|---|---|
| Do any non-trivial task with rigor | [`$poteto-mode`](../poteto-mode/SKILL.md) |
| Check that the agent understood their goal and the problem before it starts | [`$in-your-own-words`](../in-your-own-words/SKILL.md) |
| Get a prompt rewritten deeper, not bigger, before sending it: what a top professional would add, their raw material and methods, and an outside check. It returns the prompt and doesn't do the task | [`$sharpen`](../sharpen/SKILL.md) |
| Know how code works now, or where new code should live | [`$how`](../how/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`$why`](../why/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`$teach`](../teach/SKILL.md) |
| Catch up on their own recent work on a topic | [`$recall`](../recall/SKILL.md) |
| Catch up on what changed in this chat since their last message, in plain words and small visuals, with every item waiting on them listed and decidable from the reply alone | [`$ketchup`](../ketchup/SKILL.md) |
| Catch up like `$ketchup`, in a short subtitled video of slides, with the waiting calls as text under it | [`$ketchup-video`](../ketchup-video/SKILL.md) |
| Know what a small diff could break outside itself | [`$blast-radius`](../blast-radius/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`$architect`](../architect/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`$arena`](../arena/SKILL.md) |
| Run parallel checks over slices, or race workers, as cloud agents | [`$swarm`](../swarm/SKILL.md) |
| Have different models review a diff and try to break it | [`$interrogate`](../interrogate/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`$tdd`](../tdd/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`$typescript-best-practices`](../typescript-best-practices/SKILL.md) |
| Strip comments before review, using a reviewer that didn't write them | [`$no-comments`](../no-comments/SKILL.md) |
| Clean AI tells out of prose | [`$unslop`](../unslop/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`$technical-writing`](../technical-writing/SKILL.md) |
| Hear the last reply again in plain words | [`$bro`](../bro/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`$create-verification-skill`](../create-verification-skill/SKILL.md) |
| Bring a verification skill and its feature map back in line with the app | [`$maintain-verification-skill`](../maintain-verification-skill/SKILL.md) |
| Formally verify a race, invariant, or other property that tests rarely reach | [`$create-formal-verification-skill`](../create-formal-verification-skill/SKILL.md) |
| Bring a formal verification back in line after the code it covers changed, and learn whether a failure is drift or a bug | [`$maintain-formal-verification-skill`](../maintain-formal-verification-skill/SKILL.md) |
| Show a PM or designer what the user sees as a chart checked by a TLA+ model, with the shortest path to each state that breaks a rule | [`$statechart`](../statechart/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`$benchmark-checklist`](../benchmark-checklist/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`$figure-it-out`](../figure-it-out/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`$show-me-your-work`](../show-me-your-work/SKILL.md) |
| Pick a model for each role and a reasoning budget | [`$setup-pstack`](../setup-pstack/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`$automate-me`](../automate-me/SKILL.md) |
| Turn what a finished task taught into skill edits | [`$reflect`](../reflect/SKILL.md) |
| Stop agents from repeating the same mistakes in this repo | [`$correct`](../correct/SKILL.md) |
| Build a page whose buttons wake a Grok Bot over a webhook | [`$make-bot-ui`](../make-bot-ui/SKILL.md) |
| Find their way around pstack | `$poteto-help` |

If a skill directory next to this one is missing from the table, read its frontmatter and route by its description. The `principle-*` directories are covered under principles below.

Close calls:

- `$how` explains what the code does. `$why` explains the reasons. `$teach` runs one or both and explains the result plainly.
- `$arena` gives every worker the same brief and merges the best parts. `$swarm` splits work into slices or a race and returns one report.
- `$architect` implements right after it settles the design. Add "with checkpoint" to review the design before it writes code.
- `$interrogate` reviews the diff. `$blast-radius` looks for breakage outside the diff and proves the one fact that makes the change safe.
- `$recall` rebuilds context across recent chats. `$ketchup` covers only this chat since the user's last message. Resuming one specific chat or branch is the Session pickup playbook.
- `$figure-it-out` designs one rigorous run. The Orchestrate playbook runs a program that spans days and many PRs. The Autonomous run playbook drives one task to a finish condition.


## Playbooks and principles

[poteto-mode](../poteto-mode/SKILL.md) lists the playbooks and principles. Describe the task to choose a playbook, for example `$poteto-mode check PR 123` or `$poteto-mode plan this migration`. A status check does not authorize a merge. Read-only requests remain read-only.

For long work, state the goal and observable finish condition. Codex watches the current task using available wait tools. Installation does not create future wakeups. Use the supported Automations tools only when the user requests a recurring schedule.

## Customize

Use [automate-me](../automate-me/SKILL.md) to create a personal style skill and [reflect](../reflect/SKILL.md) to propose lessons from this chat. Edit the maintained source rather than plugin cache files, then reinstall the plugin. Use project verification skills for app-specific runtime evidence.

Give one concrete invocation example appropriate to the user's question. Do not require setup or a preference interview to answer a narrow help request.
