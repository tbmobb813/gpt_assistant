import os
import pytest  # pylint: disable=import-error
import json
import pytest
from modules import scheduler

@ pytest.fixture(autouse=True)
def temp_queue_file(tmp_path, monkeypatch):
    # Redirect QUEUE_FILE path to a temp file
    temp_file = tmp_path / 'post_queue.json'
    monkeypatch.setattr(scheduler, 'QUEUE_FILE', str(temp_file))
    # Ensure file does not exist at start
    if temp_file.exists():
        temp_file.unlink()
    return temp_file


def test_load_queue_empty(temp_queue_file):
    # When file is missing, load_queue returns empty list
    data = scheduler.load_queue()
    assert data == []


def test_queue_post_and_load(temp_queue_file):
    # Queue a post and verify it is saved and loaded correctly
    result = scheduler.queue_post("content here", platform="TestPlat", tags=["a","b"], scheduled_for="2025-07-27")
    assert "✅ Post queued for TestPlat!" in result
    loaded = scheduler.load_queue()
    assert len(loaded) == 1
    post = loaded[0]
    assert post['platform'] == "TestPlat"
    assert post['content'] == "content here"
    assert post['tags'] == ["a","b"]
    assert post['scheduled_for'] == "2025-07-27"


def test_format_queue_for_display(temp_queue_file):
    # Pre-populate queue file
    sample = [{"platform": "IG", "content": "hello world", "scheduled_for": None}]
    temp_queue_file.write_text(json.dumps(sample))
    lines, data = scheduler.format_queue_for_display()
    assert isinstance(lines, list)
    assert len(lines) == 1
    assert "hello world" in lines[0]
    assert data == sample
