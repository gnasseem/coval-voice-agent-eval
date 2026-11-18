"""Conversation loop: caller and agent alternate until the caller says goodbye or 12 caller turns.

python run.py <persona-id> <config>      needs ANTHROPIC_API_KEY
python run.py --prompt <persona-id>      prints the prompts the subagent route used
"""
import sys

from agent import AGENT_SYSTEM
from caller import caller_system, load_persona
from llm import complete, save_transcript

MAX_TURNS = 12

# Used for the published runs: one subagent per conversation plays both sides, turn by turn,
# strictly in character, with no peeking at the other side's instructions when writing a line.
SUBAGENT_RULES = """Write a phone call transcript by playing BOTH roles in strict alternation, starting with the caller
(the agent's greeting is implied). Write each line as the role would, using only what that role knows: the caller never
sees the agent policy; the agent never sees the caller's goal or mood. Do not make the agent smarter or worse than a
typical model of your size would be; do not steer the call toward a tidy ending. Stop when the caller says goodbye or
after 12 caller turns. Save JSON to the given path: {"persona": id, "config": config, "turns": [{"role": "caller"|"agent", "text": str}], "ended": "caller_ended"|"max_turns"}."""


def booking_note(p):
    return f"BOOKING RECORD: {p['booking']}"


def converse(p, config):
    cs = caller_system(p)
    ag = AGENT_SYSTEM + "\n\n" + booking_note(p)
    turns = []
    ended = "max_turns"
    for _ in range(MAX_TURNS):
        # each side sees the other's lines as "user" and its own as "assistant"
        c_msgs = [{"role": "user", "content": "(The call connects. The agent greets you.)"}] if not turns else []
        for t in turns:
            c_msgs.append({"role": "user" if t["role"] == "agent" else "assistant", "content": t["text"]})
        c = complete(config_for_caller(), cs, c_msgs)
        turns.append({"role": "caller", "text": c})
        if "goodbye" in c.lower() or "bye" in c.lower().split():
            ended = "caller_ended"
            break
        a_msgs = [{"role": "user" if t["role"] == "caller" else "assistant", "content": t["text"]} for t in turns]
        turns.append({"role": "agent", "text": complete(config, ag, a_msgs)})
    return {"persona": p["id"], "config": config, "turns": turns, "ended": ended}


def config_for_caller():
    return "sonnet"  # the caller is held fixed so only the agent model varies


if __name__ == "__main__":
    if sys.argv[1] == "--prompt":
        p = load_persona(f"personas/{sys.argv[2]}.yaml")
        print(SUBAGENT_RULES + "\n\n--- AGENT ---\n" + AGENT_SYSTEM + "\n\n" + booking_note(p) + "\n\n--- CALLER ---\n" + caller_system(p))
    else:
        save_transcript(converse(load_persona(f"personas/{sys.argv[1]}.yaml"), sys.argv[2]))
