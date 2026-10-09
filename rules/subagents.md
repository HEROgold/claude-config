# Subagents get a surgical brief and stick to it

A subagent starts from the brief it is given. Rereading the codebase or the docs every time one is spawned costs time and tokens, and it pulls the agent away from its task.

## When you write a brief

- Put the facts in the brief: the decisions already made, the files to change with their paths, the signatures and snippets the agent needs, and the exact behaviour expected.
- Give one surgical task with a clear end: what to change, what not to touch, and how to check it is done.
- Name each file the agent may read. Don't tell it to "read all of X first".
- If the agent needs a fact you don't have, look it up yourself before spawning, or name the one file that holds it.

## When you are the subagent

- The brief is your context. Trust it, and don't re-explore the codebase or reread the docs to rebuild it.
- Read only the files you are about to change, plus any file the brief names. Read only the part you need.
- Stay inside the task. Don't fix, refactor or "improve" anything the brief doesn't ask for.
- If the brief is missing a fact you can't do the task without, stop and ask for it in your report. Don't go searching for it.
