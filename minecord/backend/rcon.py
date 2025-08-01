import os
import re
from typing import List, Optional

from mcrcon import MCRcon, MCRconException


class MinecraftRCONClient:
    """
    A client to interact with a Minecraft server's RCON console.

    Handles connection, command execution, and response parsing.
    Configuration is loaded from environment variables.
    """

    def __init__(
        self, host: str = "localhost", port: int = 25575, password: Optional[str] = None
    ):
        """
        Initializes the RCON client.

        Args:
            host: Minecraft server hostname (default: localhost)
            port: RCON port (default: 25575)
            password: RCON password (required)
        """
        self.host = host
        self.port = port
        self.password = password

        if not self.password:
            raise ValueError("RCON password is required")

    def _execute_command(self, command: str) -> str:
        """Establishes a connection and executes a single command."""
        try:
            with MCRcon(self.host, self.password, self.port) as mcr:
                response = mcr.command(command)
                return response
        except MCRconException as e:
            print(f"RCON Error: Failed to execute command '{command}'. Reason: {e}")
            # Re-raise to allow the caller to handle connection/auth errors
            raise

    def list_players(self) -> List[str]:
        """
        Executes the /list command and returns a list of online players.

        Returns:
            A list of player names. Returns an empty list if no players are online
            or if the command fails.
        """
        try:
            response = self._execute_command("list")
        except MCRconException:
            return []  # Return empty list on connection/auth failure

        # Typical response: "There are 1/20 players online: player1"
        # We extract the content after the colon.
        match = re.search(r":\s*(.*)", response)
        if not match or not match.group(1):
            return []  # No players listed

        player_list_str = match.group(1).strip()
        players = [p.strip() for p in player_list_str.split(",")]
        return players

    def get_fingerprint(self) -> List[str]:
        """
        Executes the '/automodpack host fingerprint' command and returns the fingerprint.

        Returns:
            A hexadecimal fingerprint for the server to allow automodpack users to connect
        """
        try:
            response = self._execute_command("automodpack host fingerprint")
        except MCRconException:
            return "Failed to retrieve fingerprint"  # Return on connection/auth failure

        # Typical response: "Certificate fingerprint - 00112233445566778899aabbccddeeff..."
        # We extract the content after the dash.
        match = re.search(r"-\s*([a-f0-9]*)", response)
        if not match or not match.group(1):
            return "Unexpected fingerprint response"

        return match.group(1).strip()

    def whitelist_add(self, username: str) -> str:
        """
        Executes the 'whitelist add <username>' command to add a player to the server whitelist.

        Args:
            username: The Minecraft username to add to the whitelist

        Returns:
            The server response message, or an error message if the command fails
        """
        try:
            response = self._execute_command(f"whitelist add {username}")
            return response
        except MCRconException:
            return f"Failed to add {username} to whitelist"  # Return on connection/auth failure

    def whitelist_list(self) -> str:
        """
        Executes the 'whitelist list' command to get the current server whitelist.

        Returns:
            The server response with the whitelist, or an error message if the command fails
        """
        try:
            response = self._execute_command("whitelist list")
            return response
        except MCRconException:
            return "Failed to retrieve allowlist"  # Return on connection/auth failure


if __name__ == "__main__":
    # Example usage for direct testing of this module
    # This requires configuration to be passed explicitly now
    import sys

    if len(sys.argv) < 4:
        print("Usage: python rcon.py <host> <port> <password>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    password = sys.argv[3]

    try:
        client = MinecraftRCONClient(host=host, port=port, password=password)
        online_players = client.list_players()
        print("--- Minecraft Server Status ---")
        if online_players:
            print(
                f"Online players ({len(online_players)}): {', '.join(online_players)}"
            )
        else:
            print("No players are currently online.")
        print("-----------------------------")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
