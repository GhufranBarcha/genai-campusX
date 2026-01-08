import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
import os
import json


load_dotenv()
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")


SERVERS = {
    "math": {
        "transport": "stdio",
        "command": "/home/ghufranbarcha/.local/bin/uv",
        "args": [
            "run",
            "fastmcp",
            "run",
            "/home/ghufranbarcha/Desktop/Tech_learning/genai-campusX/mcp-campusX/fastmcp-demo-remote-server/main.py"
        ]

    },
    "expense_tracker": {
        "transport": "streamable_http",
        "url": "https://expense-tracker.fastmcp.app/mcp"
    }

}

async def main():
    client =  MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()
    # print("Math tool: ", tools)

    named_tools =  {tool.name : tool for tool in tools }
    # print("Named tools: ", named_tools)

    llm = ChatOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            model="google/gemini-2.5-flash",
    )
    llm_with_tools = llm.bind_tools(tools)

    prompt = "Add 50 dolloar for meal on jan 10 2025."
    response = await llm_with_tools.ainvoke(prompt)

    if not getattr(response, "tool_calls", None):
        print("\nLLM Reply:", response.content)
        return

    tool_messages = []
    for tc in response.tool_calls:
        selected_tool = tc["name"]
        selected_tool_args = tc.get("args") or {}
        selected_tool_id = tc["id"]

        result = await named_tools[selected_tool].ainvoke(selected_tool_args)
        tool_messages.append(ToolMessage(tool_call_id=selected_tool_id, content=json.dumps(result)))
        

    final_response = await llm_with_tools.ainvoke([prompt, response, *tool_messages])
    print(f"Final response: {final_response.content}")


if __name__ == '__main__':
    asyncio.run(main())