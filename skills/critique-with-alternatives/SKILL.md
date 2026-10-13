---
name: critique-with-alternatives
description: 'Critique a plan or a risky request before it runs: test its premises against the repository, judge it on evidence rather than on what anyone prefers, and replace each flaw with a concrete better way, ending with a one-line verdict. Use when the user asks for a critique or a second look at a plan ("critique this", "is this a good idea?", "think this through first"), and before carrying out a request that is hard to undo or reaches beyond the files at hand (deleting or migrating data, a public interface, shared configuration, CI, production), even when the user just says to do it. Not for small changes that are easy to revert, or for reviewing finished work such as code, a pull request, a document or a design.'
license: MIT
metadata:
  version: "2.0.0"
---

# critique-with-alternatives

Review a plan before it runs, judge it on **evidence**, and hand back a **better way** for every flaw you keep. The aim is the user's goal, reached safely: a critique that stops at "this is risky" is half done, and one that flatters the plan, or your own taste, is no critique.

## Steps

1. **Pin the target and the goal.** The target is the plan or request the user points to; a concern they add sets the focus, not the target. With no pointer, take the most recent plan in the conversation, including one you proposed; if you cannot tell which one is meant, or it is gone, ask. Open with one line naming the target. Take the goal as stated, and question it only when it rests on a false premise. If no goal is stated anywhere, say so, and state your assumption only when the verdict turns on it.
2. **Test every premise against the repository.** Facts are your job, decisions are the user's: read the code, configuration and history, and run read-only commands, before you judge. List what must be true for the plan to work and everything it changes, and trace each change to whatever reads or relies on it. Mark each premise true, false or unknown, and **ground** each finding in a file, line, commit or command output. The step is done when no premise is unmarked and no changed thing is untraced.
3. **Judge on evidence.** An **objection** is a false premise, or a risk you can show happens here, weighed by how likely and how costly it is. The user's confidence, deadline or own checks leave a checkable claim unchecked, and a repeated request is the same evidence again. Your own taste counts only when the plan misses its goal or carries a grounded risk. When no objection survives, say the plan is sound and give the one or two grounded reasons.
4. **Repair each objection with a better way.** Say what to change, where, and which step of the plan it replaces. Match the objection to the patterns below; they repair objections from step 3 and never add new ones. Then run the better way through step 2: it reaches the goal and brings no false premise or risk of its own. If no better way exists, say so. Put nice-to-haves under **Optional**, apart from what the plan needs.
5. **Finish** as the endings below say for what the user asked.

## Better-way patterns

- **Reuse what exists.** _Use when_ the plan builds a check, script, helper or rule. Search the repository first; one that exists but is unwired, stale or broken is the finding, and wiring or fixing it is the better way.
- **Ratchet.** _Use when_ a new check or rule meets code that already breaks it. Check only what is added or changed (the staged files, the lines a pull request adds), so existing code passes untouched and every new line is held to the rule, with no list to maintain. An exemption list or a scope that skips where violations live also lets new violations in there.
- **Measure, then block.** _Use when_ a new check will fail builds or block merges. Run it over the current tree and review what it flags before it blocks; start it as a warning when the hits are many or noisy.
- **Expand, then contract.** _Use when_ the plan removes or renames something others read: a table, column, field, endpoint, export or configuration key. Add the new beside the old, move every reader, and remove the old in a later step.
- **Keep the contract.** _Use when_ the change touches a public interface or data already stored. Change the internals; keep the shape that callers and stored data rely on.
- **Fix the source.** _Use when_ the plan cleans up something a tool, script or process keeps producing. Change the producer as well, so the cleanup holds.
- **Split by need.** _Use when_ one setting covers parts with different requirements, such as retention, limits, permissions or timeouts. Give each part the value it needs.
- **Undo first.** _Use when_ the plan deletes data, migrates, deploys or sends. Put a dry run, flag, backup or staged rollout before the step that cannot be undone, and name that step.

When no pattern fits, derive the better way from the objection itself and hold it to the same check.

## Endings

Choose the ending by what the user asked for. A message that asks for a review, a critique or your opinion is a critique, even when it spells out the change: the user wants the verdict before the change.

- **A critique.** End with a one-line **verdict**: proceed; proceed with changes, naming only the changes the plan needs; or stop, naming what to do instead. Then ask one question worded so that "yes" accepts your verdict, and stop. Until the user says yes, the repository stays as you found it: reading, searching, read-only commands, and writing the critique where the user asked for it are the whole job. Asking for the critique, agreeing with it, or your own verdict is not that yes.
- **The work itself.** With no objection, do it as asked. With an objection and a better way that reaches the goal, do the better way when your own part is easy to undo (file edits or a local commit; deleting data, deploying and sending are not), and say plainly what you changed from the request and why. The user's explicit choices stand, so change only what the objection requires. Otherwise give the verdict and the better way, ask, and stop.
- **No one can reply** (a non-interactive run, a subagent, CI): end with the verdict, or with what is missing, where you would ask.
