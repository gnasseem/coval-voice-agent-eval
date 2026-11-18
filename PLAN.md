# Plan

Independent project, not affiliated with Coval. Text-level evaluation of a customer-support voice agent: simulated callers, an agent under test, an LLM judge.

## How model calls run

The `claude` CLI is signed out on this machine and there is no API key, so the network lane runs every caller, agent and judge turn through its own Claude subagents (Agent tool, models haiku, sonnet and opus) and saves the transcripts under `runs/`. The code reads `ANTHROPIC_API_KEY` for anyone re-running it; the README says how the published results were produced.

## Checklist

- [ ] `llm.py`: one call wrapper, Anthropic SDK with `ANTHROPIC_API_KEY`; transcripts from the subagent route saved in the same JSON shape
- [ ] 30 to 50 caller personas in `personas/*.yaml` (goal, mood, disfluencies, interruptions, ambiguity)
- [ ] `agent.py`: airline rebooking agent with a fixed system prompt and policy
- [ ] `caller.py`: LLM-driven simulated caller
- [ ] `run.py`: conversation loop for 2 to 3 model configurations
- [ ] Verify harness on 3 conversations before the full run
- [ ] `judge.py`: scores task success, policy adherence, conversation recovery
- [ ] Full run, write `results.csv`
- [ ] `FINDINGS.md`: one page, only what the run produced
- [ ] `README.md`: what it does, how to run it, what it found
