from mcp import ClientSession
from mcp.client.sse import sse_client
from rich import print, inspect
from nautobot_mcp.tools.registry import get_all_tools


async def run():
    # Connect to the MCP server running on 127.0.0.1:8005
    # The URL format should match what the FastMCP server is expecting
    async with sse_client(url="http://127.0.0.1:8005/sse") as streams:
        async with ClientSession(*streams) as session:

            print("Initializing MCP session...")
            await session.initialize()

            # # # List available tools
            # print("Listing tools...")
            tools = await session.list_tools()
            for tool in tools:
                print(tool)

            # # List available resources
            # resources = await session.list_resources()
            # print("resources", resources)

            # Call a tool
            # result = await session.call_tool(
            #     name="get_device_details", arguments={"device_name": "ang01-edge-01"}
            # )
            # print(result.content[0].text)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
