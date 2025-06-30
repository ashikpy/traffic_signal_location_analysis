from utils.tabulate_dir import tabulate_files
import pandas as pd
from rich.prompt import IntPrompt
from rich.console import Console
from utils.rich_tabulate import rich_tablulate
import plotly.express as px
from utils.zoom_center_plotly import zoom_center

console = Console()


def main():
    csv_dir = "data/traffic_csv"
    original_file = tabulate_files(csv_dir, "csv")[0]
    rich_tablulate(original_file)

    try:
        input_index = IntPrompt.ask(
            "Select the index of the file to Visualize Scatter Plot")
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

    df = pd.read_csv(input_file)

    zoom, center = zoom_center(
        lons=df["lon"].tolist(),
        lats=df["lat"].tolist()
    )

    fig = px.scatter_map(
        df,
        lat="lat",
        lon="lon",
        hover_name="id" if "id" in df.columns else None,
        center=center,
        zoom=zoom,
        map_style="open-street-map",
        title=f"Traffic Lights in {region_name}",
        labels={"lat": "Latitude", "lon": "Longitude",
                "id": "Traffic Light ID"} if "id" in df.columns else None
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        title=f"Traffic Lights in {region_name}",
        margin={"r": 0, "t": 30, "l": 0, "b": 0}
    )

    fig.update_traces(marker=dict(size=5, color="blue", opacity=0.1))
    fig.show()


if __name__ == "__main__":
    main()
