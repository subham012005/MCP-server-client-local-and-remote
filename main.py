import asyncio
import streamlit as st
import nest_asyncio
from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
    AIMessage,
)

# -----------------------------
# FIX ASYNCIO FOR STREAMLIT
# -----------------------------
nest_asyncio.apply()

load_dotenv()

# -----------------------------
# MCP SERVERS CONFIG
# -----------------------------
SERVERS = {
    "expense_tracker": {
        "transport": "streamable_http",
        "url": "https://expense-tracker-mcpserver.fastmcp.app/mcp",
    },
}

SYSTEM_MESSAGE = SystemMessage(
    content=(
        "You are a general-purpose assistant.\n"
        "If a tool can help, you MUST use it.\n"
        "Be concise and helpful."
    )
)

# -----------------------------
# INIT MCP CLIENT (ONCE)
# -----------------------------
@st.cache_resource
def init_agent():
    return MultiServerMCPClient(SERVERS)

# -----------------------------
# ASYNC AGENT LOOP
# -----------------------------
async def run_chat_step(messages):
    client = init_agent()
    tools = await client.get_tools()
    named_tools = {tool.name: tool for tool in tools}

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
    )

    llm_with_tools = llm.bind_tools(tools)

    MAX_STEPS = 5

    for _ in range(MAX_STEPS):
        response = await llm_with_tools.ainvoke(messages)

        # FINAL ANSWER
        if not getattr(response, "tool_calls", None):
            messages.append(response)
            return messages

        # HIDE INTERMEDIATE AI MESSAGE
        response.additional_kwargs["intermediate"] = True
        messages.append(response)

        # EXECUTE TOOLS
        for tool_call in response.tool_calls:
            tool = named_tools[tool_call["name"]]
            result = await tool.ainvoke(tool_call.get("args") or {})

            content = (
                result[0]["text"]
                if isinstance(result, list) and result and "text" in result[0]
                else str(result)
            )

            messages.append(
                ToolMessage(
                    content=content,
                    tool_call_id=tool_call["id"],
                )
            )

    return messages

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="MCP Chat Agent", layout="wide")
st.title("💬 MCP Chat Agent (Gemini)")

# Init chat state
if "messages" not in st.session_state:
    st.session_state.messages = [SYSTEM_MESSAGE]

# Render messages
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)

    elif isinstance(msg, AIMessage):
        if msg.additional_kwargs.get("intermediate"):
            continue
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# Input
user_input = st.chat_input("Ask anything…")

if user_input:
    st.session_state.messages.append(HumanMessage(content=user_input))

    with st.spinner("Thinking..."):
        loop = asyncio.get_event_loop()
        st.session_state.messages = loop.run_until_complete(
            run_chat_step(st.session_state.messages)
        )

    st.rerun()
