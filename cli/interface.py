import sys
import asyncio

from typing import Dict, Any

from rich.console import Console, Group
from rich.markdown import Markdown
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.prompt import Confirm

from sdk.types import Model

from .theme import Theme


class ChatInterface:
    """Elegant chat interface with rich visual components."""

    def __init__(self, console: Console, theme: Theme):
        self.console = console
        self.theme = theme
        self._live_panel = None
        self._full_response = ""
        self._current_tool_display = None

    def show_header(self, model_info: Model, tool_count: int, prompt_loaded: bool):
        """Display an elegant header with model and session information."""
        self._clear_screen()

        name = model_info.name
        details = model_info.details
        capabilities = model_info.capabilities

        param_size = details.get("parameter_size", "N/A")
        quant_level = details.get("quantization_level", "N/A")

        model_text = Text()
        model_text.append(name, style=self.theme.title)
        model_text.append(f" • {param_size} parameters", style=self.theme.dim)
        model_text.append(f" • {quant_level} quantization", style=self.theme.dim)

        caps_text = Text()
        if capabilities:
            caps_text.append(", ".join(capabilities), style=self.theme.info)

        session_text = Text()
        session_text.append(f"{tool_count} tools enabled", style=self.theme.highlight)
        session_text.append(
            f"\n{'Custom' if prompt_loaded else 'Default'} prompt", style=self.theme.dim
        )

        info_table = Table.grid(expand=True)
        info_table.add_column(justify="left")
        info_table.add_column(justify="right")

        left_content = Group(model_text, caps_text) if capabilities else model_text
        info_table.add_row(left_content, session_text)

        header_panel = Panel(
            info_table,
            title=Text("Offline Function Calling Agent", style=self.theme.title),
            border_style=self.theme.header_border,
        )

        self.console.print(header_panel)

    def get_user_input(self) -> str:
        """Get multiline user input with elegant prompting."""
        self.console.rule(characters="─", style=self.theme.border)

        user_prompt = Text()
        user_prompt.append("You", style=self.theme.user)
        user_prompt.append(" (Press Ctrl+D to submit)", style=self.theme.dim)

        self.console.print(user_prompt)

        try:
            lines = []
            for line in sys.stdin:
                lines.append(line)
            return "".join(lines).strip()
        except EOFError:
            return "".join(lines).strip() if lines else ""

    def start_stream(self) -> None:
        """Initializes and starts a Live display for streaming."""
        self._full_response = ""
        self._live_panel = Live(console=self.console, auto_refresh=False)
        self._live_panel.start()

    def update_stream(self, chunk: str) -> None:
        """Updates the Live display with a new chunk of text."""
        if self._live_panel is None:
            self.start_stream()

        self._full_response += chunk
        content = Markdown(self._full_response + " ▋", style=self.theme.assistant)
        panel = Panel(content, border_style=self.theme.border)
        self._live_panel.update(panel, refresh=True)

    def stop_stream(self) -> None:
        """Finalizes and stops the Live display."""
        if self._live_panel:
            final_content = Markdown(self._full_response, style=self.theme.assistant)
            final_panel = Panel(final_content, border_style=self.theme.border)
            self._live_panel.update(final_panel)
            self._live_panel.stop()
            self._live_panel = None

        self.console.print()

    async def execute_tool_with_consent(
        self, tool_name: str, arguments: Dict[str, Any], tool_executor: callable
    ) -> Any:
        """Execute a single tool with user consent and clean visual feedback."""
        self._show_tool_request(tool_name, arguments)

        self.console.print()
        consent = await asyncio.to_thread(
            Confirm.ask,
            Text.assemble(
                ("Execute ", None), (tool_name, self.theme.highlight), ("?", None)
            ),
            default=True,
            console=self.console,
        )

        if not consent:
            self._show_tool_denied(tool_name)
            return None

        return await self._execute_with_progress(tool_name, tool_executor)

    def _show_tool_request(self, tool_name: str, arguments: Dict[str, Any]):
        """Display tool request as a message from 'Tools' user."""
        self.console.rule(characters="─", style=self.theme.border)

        user_prompt = Text()
        user_prompt.append("Tool", style=self.theme.tools)
        user_prompt.append(f" • {tool_name}", style=self.theme.info)
        self.console.print(user_prompt)

        if arguments:
            args_content = []
            for key, value in arguments.items():
                arg_line = Text()
                arg_line.append(f" • {key}: ", style=self.theme.argument)

                if isinstance(value, str):
                    if len(value) > 100:
                        display_value = value[:97] + "..."
                    else:
                        display_value = value
                    arg_line.append(f'"{display_value}"', style=self.theme.dim)
                elif isinstance(value, (int, float, bool)):
                    arg_line.append(str(value), style=self.theme.dim)
                elif isinstance(value, (list, dict)):
                    if len(str(value)) > 100:
                        display_value = str(value)[:97] + "..."
                    else:
                        display_value = str(value)
                    arg_line.append(display_value, style=self.theme.dim)
                else:
                    arg_line.append(str(value), style=self.theme.dim)

                args_content.append(arg_line)

            content = Group(*args_content)
        else:
            content = Text(" (no arguments)", style=self.theme.dim)

        self.console.print(content)

    async def _execute_with_progress(
        self, tool_name: str, tool_executor: callable
    ) -> Any:
        """Execute tool with a clean progress indicator."""
        progress_text = Text()
        progress_text.append("Executing ")
        progress_text.append(tool_name, style=self.theme.info)
        progress_text.append("...")

        with self.console.status(
            progress_text, spinner="dots", spinner_style=self.theme.spinner
        ):
            try:
                result = await tool_executor()
                self._show_tool_success(tool_name, result)
                return result
            except Exception as e:
                self._show_tool_error(tool_name, e)
                raise

    def _show_tool_success(self, tool_name: str, result: Any):
        """Display successful tool execution as a message from 'Tools'."""
        success_text = Text()
        success_text.append(
            f"Called {tool_name} successfully", style=self.theme.tool_success
        )
        self.console.print(success_text)
        self.console.print()

    def _show_tool_denied(self, tool_name: str):
        """Display tool execution denial as a message from 'Tools'."""
        denied_text = Text()
        denied_text.append(
            f"Tool {tool_name} execution denied by user", style=self.theme.warning
        )
        self.console.print(denied_text)
        self.console.print()

    def _show_tool_error(self, tool_name: str, error: Exception):
        """Display tool execution error as a message from 'Tools'."""
        error_text = Text()
        error_text.append(f"Tool call for {tool_name} failed: ", style=self.theme.error)
        error_text.append(str(error), style=self.theme.warning)
        self.console.print(error_text)
        self.console.print()

    def show_tools_summary(
        self, total_tools: int, executed_tools: int, failed_tools: int
    ):
        """Show a summary after tool execution batch."""
        if total_tools <= 1:
            return

        summary_text = Text()
        summary_text.append("Tools Summary: ", style=self.theme.subtitle)
        summary_text.append(
            f"{executed_tools}/{total_tools} executed", style=self.theme.tool_success
        )

        if failed_tools > 0:
            summary_text.append(f", {failed_tools} failed", style=self.theme.error)

        self.console.rule(style=self.theme.border)
        self.console.print(summary_text)
        self.console.rule(style=self.theme.border)
        self.console.print()

    def show_tools_list(self, tools: list):
        """Display available tools in an elegant table."""
        if not tools:
            self.console.print("No tools available", style=self.theme.warning)
            return

        self.console.print()
        self.console.print(Text("Tools", style=self.theme.subtitle))
        self.console.print(
            Text(
                "The following is a list of tools available to the agent.",
                style=self.theme.info,
            )
        )
        self.console.print()

        for tool_func in tools:
            doc = (
                (tool_func.__doc__ or "No description available").strip().split("\n")[0]
            )
            self.console.print(Text(tool_func.__name__, style=self.theme.command))
            self.console.print(Text(doc, style=self.theme.dim))
            self.console.print()

    def show_tools_reloaded(self, count: int):
        self.console.print()
        self.console.print(Text("Tools", style=self.theme.subtitle))
        self.console.print(Text(f"Reloaded {count} tools", style=self.theme.info))
        self.console.print()

    def show_help(self):
        """Display elegant help information."""
        self.console.print()

        commands_table = Table(show_header=False, pad_edge=False, box=None)
        commands_table.add_column("Command", style=self.theme.command, width=20)
        commands_table.add_column("Description", style=self.theme.info)
        commands = [
            ("/exit", "Exit the chat session"),
            ("/clear", "Clear history and screen"),
            ("/tools [list|reload]", "Manage available tools"),
            ("/help", "Show this help message"),
        ]
        for cmd, desc in commands:
            commands_table.add_row(cmd, desc)

        commands_info = Group(
            Text("Commands", style=self.theme.subtitle), commands_table
        )

        files_info = Group(
            Text("Attaching Files", style=self.theme.subtitle),
            Text(
                "Mention any valid file path in your message to attach it.",
                style=self.theme.info,
            ),
        )

        help_content = Group(commands_info, Text(), files_info)
        self.console.print(help_content)
        self.console.print()

    def show_message(self, message: str, style=None):
        """Display a styled message."""
        self.console.print(message, style=style or self.theme.info)

    def show_error(self, message: str):
        """Display an error message."""
        self.console.print(Text(message, style=self.theme.error))
        self.console.print_exception(show_locals=True)

    def show_warning(self, message: str):
        """Display a warning message."""
        self.console.print(f"{message}", style=self.theme.warning)

    def show_success(self, message: str):
        """Display a success message."""
        self.console.print(f"{message}", style=self.theme.success)

    def show_farewell(self):
        """Display farewell message."""
        self.console.print()
        self.console.print(Text("Goodbye!", style=self.theme.info))

    def _clear_screen(self):
        """Clear the console screen."""
        self.console.clear()
