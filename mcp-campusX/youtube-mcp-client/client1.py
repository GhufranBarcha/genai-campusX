import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
import os


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
    prompt = "what is the capital of pakistan"

    llm_with_tools = llm.bind_tools(tools=tools)
    response = await llm_with_tools.ainvoke(prompt)

    if not getattr(response, "tool_calls", None):
        print("\nLLM Reply:", response.content)
        return


    selected_tool = response.tool_calls[0]["name"]
    selected_tools_arg = response.tool_calls[0]["args"]
    selected_tool_id = response.tool_calls[0]["id"]

    tool_result =await named_tools[selected_tool].ainvoke(selected_tools_arg)

    print(selected_tool)
    print(selected_tools_arg)

    print("tools results",tool_result)

    tool_message = ToolMessage(content=tool_result, tool_call_id = selected_tool_id)
    final_response = await llm_with_tools.ainvoke([prompt,response, tool_message])
    print("final Response",final_response.content)


if __name__ == "__main__":
    asyncio.run(main())