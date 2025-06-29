from rich.console import Console
from rich.panel import Panel
from rich import box


console = Console()


def rich_tablulate(data):
    file_list_text = "\n".join(
        f"[bold green]{idx}[/bold green]: {file.split('/')[-1].split('.')[0].split('_')[0].capitalize()}"
        for idx, file in enumerate(data)
    )
    console.print(Panel(file_list_text, title="Available GeoJSON Files",
                        box=box.ROUNDED, style="cyan", expand=False))
    return
