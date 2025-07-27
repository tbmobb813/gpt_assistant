import os
import json
import pytest
from modules.snippets import load_snippets, save_snippet, get_snippet, list_snippets, search_snippets, save_snippets

TEST_FILE = os.path.join(os.path.dirname(__file__), 'test_snippets.json')

@pytest.fixture(autouse=True)
def setup_snippet_file(tmp_path, monkeypatch):
    # Redirect SNIPPET_FILE to a temp location
    file_path = tmp_path / 'snippets.json'
    file_path.write_text(json.dumps({'foo': 'bar'}))
    monkeypatch.setenv('SNIPPET_FILE', str(file_path))
    # inject correct path
    import modules.snippets as s
    s.SNIPPET_FILE = str(file_path)
    yield
    # cleanup
    if file_path.exists():
        file_path.unlink()


def test_load_snippets():
    data = load_snippets()
    assert data == {'foo': 'bar'}


def test_get_snippet_found():
    assert get_snippet('foo') == 'bar'


def test_get_snippet_not_found():
    assert 'not found' in get_snippet('baz')


def test_save_snippet_and_list():
    save_snippet('baz', 'qux')
    assert 'baz' in list_snippets()


def test_search_snippets():
    results = search_snippets('fo')
    assert any(name == 'foo' for name, _ in results)
