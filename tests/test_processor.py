import os
import json
import pytest
from pathlib import Path
from modules.processor import process_folder

class DummyResponse:
    def __init__(self, content):
        self.choices = [type("c", (), {"message": type("m", (), {"content": content})})()]

class DummyClient:
    def __init__(self, reply):
        self.reply = reply
        self.chat = self
n    def completions(self):
        pass

    def create(self, model, messages, temperature):
        return DummyResponse(self.reply)

@pytest.fixture
def tmp_folder(tmp_path, monkeypatch):
    # create a directory with a sample file
    folder = tmp_path / "data"
    folder.mkdir()
    file1 = folder / "file1.txt"
    file1.write_text("hello world")
    # monkeypatch client
    dummy_client = DummyClient("openai_reply")
    return folder, dummy_client

def test_process_folder_openai(tmp_folder):
    folder, client = tmp_folder
    outputs = process_folder(str(folder), task="Summarize", model="gpt-3.5", persona="Default", client=client, use_local=False, local_model="")
    assert len(outputs) == 1
    out = outputs[0]
    assert out['reply'] == 'openai_reply'
    assert out['file'] == 'file1.txt'


def test_process_folder_local(tmp_folder, monkeypatch):
    folder, client = tmp_folder
    # monkeypatch chat_with_ollama
    import modules.processor as proc
    monkeypatch.setattr(proc, 'chat_with_ollama', lambda prompt, model, history: 'ollama_reply')
    outputs = process_folder(str(folder), task="Summarize", model="", persona="Default", client=None, use_local=True, local_model="tiny")
    assert len(outputs) == 1
    assert outputs[0]['reply'] == 'ollama_reply'
