# Plan

Independent project, not affiliated with Coval. Text-level evaluation of a customer-support voice agent: simulated callers, an agent under test, an LLM judge.

## Blocker

The `claude -p --model haiku` CLI is installed but not logged in (`claude auth status` reports `loggedIn: false`), so no LLM call can run. Nothing below was started. Log in once on this machine, then continue from the first box.

## Checklist

- [ ] Verify `claude -p --model haiku|sonnet|opus` works via subprocess
- [ ] 30 to 50 caller personas in `personas/*.yaml` (goal, mood, disfluencies, interruptions, ambiguity)
- [ ] `agent.py`: airline rebooking agent with a fixed system prompt and policy
- [ ] `caller.py`: LLM-driven simulated caller
- [ ] `run.py`: conversation loop for 2 to 3 model configurations
- [ ] Verify harness on 3 conversations before the full run
- [ ] `judge.py`: scores task success, policy adherence, conversation recovery
- [ ] Full run, write `results.csv`
- [ ] `FINDINGS.md`: one page, only what the run produced
- [ ] `README.md`: what it does, how to run it, what it found
