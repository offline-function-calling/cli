#!/usr/bin/env python3

import asyncio
from typing import Optional, List

import typer

from rich.console import Console
from sdk import OllamaProvider

from cli.session import ChatSession
from cli.theme import Theme
from cli.interface import ChatInterface


app = typer.Typer(
    name="cli",
    help="Offline Function Calling CLI",
    add_completion=False,
    no_args_is_help=True,
)


@app.command()
def chat(
    model_name: str = typer.Option(
        "gemma3:12b-fc", "--model", "-m", help="The Ollama model to use"
    ),
    ollama_host: str = typer.Option(
        "http://localhost:11434", "--ollama", "-o", help="The Ollama server to use"
    ),
    system_prompt: Optional[str] = typer.Option(
        None, "--system", "-s", help="The system prompt to use"
    ),
    tools_dir: Optional[List[str]] = typer.Option(
        None, "--tools", "-t", help="Directory containing tool definitions"
    ),
):
    """Start an interactive chat session with function calling capabilities."""

    console = Console()
    theme = Theme()
    interface = ChatInterface(console, theme)

    config = {
        "provider": OllamaProvider(model_name, ollama_host),
        "prompt": system_prompt,
        "tools": tools_dir,
    }

    session = ChatSession(interface, config)

    try:
        asyncio.run(session.run())
    except KeyboardInterrupt:
        pass
    finally:
        interface.show_farewell()


if __name__ == "__main__":
    app()
