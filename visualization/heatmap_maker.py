from rich.prompt import IntPrompt
from utils.csv_region_selector import csv_region_selector
from utils.zoom_center_plotly import zoom_center
from utils.tabulate_dir import tabulate_files
from utils.rich_tabulate import rich_tablulate
import pandas as pd
import plotly.express as px
from rich.console import Console
from utils.contstants import csv_dir

console = Console()


def main():
    input_file, region_name = csv_region_selector()

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
