import json
import asyncio

from typing import List, Dict, Any
from textwrap import dedent

from sdk.types import Message, Part, ToolCall
from .interface import ChatInterface


class ToolManager:
    """Manages tool execution with user consent and clean visual feedback."""

    def __init__(self, interface: ChatInterface):
        self.interface = interface

    async def process_tool_calls(
        self, model, tool_calls: List[ToolCall]
    ) -> List[Message]:
        """Execute tool calls with user consent and clean UI."""
        if not tool_calls:
            return []

        tool_results = []
        executed_count = 0
        failed_count = 0

        for i, tool_call in enumerate(tool_calls, 1):
            tool_name = tool_call.tool
            arguments = tool_call.parameters

            try:
                tool_executor = lambda: self._execute_tool(model, tool_name, arguments)

                result = await self.interface.execute_tool_with_consent(
                    tool_name, arguments, tool_executor
                )

                if result is None:
                    tool_results.append(self._create_denial_message(tool_call))
                    self.interface.show_warning(
                        "\nTool execution sequence aborted by user."
                    )
                    break
                else:
                    tool_results.append(self._create_success_message(tool_call, result))
                    executed_count += 1

            except Exception as e:
                tool_results.append(self._create_error_message(tool_call, e))
                failed_count += 1
                self.interface.show_error(
                    f"Tool {tool_name} execution failed: {str(e)}"
                )

        if len(tool_calls) > 1:
            self.interface.show_tools_summary(
                len(tool_calls), executed_count, failed_count
            )

        return tool_results

    async def _execute_tool(self, model, tool_name: str, arguments: Dict[str, Any]):
        """Execute the actual tool call."""
        return await asyncio.to_thread(
            model.tool_manager.execute_tool, name=tool_name, kwargs=arguments
        )

    def _create_denial_message(self, tool_call: ToolCall) -> Message:
        """Create message for denied tool execution."""
        return Message(
            role="tool",
            parts=[
                Part(
                    kind="text",
                    data=dedent(f"""
                    ```tool_result
                    {{
                        "error": {{
                            "name": "ToolExecutionDenied",
                            "description": "User denied execution of tool '{tool_call.tool.name}'."
                        }}
                    }}
                    ```
                """),
                ),
                Part(kind="tool_call", data=tool_call),
            ],
        )

    def _create_success_message(self, tool_call: ToolCall, result) -> Message:
        """Create message for successful tool execution."""
        return Message(
            role="tool",
            parts=[
                Part(
                    kind="text",
                    data=dedent(f"""
                    ```tool_result
                    {{
                        "result": {json.dumps(result)}
                    }}
                    ```
                """),
                ),
                Part(kind="tool_call", data=tool_call),
            ],
        )

    def _create_error_message(self, tool_call: ToolCall, error: Exception) -> Message:
        """Create message for failed tool execution."""
        return Message(
            role="tool",
            parts=[
                Part(
                    kind="text",
                    data=dedent(f"""
                    ```tool_result
                    {{
                        "error": {{
                            "name": "{type(error).__name__}",
                            "description": "{str(error)}"
                        }}
                    }}
                    ```
                """),
                ),
                Part(kind="tool_call", data=tool_call),
            ],
        )
