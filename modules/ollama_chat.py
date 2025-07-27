import requests
import json

def chat_with_ollama(message, model="tinyllama", history=None):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": (history or []) + [{"role": "user", "content": message}],
        "stream": True
    }

    try:
        response = requests.post(url, json=payload, stream=True)
        full_reply = ""

        for line in response.iter_lines():
            if not line:
                continue
            try:
                data = json.loads(line.decode("utf-8"))
                chunk = data.get("message", {}).get("content", "")
                full_reply += chunk
            except Exception as e:
                return f"❌ Parse error: {str(e)}"

        return full_reply or "⚠️ No reply generated."
    except Exception as e:
        return f"❌ Ollama error: {str(e)}"

