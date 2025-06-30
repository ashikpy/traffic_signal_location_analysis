import geopandas as gpd
from utils.tabulate_dir import tabulate_files
import os
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from utils.rich_tabulate import rich_tablulate
from utils.contstants import csv_dir, geojson_dir
from utils.csv_region_selector import csv_region_selector


# NEEDED

def convert_geojson_to_csv(geojson_path, csv_dir):
    # Load GeoJSON data
    gdf = gpd.read_file(geojson_path)

    # Strip the file name.
    file_name = geojson_path.split("/")[-1].split(".")[0]

    # Extract longitude and latitude
    gdf["lon"] = gdf.geometry.x
    gdf["lat"] = gdf.geometry.y

    # Export to CSV
    gdf[["lat", "lon"]].to_csv(
        csv_dir + f"/{file_name}.csv", index=False)

    return f"Conversion complete: {geojson_path} to {csv_dir}/{file_name}.csv"


def main():

    target_ext = csv_dir
    # Check if these directories exist
    try:
        os.makedirs(geojson_dir, exist_ok=True)
        os.makedirs(target_ext, exist_ok=True)
    except Exception as e:
        print(f"Error creating directories: {e}")
        return

    console = Console()

    # Tabulate the files in the directory
    orignal_list = tabulate_files(geojson_dir, "geojson")[0]

    if not orignal_list:
        console.print(
            "[bold red]No GeoJSON files found in the directory.[/bold red]")
        return
    else:
        rich_tablulate(orignal_list)

    try:
        index = int(Prompt.ask(
            "[bold yellow]Enter the index of the GeoJSON file to convert (N to cancel)[/bold yellow]"))
        if index < 0 or index >= len(orignal_list):
            raise IndexError("Index out of range.")
        geojson_path = orignal_list[index]
        console.print(f"[bold blue]Selected file:[/bold blue] {geojson_path}")
        verification = Prompt.ask(
            f"[bold magenta]Your CSV will be saved as [italic]{geojson_path.split('/')[-1].split('.')[0]}.csv[/italic]. Proceed? (Y/N)[/bold magenta]"
        ).strip().upper()
        if verification != 'Y':
            console.print("[bold red]Conversion cancelled.[/bold red]")
            return
        else:
            result = convert_geojson_to_csv(geojson_path, target_ext)
            console.print(f"[bold green]{result}[/bold green]")
    except (ValueError, IndexError) as e:
        console.print(f"[bold red]Invalid input:[/bold red] {e}")
        return


if __name__ == "__main__":
    main()
