
# 🧠 GPT Assistant Features (Zorin OS Custom)

This assistant supports local + cloud GPT workflows, content automation, and dev tools with full GUI controls.

---

## ✅ Core Functional Features

### 🧠 AI Model Integration

- ✅ **Online/Offline Toggle**: Switch between OpenAI API and Ollama (local model).
- ✅ **Model Selection**: Choose from gpt-3.5-turbo, gpt-4, or local models like mistral.

---

### 🔧 Dev-Focused Tools

- ✅ **Snippet Save/Load**: Save reusable code or GPT content by name.
- ✅ **Snippet Search**: Search inside all snippet content by keyword.
- ✅ **Persona Presets**: Choose tone (e.g., Jason the Dev, IG Copywriter).

---

### ✍️ Content Creation & Automation

- ⬜ **Auto Blog/Post Formatter**: Write content and format for IG/Pinterest/FB.
- ✅ **SEO Tone Adjuster**: Adjust prompt using selected persona.
- ✅ **Instagram-style caption formatting** with emojis, CTAs, and line breaks.

---

### 📅 Social Media Tools

- ✅ **Post Scheduler**: Queue posts locally with tags, platform, and timestamp.
- ✅ **Queue Viewer Panel**: List and load scheduled posts directly into editor.
- ✅ **Google Sheets Integration**:
  - Export posts to content calendar.
  - Import drafts/ideas from Google Sheets and reuse them in chat.

---

### 🧩 GPT Assistant Interface Features

- ✅ **Multi-model toggle**
- ✅ **Folder walker** for batch processing text/code
- ✅ **Task-based actions** (Summarize, Explain, Rewrite)
- ✅ **GUI Persona selector**
- ✅ **Dropdown snippet manager**
- ✅ **Multiline output with append + autosave**

---

### 📁 File Organization

```
gpt_assistant/
├── gpt_gui.py
├── config.json
├── post_queue.json
├── snippets.json
├── credentials/gsheets_service_account.json
└── modules/
    ├── snippets.py
    ├── scheduler.py
    ├── sheets_writer.py
    └── ollama_chat.py
```

---

### ⚙️ Future-Ready Enhancements (Planned/Optional)

- [ ] Delete/edit posts in queue
- [ ] Drag-and-drop snippet loading
- [ ] Batch caption formatter
- [ ] Notion integration
- [ ] Rule-based post generator (ML/Regex)
