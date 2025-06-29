from rich import box
from scripts import (
    get_traffic_geojson_by_name,
    geojson_to_csv
)

from visualization import (
    lon_lat_visualizer
)


from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text


console = Console()

available_scripts = [
    ("Get GeoJSON by name", get_traffic_geojson_by_name.main),
    ("Convert GeoJSON to CSV", geojson_to_csv.main)
]


available_visualizations = [
    ("Visualize From CSV (lon/lat)", lon_lat_visualizer.main)
]


def main():
    while True:
        console.print(Panel(
            Text("▶ Welcome to Traffic Data Analysis Tool",  style="bold blue"),  expand=False))

        script_list_text = "\n".join(
            f"[bold green]{i}[/bold green]. {name}"
            for i, (name, _) in enumerate(available_scripts, start=1)
        )
        console.print(Panel(script_list_text, title="Available Scripts",
                      box=box.ROUNDED, style="green", expand=False))

        offset = len(available_scripts)

        viz_list_text = "\n".join(
            f"[bold cyan]{i + offset}[/bold cyan]. {name}"
            for i, (name, _) in enumerate(available_visualizations, start=1)
        )
        console.print(Panel(viz_list_text, title="Available Visualizations",
                      box=box.ROUNDED, style="cyan", expand=False))

        try:
            choice = int(Prompt.ask(
                "\n[bold yellow]Select an option (0: Exit)[/bold yellow]"))
        except ValueError:
            console.print(
                "[bold red]Invalid input. Please enter a number.[/bold red]")
            continue

        if choice == 0:
            console.print("[bold red]Exiting...[/bold red]\n")
            break
        elif 1 <= choice <= offset:
            _, func = available_scripts[choice - 1]
            func()
        elif offset < choice <= offset + len(available_visualizations):
            _, func = available_visualizations[choice - offset - 1]
            func()
        else:
            console.print("[bold red]Invalid choice. Try again.[/bold red]")


if __name__ == "__main__":
    main()
