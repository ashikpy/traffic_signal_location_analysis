from rich import box
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text


console = Console()


def print_panel(text):
    console.print(Panel(
        Text(f"▶ {text}",  style="bold blue"),  expand=False))


def bold_color_print(text, color, new_line=False):
    if new_line:
        console.print(f"\n[bold {color}]{text}[/bold {color}]")
    console.print(f"[bold {color}]{text}[/bold {color}]")


def box_text(script_list_text, title, color):
    console.print(Panel(script_list_text, title=title,
                        box=box.ROUNDED, style=color, expand=False))


def numbered_list_panel(given_dict, color, start=1) -> str:
    return "\n".join(
        f"[bold {color}]{i}[/bold {color}]. {name}"
        for i, (name, _) in enumerate(given_dict, start=start)
    )


def bold_input(text, color="yellow", new_line=False):
    if new_line:
        return Prompt.ask(f"\n [bold {color}]{text}[/bold {color}]")
    return Prompt.ask(f"[bold {color}]{text}[/bold {color}]")


def line_title(text):
    console.rule(
        f"[bold blue][green]{text}[/green][/bold blue]")
