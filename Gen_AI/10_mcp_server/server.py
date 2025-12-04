"""
Enkel MCP-server som exponerar verktyg.
Demonstrerar grunderna i Model Context Protocol.
"""

from mcp.server.fastmcp import FastMCP

# Skapa MCP-server
mcp = FastMCP("Demo Server")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Adderar två tal."""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiplicerar två tal."""
    return a * b


@mcp.tool()
def get_weather(city: str) -> str:
    """Hämtar väder för en stad (mock-data)."""
    # MCOKDATA, annars API
    weather_data = {
        "Stockholm": "12°C, molnigt",
        "Göteborg": "14°C, regn",
        "Malmö": "15°C, soligt",
    }
    return weather_data.get(city, f"Okänd stad: {city}")


@mcp.tool()
def reverse_string(text: str) -> str:
    """Vänder på en textsträng."""
    return text[::-1]


if __name__ == "__main__":
    # Körs med: mcp run server.py
    # Eller lägg till i Claude Desktop config
    mcp.run()
