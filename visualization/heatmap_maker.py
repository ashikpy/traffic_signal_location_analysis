from rich.prompt import IntPrompt
from rich.prompt import Prompt
from utils.csv_region_selector import csv_region_selector
from utils.rich_components import bold_input
from utils.zoom_center_plotly import zoom_center
import pandas as pd
import plotly.express as px
from rich.console import Console

console = Console()

# NEEDED


def main():
    input_file, region_name = csv_region_selector()

    console.print(f"[bold yellow]Selected region:[/bold yellow] {region_name}")

    # ask for radius input
    radius = IntPrompt.ask("Enter the radius for the heatmap", default=10)
    opacity = float(Prompt.ask(
        "Enter the opacity for the heatmap (0.0 - 1.0)", default="1.0"))

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
        radius=radius,
        center=center,
        zoom=zoom,
        map_style='open-street-map',
        color_continuous_scale='rainbow',
        title=f'Density Map of Traffic Signals in {region_name}',
        labels={'lat': 'Latitude', 'lon': 'Longitude'},
        hover_name='id' if 'id' in df.columns else None
    )

    fig.update_traces(opacity=opacity)
    fig.show()


if __name__ == "__main__":
    main()
