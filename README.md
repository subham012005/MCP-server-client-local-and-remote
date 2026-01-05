# 🚀 Full MCP Chatbot (Multi-Server MCP Client)

A **multi-tool AI chatbot** built using **LangChain + MCP (Model Context Protocol)** that connects to **multiple MCP servers**, reasons over user queries, and automatically invokes the correct tools.

This project is designed as a **reference implementation** for building real-world agentic systems using MCP.

---

## ✨ Features

- 🔗 Connects to **multiple MCP servers** at once  
- 🧠 Automatic **tool selection & execution**
- 💬 Clean **Streamlit chat interface**
- ⚙️ Fully **async** architecture
- 🔒 Secure API key loading via `.env`
- 🧩 Easily extensible MCP server config

---

## 🏗️ Architecture
```bash
User
 ↓
Streamlit Chat UI
 ↓
LangChain Agent (Gemini)
 ↓
MultiServerMCPClient
 ↓
┌───────────────┐   ┌──────────────────┐
│ Math MCP      │   │ Expense MCP       │
│ (stdio)       │   │ (HTTP)            │
└───────────────┘   └──────────────────┘
```

The agent:
- Reads user input
- Decides whether a tool is required
- Calls the correct MCP tool
- Returns a clean final answer

---

## 📂 Project Structure
```bash
.
├── main.py              # CLI-based MCP agent runner
├── streamlit_app.py     # Streamlit chat UI
├── pyproject.toml       # Project metadata & dependencies
├── .env                 # API keys (add your api keys)
├── .gitignore
└── README.md
```

---

## 🧠 MCP Servers

### 1️⃣ Math MCP (Local – stdio)
- Used for math & computational tasks
- Runs via `fastmcp`

### 2️⃣ Expense Tracker MCP (Remote – HTTP)
- Hosted MCP server
- Used for expense queries and summaries

Both are configured in the `SERVERS` dictionary inside the client.

---

## 🔑 Environment Setup

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

## 📦 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/full-mcp-chatbot.git
cd full-mcp-chatbot
````

### 2️⃣ Install dependencies

**Using pip**

```bash
pip install -r requirements.txt
```

**Using uv**

```bash
uv sync
```

Dependencies are defined in `pyproject.toml`.

---

## ▶️ Running the Project

### 🔹 Run CLI Agent

```bash
python main.py
```

Used for debugging and single-prompt testing.

---

Note: before run make sure you change the servers according to your project

### 🔹 Run Streamlit Chat UI

```bash
streamlit run main.py
```

Launches a browser-based MCP-powered chatbot.

---

## 🧪 Tool Execution Flow

1. User sends a prompt
2. LLM checks if a tool is required
3. MCP tool is invoked
4. Tool result is injected back
5. Final response is returned

Intermediate tool-thinking steps are hidden for a clean UI.

---

## 🧩 Adding a New MCP Server

Add a new entry to the `SERVERS` config:

```python
SERVERS["new_server"] = {
    "transport": "streamable_http",
    "url": "https://your-mcp-server/mcp"
}
```

No agent logic changes required.

---

## 🛠️ Tech Stack

* Python 3.12+
* LangChain
* Model Context Protocol (MCP)
* Google Gemini
* Streamlit
* FastMCP

---

## 🎯 Use Cases

* Agentic AI systems
* Tool-augmented chatbots
* MCP experimentation
* LangChain + MCP learning
* Multi-tool orchestration demos

---

## 🛠️ Contributing

1. Fork the repository  
2. Create a feature branch  
3. Commit and push changes  
4. Open a Pull Request  



https://github.com/user-attachments/assets/8b4b979a-a80c-410a-b436-ee675a58e1f6

