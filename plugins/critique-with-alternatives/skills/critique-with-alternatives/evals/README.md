# Evaluation of critique-with-alternatives 2.0.0

Evaluated SKILL.md sha256: `139b781aa444e5bc8ed0bffed062503fb58a774edd9e3e673bfe10b187050a41`. This file's sha256 is `422c55a5db69f897e239faec355c2c296f6ad1ac9176910b1400de5f05998d38`: the only difference is that the `description` value is now in single quotes, so the frontmatter is valid YAML; the name, description text and body are the same.

Confirmation run iteration-6 (2026-10-13), 12 held-out cases, three agents (Claude Code, Codex CLI, Grok CLI), with and without the skill, one run per case and arm: outcome pass rate 100% with the skill and 59% without, +41 points (95% CI +26 to +59, p = 0.00049); every agent meets the criteria (Grok CLI as weak evidence). The difference comes from review requests: with the skill, the agent stops at the review instead of making the change.

`triggers.json` holds the trigger-test queries: every agent loaded the skill on 12 of 12 requests it should load for, and on at most 1 of 10 it should not.

Full results, weaknesses, cost and limits: `workspaces/critique-with-alternatives-workspace/README.md` in the repository this skill comes from.
