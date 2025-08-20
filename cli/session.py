from typing import Dict, Any, List, Optional

from sdk import Agent
from sdk.types import ToolCall

from .files import FileHandler
from .tools import ToolManager
from .commands import CommandHandler
from .interface import ChatInterface


class ChatSession:
    """Initialises the model and handles the chat loop."""

    def __init__(self, interface: ChatInterface, config: Dict[str, Any]):
        self.interface = interface
        self.config = config
        self.file_handler = FileHandler(interface)
        self.tool_manager = ToolManager(interface)
        self.command_handler = CommandHandler(interface)
        self.agent: Optional[Agent] = None

    async def run(self):
        """Run the main chat session."""
        try:
            await self._initialize_model()
            await self._chat_loop()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            self.interface.show_error(f"Unexpected error: {str(e)}")
            raise

    async def _initialize_model(self):
        """Initialize the model and display header."""
        self.agent = Agent(**self.config)

        model_info = await self.agent.describe_model()
        tools = self.agent.tool_manager.get_tools()
        prompt = True if self.config["prompt"] else False

        self.interface.show_header(model_info, len(tools), prompt)
        self.interface.show_message(
            "\nBegin a conversation, or type '/help' for more information.",
            style=self.interface.theme.system,
        )

    async def _chat_loop(self):
        """Main chat interaction loop."""
        while True:
            try:
                user_input = self.interface.get_user_input()
                if not user_input:
                    continue

                if await self.command_handler.handle_command(user_input, self.agent):
                    continue

                await self._process_user_message(user_input)

            except EOFError:
                break
            except Exception as e:
                self.interface.show_error(f"Error processing message: {str(e)}")

    async def _process_user_message(self, user_input: str):
        """Process a user message through the full conversation flow."""
        cleaned_prompt, extracted_files = self.file_handler.extract_files(user_input)
        all_files = getattr(self, "_initial_files", []) + extracted_files
        if not cleaned_prompt and all_files:
            cleaned_prompt = "Please analyze the attached files."

        await self._process_conversation_turn(cleaned_prompt, all_files)

    async def _process_conversation_turn(self, prompt: str, files: List[str]):
        """Process a complete conversation turn with potential tool calls."""
        self.interface.console.print()
        stream = self.agent.stream_response(prompt, files)

        while True:
            tool_calls = []
            text_stream_started = False

            with self.interface.console.status(
                "Thinking...", spinner_style=self.interface.theme.spinner
            ) as status:
                async for part in stream:
                    if part.kind == "text":
                        if not text_stream_started:
                            status.stop()
                            self.interface.start_stream()
                            text_stream_started = True

                        self.interface.update_stream(part.data)

                    elif part.kind == "tool_call":
                        if text_stream_started:
                            self.interface.stop_stream()
                            text_stream_started = False

                        status.stop()
                        tool_calls.append(part.data)

            if text_stream_started:
                self.interface.stop_stream()

            if not tool_calls:
                break

            tool_results = await self._execute_tool_calls(tool_calls)
            if not tool_results:
                self.interface.show_error("Tool execution failed.")
                break

            self.agent.history.extend(tool_results)
            stream = self.agent.stream_response(prompt=None)

    async def _execute_tool_calls(self, tool_calls: List[ToolCall]) -> List:
        return await self.tool_manager.process_tool_calls(self.agent, tool_calls)
