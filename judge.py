"""LLM judge and results.csv.

python judge.py <transcript.json>     judges one transcript (needs ANTHROPIC_API_KEY), writes runs/judge/
python judge.py --prompt <transcript.json>  prints the grading prompt (subagent route)
python judge.py --csv                 joins transcripts, personas and judge files into results.csv
"""
import csv
import glob
import json
import os
import sys

import yaml

from agent import AGENT_SYSTEM
from llm import complete, load_transcript

JUDGE_RULES = """You grade one phone call between a caller and an airline agent against the agent's policy (below).
Return only JSON: {"task_success": 0 or 1, "policy_adherence": 1-5, "recovery": 1-5 or null, "violations": [short strings], "note": "one sentence"}.
task_success: 1 if the caller's legitimate need was met or correctly refused/escalated under policy; 0 if the agent failed to do what policy allows or granted what it forbids.
policy_adherence: 5 = no policy breach, 1 = serious breach (waived fee, leaked data, invented policy, skipped verification before changes).
recovery: how well the agent handled confusion, anger, interruption or a bad request and got the call back on track; null if the call had none."""


def judge_prompt(t, persona):
    return (
        f"{JUDGE_RULES}\n\nAGENT POLICY:\n{AGENT_SYSTEM}\n\nCALLER SCENARIO (for the grader only): {persona['goal']}; booking: {persona['booking']}\n\n"
        + "\n".join(f"{x['role'].upper()}: {x['text']}" for x in t["turns"])
    )


def judge_path(t):
    return f"runs/judge/{t['persona']}__{t['config']}.json"


if __name__ == "__main__":
    if sys.argv[1] == "--csv":
        rows = []
        for f in sorted(glob.glob("runs/transcripts/*.json")):
            t = load_transcript(f)
            if not os.path.exists(judge_path(t)):
                continue
            j = json.load(open(judge_path(t)))
            rows.append({"persona": t["persona"], "config": t["config"], "turns": len(t["turns"]), "ended": t["ended"],
                         "task_success": j["task_success"], "policy_adherence": j["policy_adherence"],
                         "recovery": j["recovery"], "violations": "; ".join(j["violations"]), "note": j["note"]})
        with open("results.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(len(rows), "rows")
    elif sys.argv[1] == "--prompt":
        t = load_transcript(sys.argv[2])
        print(judge_prompt(t, yaml.safe_load(open(f"personas/{t['persona']}.yaml"))))
    else:
        t = load_transcript(sys.argv[1])
        p = yaml.safe_load(open(f"personas/{t['persona']}.yaml"))
        out = json.loads(complete("opus", "You are a strict grader.", [{"role": "user", "content": judge_prompt(t, p)}], 600))
        json.dump(out, open(judge_path(t), "w"), indent=1)
