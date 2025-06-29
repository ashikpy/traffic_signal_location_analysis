from utils.tabulate_dir import tabulate_files
import contextily as ctx
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from rich import print
from rich.prompt import IntPrompt
from rich.panel import Panel
from rich.console import Console
from rich import box
from utils.rich_tabulate import rich_tablulate

console = Console()


def main():
    csv_dir = "data/traffic_csv"
    original_file = tabulate_files(csv_dir, "csv")[0]
    rich_tablulate(original_file)

    try:
        input_index = IntPrompt.ask(
            "Select the index of the file to visualize")
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
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(
        df.lon, df.lat), crs="EPSG:4326")
    gdf = gdf.to_crs(epsg=3857)

    # Plot the data
    ax = gdf.plot(marker='o', color='red', markersize=2, figsize=(8, 8))
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    plt.title(f"Traffic Lights in {region_name}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    plt.show()


if __name__ == "__main__":
    main()
