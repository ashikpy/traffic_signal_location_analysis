from utils.csv_region_selector import csv_region_selector
import pandas as pd
from rich.console import Console
import plotly.express as px
from utils.zoom_center_plotly import zoom_center
console = Console()

# NEEDED


def main():

    input_file, region_name = csv_region_selector()

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

    fig.update_traces(marker=dict(size=5, color="blue", opacity=0.5))
    fig.show()


if __name__ == "__main__":
    main()
