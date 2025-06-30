import time
import json
import os
import requests
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from utils.fancy_text_box import fancy_text_box

console = Console()

# NEEDED


def fetch_traffic_signals(city_name):
    console.print(
        Panel(Text("▶ Fetch GeoJSON by City Name", style="bold blue"), expand=False))
    query = f"""
    [out:json][timeout:300];
    area["name:en"="{city_name}"]->.searchArea;
    node["highway"="traffic_signals"](area.searchArea);
    out body;
    >;
    out skel qt;
    """

    overpass_url = "http://overpass-api.de/api/interpreter"

    fancy_text_box("Contacting OSM API")
    console.print("Waiting for response", end="")
    for _ in range(6):
        time.sleep(0.3)
        console.print(".", end="")
    console.print()

    response = requests.post(overpass_url, data=query)
    if response.status_code != 200:
        console.print(
            f"[bold red]Error: HTTP {response.status_code}[/bold red]")
        return

    data = response.json()

    features = []
    for element in data["elements"]:
        if element["type"] == "node":
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [element["lon"], element["lat"]],
                },
                "properties": element.get("tags", {}),
            })

    if not features:
        console.print(
            f"[bold yellow]No traffic signals found for {city_name}. Nothing was saved.[/bold yellow]")
        return

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    os.makedirs("data/traffic_geojson", exist_ok=True)
    filepath = f"data/traffic_geojson/{city_name.lower()}_traffic_signals.geojson"
    with open(filepath, "w") as f:
        json.dump(geojson, f, indent=2)

    console.print(f"[bold green]Saved to {filepath}[/bold green]")


def main():
    city_name = Prompt.ask("[bold cyan]Enter a city name[/bold cyan]")
    if not city_name:
        console.print("[bold red]City name cannot be empty.[/bold red]")
        return
    city_name = city_name.strip()
    fetch_traffic_signals(city_name)


if __name__ == "__main__":
    main()
