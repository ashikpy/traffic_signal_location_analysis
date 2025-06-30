from rich.console import Console

console = Console()


def line_title(text):
    console.rule(
        f"[bold blue][green]{text}[/green][/bold blue]")
