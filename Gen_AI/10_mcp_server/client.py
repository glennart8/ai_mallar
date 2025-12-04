"""
Enkel MCP-klient som ansluter till servern och anropar verktyg.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    # Starta servern som en subprocess och anslut
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initiera anslutningen
            await session.initialize()

            # Lista tillgängliga verktyg
            tools = await session.list_tools()
            print("Tillgängliga verktyg:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            print("\n" + "=============================================="  + "\n")

            # Testa add
            result = await session.call_tool("add", {"a": 5, "b": 3})
            print(f"add(5, 3) = {result.content[0].text}")

            # Testa multiply
            result = await session.call_tool("multiply", {"a": 7, "b": 6})
            print(f"multiply(7, 6) = {result.content[0].text}")

            # Testa get_weather
            result = await session.call_tool("get_weather", {"city": "Stockholm"})
            print(f"get_weather('Stockholm') = {result.content[0].text}")

            # Testa reverse_string
            result = await session.call_tool("reverse_string", {"text": "Hej världen!"})
            print(f"reverse_string('Hej världen!') = {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
