import pytest
import os
import sys
from pathlib import Path

# Ensure project root in sys.path
ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT))

@pytest.fixture(autouse=True)
def change_cwd(tmp_path, monkeypatch):
    # Run tests with cwd at project root
    monkeypatch.chdir(ROOT)
