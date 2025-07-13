# Minecord Simplification and Refactoring Tasks

This document outlines several areas in the `minecord` codebase that can be simplified and improved for better maintainability, readability, and robustness.

## 1. Simplify Configuration Parsing in `config.py`

**Problem:** The properties for `guild_id`, `minecord_channel_id`, and `rcon_port` each contain repetitive `try-except` blocks for converting configuration values to integers. This leads to code duplication and makes the code harder to maintain.

**Suggestion:**
- Create a private helper method, for example `_get_as_int(self, key: str, default: Optional[int] = None) -> Optional[int]`, within the `Config` class.
- This method will handle the logic of retrieving a value, converting it to an integer, and managing `ValueError`/`TypeError` exceptions with a generic warning message.
- Refactor the `guild_id`, `minecord_channel_id`, and `rcon_port` properties to use this new helper method. This will also fix a minor copy-paste bug in the `guild_id` warning message.

## 2. Reduce Duplication in RCON Client (`rcon.py`)

**Problem:** The `list_players` and `list_ops` methods in `minecord/backend/rcon.py` are nearly identical. They both execute a command and then parse the output using the same regular expression and string splitting logic.

**Suggestion:**
- Create a private helper method, for example `_parse_list_command(self, command: str) -> List[str]`, that takes the RCON command as an argument.
- This method will contain the shared logic: executing the command, handling the `MCRconException`, and parsing the response to extract the list of names.
- Update `list_players` and `list_ops` to be simple one-line calls to this new helper method with their respective commands (`"list"` and `"list ops"`).

## 3. Improve RCON Error Handling

**Problem:** The `MinecraftRCONClient` currently catches `MCRconException` (which can indicate connection, authentication, or other RCON-level failures) and returns an empty list. This hides the root cause of the problem from the user-facing command in `MinecraftCog`. The `online` command in `MinecraftCog` only catches `ConnectionRefusedError`, which is too specific and won't handle authentication failures.

**Suggestion:**
- In `minecord/backend/rcon.py`, modify the RCON methods to let `MCRconException` propagate upwards instead of catching it and returning `[]`.
- In `minecord/cogs/minecraft.py`, update the `try...except` block in the `online` command to catch the more general `MCRconException`.
- Provide more informative error messages to the Discord user based on the exception, distinguishing between connection issues and potential configuration problems (like a wrong password). This makes debugging much easier for the server administrator.