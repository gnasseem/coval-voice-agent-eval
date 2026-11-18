"""The simulated caller: a persona (personas/*.yaml) turned into a system prompt."""
import yaml

CALLER_RULES = """You are role-playing a phone caller to an airline. Stay in character. Speak as people speak on a phone:
short turns (1 to 3 sentences), include the disfluencies and interruptions listed, never mention you are an AI or a simulation.
Reveal your goal gradually, not all at once. Do not accept anything that clearly breaks your stated constraints.
End the call yourself (say goodbye) once resolved, or when you have given up."""


def load_persona(path):
    with open(path) as f:
        return yaml.safe_load(f)


def caller_system(p):
    return (
        f"{CALLER_RULES}\n\nWho you are: {p['who']}\nYour goal: {p['goal']}\nMood: {p['mood']}\n"
        f"Speech habits: {p['disfluencies']}\nInterruptions: {p['interruptions']}\n"
        f"Ambiguity: {p['ambiguity']}\nYour booking: {p['booking']}"
    )
