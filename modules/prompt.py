from typing import Any


def build_prompt(task: str, content: str, persona: str) -> str:
    """
    Construct a GPT prompt based on the given task and persona.
    """
    base_prompts = {
        "Summarize": "Summarize this file:\n\n{}",
        "Explain": "Explain the following code or text to a beginner:\n\n{}",
        "Rewrite": "Rewrite this to be more clear and professional:\n\n{}"
    }
    prompt = base_prompts.get(task, "{}").format(content)

    if persona == "IG Copywriter":
        prompt = "Format this for Instagram captions with emojis, short lines, and a relatable tone:\n\n" + prompt
    elif persona == "NixLevel Hustler":
        prompt = "Rewrite this in a confident, motivational tone like a hustler giving life advice:\n\n" + prompt
    elif persona == "Jason the Dev":
        prompt = "Add inline code comments and explain it like you're mentoring a junior dev:\n\n" + prompt

    return prompt
