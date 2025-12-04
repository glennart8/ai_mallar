"""
AI-klient som använder Gemini för att anropa MCP-verktyg.
Visar hela flödet: Användare → AI → Tool → Resultat → AI → Svar
"""

import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


async def main():
    # Anslut till MCP-servern
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Hämta tillgängliga verktyg från MCP
            mcp_tools = await session.list_tools()

            # Konvertera MCP-verktyg till Gemini-format
            gemini_tools = []
            for tool in mcp_tools.tools:
                # Bygg parameter-schema
                properties = {}
                required = []
                if tool.inputSchema and "properties" in tool.inputSchema:
                    for name, prop in tool.inputSchema["properties"].items():
                        properties[name] = {
                            "type": prop.get("type", "string"),
                            "description": prop.get("description", "")
                        }
                        if tool.inputSchema.get("required") and name in tool.inputSchema["required"]:
                            required.append(name)

                gemini_tools.append({
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": required
                    }
                })

            print("Tillgängliga verktyg för AI:")
            for t in gemini_tools:
                print(f"  - {t['name']}: {t['description']}")
            print()

            # Skapa Gemini-modell med verktyg och system prompt
            model = genai.GenerativeModel(
                "gemini-2.0-flash",
                tools=[{"function_declarations": gemini_tools}],
                system_instruction="""Du är en hjälpsam assistent med tillgång till verktyg.
Använd verktygen för att svara på frågor om matematik och väder.
Svara alltid på svenska och var koncis."""
            )

            # Chatt-loop
            print("=============================================")
            print("Chatta med AI (den kan använda verktygen)")
            print("Skriv 'quit' för att avsluta")
            print("=============================================")

            chat = model.start_chat()

            while True:
                user_input = input("\nDu: ").strip()
                if user_input.lower() == "quit":
                    break

                # Skicka till Gemini
                response = chat.send_message(user_input)

                # Kolla om AI vill anropa ett verktyg
                if response.candidates[0].content.parts[0].function_call:
                    fc = response.candidates[0].content.parts[0].function_call
                    tool_name = fc.name
                    tool_args = dict(fc.args)

                    print(f"\n[AI anropar: {tool_name}({tool_args})]")

                    # Anropa verktyget via MCP
                    result = await session.call_tool(tool_name, tool_args)
                    tool_result = result.content[0].text

                    print(f"[Resultat: {tool_result}]")

                    # Skicka resultatet tillbaka till AI
                    response = chat.send_message(
                        genai.protos.Content(
                            parts=[genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(
                                    name=tool_name,
                                    response={"result": tool_result}
                                )
                            )]
                        )
                    )

                # Skriv ut AI:s svar
                print(f"\nAI: {response.text}")


if __name__ == "__main__":
    asyncio.run(main())
