import asyncio
from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
)

load_dotenv()

# -----------------------------
# MCP SERVERS CONFIGURATION
# -----------------------------
SERVERS = {
    "math": {
        "transport": "stdio",
        "command": "C:/Users/subha/AppData/Local/Programs/Python/Python312/Scripts/uv.exe",
        "args": [
            "run",
            "fastmcp",
            "run",
            "D:/VS_Code/MCP_server/arithmetic_mcp/main.py",
        ],
    },
    "expense_tracker": {
        "transport": "streamable_http",
        "url": "https://expense-tracker-mcpserver.fastmcp.app/mcp",
    }
}

# -----------------------------
# SYSTEM PROMPT
# -----------------------------
system_message = SystemMessage(
    content=(
        "You are a general-purpose assistant.\n"
        "If a tool can help, you MUST use it.\n"
        "For math, use the math tool.\n"
        "For animations or videos, use the manim-server tool.\n"
        "Return clear and helpful responses."
    )
)

# -----------------------------
# MAIN ASYNC FUNCTION
# -----------------------------
async def main():
    print("Starting Multi-Server MCP Client...")

    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()

    print(f"Retrieved {len(tools)} tools.")
    print("Available tools:")
    for tool in tools:
        print(f"  - {tool.name}")

    # Map tools by name for easy access
    named_tools = {tool.name: tool for tool in tools}

    # Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
    )

    llm_with_tools = llm.bind_tools(tools)

    prompt = (
       " Create a circle with radius 2 and animate its creation."

    )

    messages = [
        system_message,
        HumanMessage(content=prompt),
    ]

    MAX_STEPS = 5

    for step in range(MAX_STEPS):
        response = await llm_with_tools.ainvoke(messages)
        messages.append(response)

        print(f"\nStep {step + 1} response:")
        print(response)

        # If no tool calls, we are done
        if not getattr(response, "tool_calls", None):
            print("\nFinal Response:")
            print(response.content)
            return

        # Handle tool calls
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call.get("args") or {}
            tool_call_id = tool_call["id"]

            print(f"\nCalling tool: {tool_name}")
            print(f"Args: {tool_args}")

            tool = named_tools[tool_name]
            tool_result = await tool.ainvoke(tool_args)

            print("Tool result:")
            print(tool_result)

            # Extract text safely
            if (
                isinstance(tool_result, list)
                and tool_result
                and isinstance(tool_result[0], dict)
                and "text" in tool_result[0]
            ):
                tool_content = tool_result[0]["text"]
            else:
                tool_content = str(tool_result)

            messages.append(
                ToolMessage(
                    content=tool_content,
                    tool_call_id=tool_call_id,
                )
            )

    print("\n⚠️ Max steps reached without a final answer.")

# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    asyncio.run(main())
