from dataclasses import dataclass
from rich.style import Style


@dataclass
class Theme:
    """Tokyo Night inspired theme for consistent UI styling."""

    # Core roles
    user: Style = Style(color="#7aa2f7", bold=True)
    assistant: Style = Style(color="#9ece6a")
    tools: Style = Style(color="#bb9af7", bold=True)
    system: Style = Style(color="#565f89", dim=True)

    # Status indicators
    success: Style = Style(color="#9ece6a", bold=True)
    warning: Style = Style(color="#e0af68", bold=True)
    error: Style = Style(color="#f7768e", bold=True)
    info: Style = Style(color="#7dcfff")

    # Interactive elements
    spinner: Style = Style(color="#bb9af7")
    prompt: Style = Style(color="#c0caf5")
    command: Style = Style(color="#7dcfff", bold=True)
    argument: Style = Style(color="#565f89", bold=True, dim=True)

    # UI components
    border: Style = Style(color="#414868")
    header_border: Style = Style(color="#7aa2f7")
    accent_border: Style = Style(color="#bb9af7")

    # Tool execution
    tool_pending: Style = Style(color="#e0af68")
    tool_success: Style = Style(color="#9ece6a")
    tool_error: Style = Style(color="#f7768e")

    # Typography
    title: Style = Style(color="#7aa2f7", bold=True)
    subtitle: Style = Style(color="#c0caf5", bold=True)
    dim: Style = Style(color="#565f89", dim=True)
    highlight: Style = Style(color="#bb9af7", bold=True)

    # Table styling
    table_header: Style = Style(color="#c0caf5", bold=True)
    table_border: Style = Style(color="#bb9af7")
