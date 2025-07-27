import logging
import os
import PySimpleGUI as sg
from pathlib import Path
from openai import OpenAI

from .processor      import process_folder
from .snippets       import save_snippet, get_snippet, list_snippets, search_snippets
from .scheduler      import queue_post, format_queue_for_display
from .sheets_writer  import append_post, get_all_posts
from config import logger


def handle_run(window, values, client: OpenAI, use_local: bool, local_model: str, config: dict):
    logger.info(f"handle_run: folder={values.get('FOLDER')}, task={values.get('TASK')}")
    folder  = values.get("FOLDER")
    task    = values.get("TASK")
    model   = values.get("MODEL")
    persona = values.get("PERSONA")

    if not folder or not os.path.isdir(folder):
        window["OUTPUT"].update("❌ Invalid folder path.\n")
        return

    window["OUTPUT"].update(f"🔍 Processing files in: {folder}\n\n")
    outputs = process_folder(folder, task, model, persona, client, use_local, local_model)

    for out in outputs:
        filename = f"gpt_output_{Path(out['file']).stem}_{out['timestamp']}.txt"
        with open(filename, "w") as f:
            f.write(out['reply'])
        window["OUTPUT"].update(f"{out['mode_str']} - {out['file']}:\n{out['reply']}\n\n", append=True)


def handle_save_snippet(window, values):
    logger.info("handle_save_snippet")
    name    = sg.popup_get_text("Enter snippet name:")
    content = values.get("OUTPUT", "")
    if name and content.strip():
        save_snippet(name, content)
        sg.popup(f"✅ Snippet '{name}' saved.")
        window["SNIPPET_LIST"].update(values=list_snippets())


def handle_get_snippet(window, values):
    logger.info(f"handle_get_snippet: selected={values.get('SNIPPET_LIST')}")
    selected = values.get("SNIPPET_LIST")
    if selected:
        window["OUTPUT"].update(get_snippet(selected))


def handle_search_snippets(window, values):
    logger.info(f"handle_search_snippets: query={values.get('SNIPPET_SEARCH')}")
    query = values.get("SNIPPET_SEARCH", "").strip()
    if not query:
        sg.popup("⚠️ Enter a search term.")
        return
    results = search_snippets(query)
    if not results:
        sg.popup("No matches found.")
        return

    options = [f"{n} — {c[:50].replace(chr(10), ' ')}..." for n,c in results]
    choice  = sg.popup_get_text("Select snippet:", default_text="\n".join(options))
    if choice:
        name = choice.split(" — ")[0]
        window["OUTPUT"].update(get_snippet(name))


def handle_queue_post(window, values):
    logger.info("handle_queue_post")
    content = values.get("OUTPUT", "")
    if not content.strip():
        sg.popup("⚠️ No content to queue.")
        return
    platform = sg.popup_get_text("Platform? (Instagram, Facebook, etc.)", default_text="Instagram")
    tags     = sg.popup_get_text("Optional tags (comma separated):")
    schedule = sg.popup_get_text("Schedule date/time? (or leave blank)", default_text="")

    tags_list = [t.strip() for t in tags.split(",")] if tags else None
    sg.popup(queue_post(content, platform=platform, tags=tags_list, scheduled_for=schedule or None))


def handle_send_to_sheet(window, values):
    logger.info("handle_send_to_sheet")
    content = values.get("OUTPUT", "")
    if not content.strip():
        sg.popup("⚠️ No content to send.")
        return
    sheet_name = sg.popup_get_text("Google Sheet name:")
    platform   = sg.popup_get_text("Platform? (Instagram, Facebook, etc.)", default_text="Instagram")
    tags       = sg.popup_get_text("Optional tags (comma separated):")
    status     = sg.popup_get_text("Status (Idea, Draft, Scheduled):", default_text="Idea")
    tags_list = [t.strip() for t in tags.split(",")] if tags else None
    sg.popup(append_post(sheet_name, content, platform, tags_list, status))


def handle_refresh_queue(window):
    logger.info("handle_refresh_queue")
    lines, queue = format_queue_for_display()
    window["QUEUE_LIST"].update(lines)
    window.metadata = queue


def handle_load_selected_post(window):
    logger.info("handle_load_selected_post")
    selected = window["QUEUE_LIST"].get()
    if not selected or not window.metadata:
        sg.popup("⚠️ No post selected.")
        return
    index = window["QUEUE_LIST"].Values.index(selected[0])
    window["OUTPUT"].update(window.metadata[index].get("content", ""))


def handle_load_posts_from_sheet(window):
    logger.info("handle_load_posts_from_sheet")
    name = sg.popup_get_text("Google Sheet name:")
    if not name:
        sg.popup("⚠️ Sheet name required.")
        return
    data = get_all_posts(name)
    if isinstance(data, str):
        sg.popup(data)
        return
    window.metadata_sheet = data
    window["SHEET_LIST"].update([
        f"[{p.get('Platform')}] {p.get('Status')} — {p.get('Content','')[:50]}..." for p in data
    ])


def handle_load_selected_sheet_post(window):
    logger.info("handle_load_selected_sheet_post")
    selected = window["SHEET_LIST"].get()
    if not selected or not window.metadata_sheet:
        sg.popup("⚠️ No post selected.")
        return
    index = window["SHEET_LIST"].Values.index(selected[0])
    window["OUTPUT"].update(window.metadata_sheet[index].get("Content", ""))
