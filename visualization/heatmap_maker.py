from rich.prompt import IntPrompt
from utils.zoom_center_plotly import zoom_center
from utils.tabulate_dir import tabulate_files
from utils.rich_tabulate import rich_tablulate
import pandas as pd
import plotly.express as px
from rich.console import Console

console = Console()


def main():
    csv_dir = "data/traffic_csv"
    original_file = tabulate_files(csv_dir, "csv")[0]
    rich_tablulate(original_file)

    try:
        input_index = IntPrompt.ask(
            "Select the index of the file to Visualize Heatmap")

    except (ValueError, KeyboardInterrupt):
        console.print(
            "[bold red]No input provided or invalid input. Exiting...[/bold red]")
        return

    if input_index is None:
        console.print("[bold red]No input received. Exiting...[/bold red]")
        return
    input_file = original_file[input_index]

    region_name = input_file.split(
        "/")[-1].split(".")[0].split("_")[0].capitalize()

    console.print(f"[bold yellow]Selected region:[/bold yellow] {region_name}")

    # Load your data
    df = pd.read_csv(input_file)
    if 'intensity' not in df.columns:
        df['intensity'] = 1

    # Compute zoom and center dynamically
    zoom, center = zoom_center(
        df['lon'].tolist(),
        df['lat'].tolist()
    )

    fig = px.density_map(
        df,
        lat='lat',
        lon='lon',
        z='intensity',
        radius=3,  # adjust this for spread
        center=center,
        zoom=zoom,
        map_style='open-street-map',
        color_continuous_scale='rainbow',
        title=f'Density Map of Traffic Signals in {region_name}',
        labels={'lat': 'Latitude', 'lon': 'Longitude'},
        hover_name='id' if 'id' in df.columns else None
    )

    fig.update_traces(opacity=0.7)  # optional for transparency
    fig.show()


if __name__ == "__main__":
    main()
