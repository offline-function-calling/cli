from typing import Dict, Callable

from .interface import ChatInterface


class CommandHandler:
    """Handles messages that are directed to the CLI as commands."""

    def __init__(self, interface: ChatInterface):
        self.interface = interface
        self.commands: Dict[str, Callable] = {
            "/exit": self._exit_command,
            "/quit": self._exit_command,
            "/help": self._help_command,
            "/clear": self._clear_command,
            "/tools": self._tools_command,
        }

    async def handle_command(self, prompt: str, model) -> bool:
        """Handles command if valid. Returns True if the command was processed."""
        if not prompt.startswith("/"):
            return False

        parts = prompt.lower().split()
        command = parts[0]
        args = parts[1:]

        if command not in self.commands:
            self.interface.show_error(f"Unknown command: {command}")
            return True

        try:
            await self.commands[command](model, args)
        except Exception as e:
            self.interface.show_error(f"Command failed: {str(e)}")

        return True

    async def _exit_command(self, model, args):
        """Exit the chat session."""
        raise KeyboardInterrupt

    async def _help_command(self, model, args):
        """Show help information."""
        self.interface.show_help()

    async def _clear_command(self, model, args):
        """Clear chat history and screen."""
        model.clear_history()

        model_info = await model.get_details()
        tools = model.tool_manager.get_tools()
        self.interface.show_header(model_info, len(tools), model.system_prompt_path)

        self.interface.show_success("Chat history cleared")

    async def _tools_command(self, model, args):
        """Handle tools subcommands."""
        subcommand = args[0] if args else "list"

        if subcommand == "list":
            tools = model.tool_manager.get_tools()
            self.interface.show_tools_list(tools)

        elif subcommand == "reload":
            count = model.reload_tools()
            self.interface.show_message(f"Reloaded {count} tools")

        else:
            self.interface.show_error(f"Unknown tools subcommand: {subcommand}")
