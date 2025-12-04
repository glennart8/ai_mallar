"""
MCP-server för textäventyr.
Demonstrerar Resources (läsa state) och Tools (ändra state).
"""

from mcp.server.fastmcp import FastMCP
import game

mcp = FastMCP("Textäventyr")


# =============================================================================
# RESOURCES - Data som AI:n kan läsa (passivt)
# =============================================================================

@mcp.resource("game://room")
def get_current_room() -> str:
    """Visar nuvarande rum, föremål och utgångar."""
    return game.get_room_info()


@mcp.resource("game://inventory")
def get_inventory() -> str:
    """Visar spelarens ryggsäck."""
    return game.get_inventory()


@mcp.resource("game://status")
def get_status() -> str:
    """Visar spelarens status (HP, framsteg)."""
    return game.get_status()


# =============================================================================
# TOOLS - Aktioner som AI:n kan utföra
# =============================================================================

@mcp.tool()
def move(direction: str) -> str:
    """Gå i en riktning (norr, söder, öster, väster, upp, ner, över, tillbaka)."""
    return game.move(direction)


@mcp.tool()
def pickup(item: str) -> str:
    """Plocka upp ett föremål."""
    return game.pickup(item)


@mcp.tool()
def look() -> str:
    """Titta dig omkring i rummet."""
    return game.get_room_info()


@mcp.tool()
def inventory() -> str:
    """Visa din ryggsäck."""
    return game.get_inventory()


@mcp.tool()
def reset() -> str:
    """Starta om spelet från början."""
    return game.reset_game()


if __name__ == "__main__":
    mcp.run()
