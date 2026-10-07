# Install

Claude Code, Codex CLI, and Grok install distill from a marketplace. Copilot CLI reads the `.claude-plugin` marketplace in this repository. Cursor and Gemini CLI use the commands at the end of this page.

The short command installs distill with `npx skills`. It needs Node.js. To install for one agent, add `-a <agent>`, for example `-a cursor`.

```sh
npx skills add jahunkoo/skills --skill distill
```

`npx skills update` compares the skill folder's git tree SHA, not the version string (skills 1.7.0). Removal: untested.

The blocks below are marketplace installs for Claude Code, Codex CLI, Grok, and Copilot CLI. Cursor and Gemini CLI follow them.

## Claude Code

```sh
claude plugin marketplace add jahunkoo/skills
claude plugin install distill@jahunkoo-skills
```

Invocation: `/distill:distill` (or `/distill` if no other command uses that name).

Update: `claude plugin marketplace update jahunkoo-skills`, then `claude plugin update distill@jahunkoo-skills`. Update follows the version string.

Remove: `claude plugin uninstall distill@jahunkoo-skills`.

## Codex CLI

```sh
codex plugin marketplace add jahunkoo/skills
codex plugin add distill@jahunkoo-skills
```

Invocation: `$distill:distill`. A copy installed as a skill, rather than as this plugin, is invoked as `$distill`.

Update: a Git marketplace upgrades at session start whether or not the version string changed. To upgrade by hand, run `codex plugin marketplace upgrade jahunkoo-skills`. To pin the marketplace to the published tag:

```sh
codex plugin marketplace add jahunkoo/skills --ref distill-v1.1.0
```

Remove: `codex plugin remove distill@jahunkoo-skills`.

## Grok

```sh
grok plugin marketplace add jahunkoo/skills
grok plugin install distill --trust
```

`--trust` is required. Install the bare name `distill`. The qualified name `distill@jahunkoo-skills` is not accepted.

Grok's marketplace list shows the repository's directory name. For this repository that name is `skills`, not `jahunkoo-skills`.

Invocation: `/distill`. If the plugin and a user skill are both installed, the names become `/user:distill` and `/distill:distill`.

Update: at session start, when the `plugin.json` version string changes. Manual `grok plugin update distill` takes the bytes at HEAD.

Remove: `grok plugin uninstall distill`.

## Copilot

Copilot CLI 1.0.91 reads `.claude-plugin/marketplace.json`. This repository does not ship a separate Copilot marketplace file.

```sh
copilot plugin marketplace add jahunkoo/skills
copilot plugin install distill@jahunkoo-skills
```

Use the qualified name `distill@jahunkoo-skills`. Session invocation, update, and removal are untested.

## Cursor

```sh
npx skills add jahunkoo/skills --skill distill -a cursor
```

This path does not use a marketplace file. Session invocation: untested.

## Gemini CLI

Untested.

```sh
gemini skills install https://github.com/jahunkoo/skills.git --path skills/distill --scope user --consent
```

Gemini CLI has no skill update command. To update, uninstall the skill and install it again.
