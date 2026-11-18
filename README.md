# coval-voice-agent-eval

An independent, small project: text-level evaluation of a phone rebooking agent. Simulated callers with different moods, speech habits and ambiguity talk to an agent with a fixed airline policy, and an LLM judge scores each call on task success, policy adherence and conversation recovery. Not affiliated with or endorsed by Coval; built only on public ideas about voice-agent simulation and evaluation. Text only, no audio.

- `personas/*.yaml`: 33 callers (goal, mood, disfluencies, interruptions, ambiguity, booking record), including identity-probing, prompt-injection and policy-inventing callers.
- `agent.py`: the agent under test, a Skyline Air (fictional) rebooking agent with a fixed system prompt and policy.
- `caller.py`: turns a persona into the caller's system prompt.
- `run.py`: the conversation loop (caller and agent alternate, one config per run).
- `judge.py`: grading prompt, and `--csv` to join everything into `results.csv`.
- `llm.py`: the single model-call wrapper and the transcript JSON shape. `runs/transcripts/` and `runs/judge/` hold the outputs.

## Run it

```
pip install anthropic pyyaml
export ANTHROPIC_API_KEY=...
python run.py easy-fee-economy haiku     # one conversation -> runs/transcripts/
python judge.py runs/transcripts/easy-fee-economy__haiku.json
python judge.py --csv                    # -> results.csv
```

## How the published results were produced

No API key was used. Each conversation was written by one Claude subagent (haiku or sonnet, the "config") given the prompts from `python run.py --prompt <id>` and instructed to play both roles turn by turn with only each role's knowledge; each transcript was graded by an Opus subagent using `python judge.py --prompt <file>`. So in the published runs one model wrote both sides of each call, which differs from `run.py`'s loop of separate calls, and the caller is not held fixed across configs as it is in the code. Re-running with a key gives the independent-call version.

## What it found

See `FINDINGS.md`: sonnet 32/33 task success vs haiku 28/33 in this single run, with haiku inventing policy and disclosing a booking to a third party once. Small sample, one run, no human labels.
