# Security policy

## Supported versions

Security fixes target the latest published pstack-codex release. Older releases do not receive separate security updates. See the [releases page](https://github.com/robansuini/pstack-codex/releases) for the current version.

## Reporting a vulnerability

Please [report a vulnerability privately through GitHub](https://github.com/robansuini/pstack-codex/security/advisories/new). Do not include vulnerability details or credentials in a public issue or pull request before a fix or coordinated disclosure.

Include the affected release or commit, Codex version, operating system, reproduction steps, expected and observed behavior, and potential impact. Remove secrets, personal information, and private project data from examples and logs. A minimal reproduction using synthetic data is preferred.

Reports may cover the Codex adaptation, bundled helper scripts, or skill instructions that could cause unintended access or actions. If the problem originates in upstream pstack, the maintainer will coordinate with the upstream project as appropriate. This is a community-maintained project; no response-time guarantee or bug bounty is offered.

## Using pstack safely

Review skill instructions and commands before running them in a sensitive project. Keep Codex permissions and your project's instructions appropriate for that project. Skills run with the tools and access available to your Codex session; installing this plugin does not provide a separate security boundary.

Install from this repository and review release notes before updating. Repository protections and passing CI reduce risk but do not guarantee that generated code or agent actions are safe for every project.
