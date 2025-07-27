# Project Improvement Roadmap

Based on analysis, here are suggested enhancements:

## 1. Project Structure & Imports
- Convert `modules/` into a package (add `__init__.py`).
- Remove manual `sys.path` manipulation and use proper package imports.
- Split large files (e.g., GUI logic) into smaller modules.

## 2. Dependency Management
- Add `requirements.txt` listing all external dependencies:
  - PySimpleGUI
  - openai
  - requests
  - gspread
  - google-auth

## 3. Configuration
- Centralize configuration with `.env` or a config module.
- Validate config values at startup.

## 4. Error Handling & Logging
- Replace generic `except Exception` with targeted exceptions.
- Integrate Python `logging` for debug/info/error messages.
- Add retry/backoff for network calls.

## 5. Testing
- Introduce pytest for unit tests of modules:
  - Mock filesystem and external APIs.
  - Test snippet, scheduler, and sheets_writer logic.

## 6. Code Quality & Formatting
- Enforce formatting with Black.
- Lint with Flake8 or Pylint.
- Add type hints and run MyPy.

## 7. UX Improvements
- Make the GUI non-blocking using async calls or threading.
- Show progress indicators during long-running tasks.

## 8. Future Enhancements
- Delete/edit posts in queue
- Drag-and-drop snippet loading
- Batch caption formatter
- Notion integration
- Rule-based post generator (ML/Regex)

---
*Next Steps: implement top items (structure, imports, requirements).*
