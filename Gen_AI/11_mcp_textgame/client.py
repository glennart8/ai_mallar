"""
Test-klient för textäventyret.
Visar hur Resources och Tools fungerar.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Visa tillgängliga Resources
            resources = await session.list_resources()
            print("RESOURCES (läsa data):")
            for r in resources.resources:
                print(f"  - {r.uri}: {r.description}")

            # Visa tillgängliga Tools
            tools = await session.list_tools()
            print("\nTOOLS (utföra aktioner):")
            for t in tools.tools:
                print(f"  - {t.name}: {t.description}")

            print("\n" + "==============================")
            print("SPELAR SPELET:")
            print("==============================")

            # Återställ spelet först
            result = await session.call_tool("reset", {})
            print(f"\n{result.content[0].text}")

            # Läs resource: var är vi?
            resource = await session.read_resource("game://status")
            print(f"\n[Resource: status] {resource.contents[0].text}")

            # Tool: gå norrut
            result = await session.call_tool("move", {"direction": "norr"})
            print(f"\n[Tool: move('norr')]\n{result.content[0].text}")

            # Tool: plocka upp fackla
            result = await session.call_tool("pickup", {"item": "fackla"})
            print(f"\n[Tool: pickup('fackla')] {result.content[0].text}")

            # Resource: kolla inventory
            resource = await session.read_resource("game://inventory")
            print(f"\n[Resource: inventory] {resource.contents[0].text}")

            # Tool: gå ner till skattkammaren
            result = await session.call_tool("move", {"direction": "ner"})
            print(f"\n[Tool: move('ner')]\n{result.content[0].text}")

            # Resource: status
            resource = await session.read_resource("game://status")
            print(f"\n[Resource: status] {resource.contents[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
