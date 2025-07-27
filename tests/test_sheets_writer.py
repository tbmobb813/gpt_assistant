import pytest
from modules.sheets_writer import append_post, get_all_posts

class DummySheet:
    def __init__(self):
        # Header + a row
        self._values = [["Content","Platform","Tags","Status"], ["hello","IG","tag1, tag2","Idea"]]
        self.rows = []
    def append_row(self, row):
        self.rows.append(row)
    def get_all_values(self):
        return self._values

@pytest.fixture(autouse=True)
def dummy_connect(monkeypatch):
    import modules.sheets_writer as sw
    monkeypatch.setattr(sw, 'connect_to_sheet', lambda name, ws="Sheet1": DummySheet())
    yield


def test_append_post():
    result = append_post("sheet", "hi there", "FB", ["a","b"], "Draft")
    assert result.startswith("✅"), "append_post should return success message"


def test_get_all_posts():
    posts = get_all_posts("sheet")
    assert isinstance(posts, list), "get_all_posts should return a list"
    assert posts and isinstance(posts[0], dict)
    assert posts[0]["Content"] == "hello"
