"""
AI-klient som låter Gemini spela textäventyret.
AI:n bestämmer själv vilka tools och resources att använda.
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
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Hämta tools från MCP
            mcp_tools = await session.list_tools()

            def clean_schema(obj):
                """Rensa schema från fält Gemini inte stödjer."""
                if obj is None:
                    return {"type": "object", "properties": {}}
                if not isinstance(obj, dict):
                    return obj
                # Ta bort 'title' och recursa endast för dict-värden
                cleaned = {}
                for k, v in obj.items():
                    if k == "title":
                        continue
                    if isinstance(v, dict):
                        cleaned[k] = clean_schema(v)
                    else:
                        cleaned[k] = v
                return cleaned

            gemini_tools = []
            for tool in mcp_tools.tools:
                schema = clean_schema(tool.inputSchema)
                # Säkerställ att schema har rätt struktur
                if not schema.get("properties"):
                    schema = {"type": "object", "properties": {}}
                gemini_tools.append({
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": schema
                })

            # Skapa Gemini med spel-prompt
            model = genai.GenerativeModel(
                "gemini-2.0-flash",
                tools=[{"function_declarations": gemini_tools}],
                system_instruction="""Du är en spelledare för ett textäventyr.

När spelaren ger kommandon, använd rätt verktyg:
- look() - när spelaren vill se sig omkring
- move(direction) - när spelaren vill gå någonstans (norr, söder, öster, väster, upp, ner, över, tillbaka)
- pickup(item) - när spelaren vill plocka upp något
- inventory() - när spelaren vill se sin ryggsäck
- reset() - när spelaren vill börja om

Beskriv resultatet på ett engagerande sätt. Var kort och koncis.
Svara på svenska."""
            )

            chat = model.start_chat()

            # Starta med att visa var spelaren är
            result = await session.call_tool("look", {})
            print(f"\n{result.content[0].text}")

            print("\n" + "===============================================")
            print("TEXTÄVENTYR - Skriv 'quit' för att avsluta")
            print("===============================================")

            while True:
                user_input = input("\n> ").strip()
                if user_input.lower() == "quit":
                    break

                response = chat.send_message(user_input)

                # Om AI:n vill anropa ett verktyg
                if response.candidates[0].content.parts[0].function_call:
                    fc = response.candidates[0].content.parts[0].function_call
                    tool_name = fc.name
                    tool_args = dict(fc.args)

                    # Anropa verktyget via MCP
                    result = await session.call_tool(tool_name, tool_args)
                    tool_result = result.content[0].text

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

                print(f"\n{response.text}")


if __name__ == "__main__":
    asyncio.run(main())
