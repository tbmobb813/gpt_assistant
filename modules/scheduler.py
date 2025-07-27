import os
import json
import logging
from datetime import datetime

QUEUE_FILE = os.path.join(os.path.dirname(__file__), '..', 'post_queue.json')
logger = logging.getLogger(__name__)

def load_queue():
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, 'r') as f:
            queue = json.load(f)
            logger.debug(f"Loaded queue with {len(queue)} items")
            return queue
    logger.debug("Queue file not found, returning empty queue")
    return []

def save_queue(queue):
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=2)
    logger.info(f"Saved queue with {len(queue)} posts")

def queue_post(content, platform="Instagram", tags=None, scheduled_for=None):
    post = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "platform": platform,
        "content": content.strip(),
        "tags": tags or [],
        "scheduled_for": scheduled_for
    }
    queue = load_queue()
    queue.append(post)
    save_queue(queue)
    logger.info(f"Queued post '{post['id']}' for platform {platform}")
    return f"✅ Post queued for {platform}!"

def get_scheduled_posts():
    posts = load_queue()
    logger.debug(f"Retrieved {len(posts)} scheduled posts")
    return posts

def format_queue_for_display():
    queue = load_queue()
    lines = []
    for post in queue:
        line = f"[{post.get('platform')}] {post.get('scheduled_for') or 'Unscheduled'} — {post.get('content')[:50].replace(chr(10), ' ')}..."
        lines.append(line)
    logger.debug(f"Formatted {len(lines)} lines for display")
    return lines, queue

