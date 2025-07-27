import logging
import PySimpleGUI as sg
from datetime import datetime
from pathlib import Path
from config import client, USE_LOCAL, LOCAL_MODEL, logger, CONFIG

"""
Removed manual modules path hack; using proper package imports instead
"""

# Imports
from modules.gui_controller import (
    handle_run,
    handle_save_snippet,
    handle_get_snippet,
    handle_search_snippets,
    handle_queue_post,
    handle_send_to_sheet,
    handle_refresh_queue,
    handle_load_selected_post,
    handle_load_posts_from_sheet,
    handle_load_selected_sheet_post,
)


# Build GPT prompt based on task and persona

# Layout
# This version reorganizes the GUI layout into clear vertical sections:
# 🔧 Settings, 📂 Folder Input, 🧠 Snippets, 📅 Scheduled Posts, 📋 Google Sheet, 📝 Output, 📤 Export

layout = [
    [sg.Frame("🔧 Settings", [
        [sg.Text("Model:"), sg.Combo(["gpt-3.5-turbo", "gpt-4"], default_value="gpt-3.5-turbo", key="MODEL")],
        [sg.Text("Mode:"), sg.Combo(["OpenAI", "Ollama"], default_value="Ollama" if USE_LOCAL else "OpenAI", key="MODE_SELECT")],
        [sg.Text("Persona:"), sg.Combo(["Default", "IG Copywriter", "NixLevel Hustler", "Jason the Dev"], default_value="Default", key="PERSONA")],
        [sg.Text("Task:"), sg.Combo(["Summarize", "Explain", "Rewrite"], default_value="Summarize", key="TASK")]
    ])],

    [sg.Frame("📂 Folder Input", [
        [sg.Text("Select Folder:"), sg.InputText(key="FOLDER"), sg.FolderBrowse()],
        [sg.Button("Run"), sg.Button("Exit")]
    ])],

    [sg.Frame("🧠 Snippet Manager", [
        [sg.Text("Snippet:"), sg.Combo([], size=(40, 1), key="SNIPPET_LIST"), sg.Button("Get Snippet"), sg.Button("Save Snippet")],
        [sg.InputText(key="SNIPPET_SEARCH", size=(40, 1), tooltip="Search snippets..."), sg.Button("Search Snippets")]
    ])],

    [sg.Frame("📅 Scheduled Posts", [
        [sg.Listbox(values=[], size=(80, 4), key="QUEUE_LIST", enable_events=True)],
        [sg.Button("Refresh Queue"), sg.Button("Load Selected Post")]
    ])],

    [sg.Frame("📋 Google Sheet Posts", [
        [sg.Listbox(values=[], size=(80, 4), key="SHEET_LIST", enable_events=True)],
        [sg.Button("Load Posts from Sheet"), sg.Button("Load Selected Sheet Post")]
    ])],

    [sg.Frame("📝 Output Editor", [
        [sg.Multiline(size=(80, 20), key="OUTPUT")]
    ])],

    [sg.Frame("📤 Export Tools", [
        [sg.Button("Queue Post"), sg.Button("Send to Google Sheet")]
    ])]
]

window = sg.Window("GPT File Assistant", layout, finalize=True)
window["SNIPPET_LIST"].update(values=list_snippets())
window.metadata = []
window.metadata_sheet = []

while True:
    event, values = window.read()
    logger.info(f"GUI event: {event}")
    if event in (sg.WIN_CLOSED, "Exit"):
        break
    elif event == "Run":
        handle_run(window, values, client, USE_LOCAL, LOCAL_MODEL, CONFIG)
    elif event == "Save Snippet":
        handle_save_snippet(window, values)
    elif event == "Get Snippet":
        handle_get_snippet(window, values)
    elif event == "Search Snippets":
        handle_search_snippets(window, values)
    elif event == "Queue Post":
        handle_queue_post(window, values)
    elif event == "Send to Google Sheet":
        handle_send_to_sheet(window, values)
    elif event == "Refresh Queue":
        handle_refresh_queue(window)
    elif event == "Load Selected Post":
        handle_load_selected_post(window)
    elif event == "Load Posts from Sheet":
        handle_load_posts_from_sheet(window)
    elif event == "Load Selected Sheet Post":
        handle_load_selected_sheet_post(window)
window.close()

