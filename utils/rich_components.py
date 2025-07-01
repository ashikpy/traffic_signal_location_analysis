from rich import box
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from utils.line_title import line_title

console = Console()


def print_panel(text):
    console.print(Panel(
        Text(f"▶ {text}",  style="bold blue"),  expand=False))
