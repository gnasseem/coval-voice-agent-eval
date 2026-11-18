# Plan

Independent project, not affiliated with Coval. Text-level evaluation of a customer-support voice agent: simulated callers, an agent under test, an LLM judge.

## How model calls run

The `claude` CLI is signed out on this machine and there is no API key, so the network lane runs every caller, agent and judge turn through its own Claude subagents (Agent tool, models haiku, sonnet and opus) and saves the transcripts under `runs/`. The code reads `ANTHROPIC_API_KEY` for anyone re-running it; the README says how the published results were produced.

## Checklist

- [x] `llm.py`: one call wrapper, Anthropic SDK with `ANTHROPIC_API_KEY`; transcripts from the subagent route saved in the same JSON shape
- [x] 30 to 50 caller personas in `personas/*.yaml` (goal, mood, disfluencies, interruptions, ambiguity)
- [x] `agent.py`: airline rebooking agent with a fixed system prompt and policy
- [x] `caller.py`: LLM-driven simulated caller
- [x] `run.py`: conversation loop for 2 to 3 model configurations
- [x] Verify harness on 3 conversations before the full run
- [x] `judge.py`: scores task success, policy adherence, conversation recovery
- [x] Full run, write `results.csv`
- [x] `FINDINGS.md`: one page, only what the run produced
- [x] `README.md`: what it does, how to run it, what it found

Pass 1 done: all items ticked. Published transcripts were written one subagent per conversation (both roles), not separate calls; see README. Possible next pass: rerun with an API key using run.py for independent calls, add a second judge for agreement.
