import json
import os
import logging

SNIPPET_FILE = os.path.join(os.path.dirname(__file__), '..', 'snippets.json')
logger = logging.getLogger(__name__)

def load_snippets():
    if not os.path.exists(SNIPPET_FILE):
        return {}
    try:
        with open(SNIPPET_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding snippets file: {e}")
        return {}

def save_snippets(snippets):
    try:
        with open(SNIPPET_FILE, 'w') as f:
            json.dump(snippets, f, indent=2)
        logger.info(f"Saved {len(snippets)} snippets")
    except OSError as e:
        logger.error(f"Error writing snippets file: {e}")
        raise

def save_snippet(name, content):
    try:
        snippets = load_snippets()
        snippets[name] = content
        save_snippets(snippets)
        return f"✅ Snippet '{name}' saved."
    except Exception as e:
        logger.error(f"Failed to save snippet '{name}': {e}")
        return f"❌ Failed to save snippet '{name}': {e}"

def get_snippet(name):
    snippets = load_snippets()
    return snippets.get(name, f"❌ Snippet '{name}' not found.")

def list_snippets():
    snippets = load_snippets()
    return list(snippets.keys())
    
def search_snippets(query):
    query = query.lower()
    matches = []
    snippets = load_snippets()
    for name, content in snippets.items():
        if query in name.lower() or query in content.lower():
            matches.append((name, content))
    return matches


