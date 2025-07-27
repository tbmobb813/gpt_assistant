import os
import time
import functools
import logging
from datetime import datetime
from pathlib import Path
import openai
from openai import OpenAI, OpenAIError
from .ollama_chat import chat_with_ollama
from .prompt import build_prompt
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def process_folder(
    folder: str,
    task: str,
    model: str,
    persona: str,
    client: OpenAI,
    use_local: bool,
    local_model: str
) -> List[Dict[str, Any]]:
    """
    Walks through files in `folder`, sends prompts to GPT (local or cloud),
    and returns a list of results with file name, reply, timestamp, and mode_str.
    """
    logger.info(f"Processing folder '{folder}' with task '{task}', model '{model}', persona '{persona}'")
    history = []
    outputs = []

    # Retry decorator for OpenAI API calls
    def retry(exceptions, tries=3, delay=1, backoff=2):
        def decorator(func):
            @functools.wraps(func)
            def wrapped(*args, **kwargs):
                mtries, mdelay = tries, delay
                while mtries > 1:
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        logger.warning(f"{e}, retrying in {mdelay}s...")
                        time.sleep(mdelay)
                        mtries -= 1
                        mdelay *= backoff
                return func(*args, **kwargs)
            return wrapped
        return decorator

    @retry((OpenAIError,), tries=3, delay=1, backoff=2)
    def call_openai(prompt):
        response = client.chat.completions.create(
            model=model,
            messages=history + [{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content

    for root, _, files in os.walk(folder):
        for file in files:
            if not file.endswith((".txt", ".md", ".py", ".js")):
                continue

            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            prompt = build_prompt(task, content, persona)
            logger.debug(f"Built prompt for file {file}")

            try:
                logger.debug(f"Sending to {'Ollama' if use_local else 'OpenAI'} for file {file}")
                if use_local:
                    reply = chat_with_ollama(prompt, model=local_model, history=history)
                else:
                    reply = call_openai(prompt)
            except OpenAIError as e:
                logger.error(f"OpenAI API error for file '{file}': {e}")
                reply = f"❌ API Error: {str(e)}"
            except Exception as e:
                logger.error(f"Unexpected error for file '{file}': {e}")
                reply = f"❌ Error: {str(e)}"

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            mode_str = "🟢 OpenAI" if not use_local else "🧠 Ollama"

            outputs.append({
                "file": file,
                "reply": reply,
                "timestamp": timestamp,
                "mode_str": mode_str
            })

            history += [{"role": "user", "content": prompt}, {"role": "assistant", "content": reply}]

    return outputs
