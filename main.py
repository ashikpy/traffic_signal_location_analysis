from rich.console import Console
from scripts import (
    get_traffic_geojson_by_name,
    geojson_to_csv,
    merge_csvs,
)

from utils.rich_components import bold_color_print, bold_input, box_text, numbered_list_panel, print_panel, line_title
from visualization import (
    lon_lat_visualizer,
    dbscan_cluster_visualizer,
    heatmap_maker,
    visualize_states
)


available_scripts = [
    ("Get GeoJSON by name", get_traffic_geojson_by_name.main),
    ("Convert GeoJSON to CSV", geojson_to_csv.main),
    ("Merge CSVs", merge_csvs.main),
]


available_visualizations = [
    ("Visualize Scatter Plot", lon_lat_visualizer.main),
    ("Visualize Heatmap", heatmap_maker.main),
    ("Visualize Clusters with DBSCAN",
     dbscan_cluster_visualizer.main),
    ("Visualize States", visualize_states.main),
]


console = Console()


def main():
    try:
        while True:
            print_panel("Welcome to Traffic Data Analysis Tool")

            # Display Available Scripts
            script_list_text = numbered_list_panel(available_scripts, "green")
            box_text(script_list_text, "Available Scripts", "green")

            # Display Available Visualizations
            viz_list_text = numbered_list_panel(
                available_visualizations, "cyan", start=len(available_scripts) + 1)
            box_text(viz_list_text, "Available Visualizations", "cyan")

            # Prompt for User Input
            bold_color_print(
                "Enter 0 or any non-number to exit.", "magenta")
            raw_input = bold_input("Select an option", "yellow")

            try:
                choice = int(raw_input)
            except ValueError:
                bold_color_print("Exiting...\n", "red")
                break

            offset = len(available_scripts)

            if choice == 0:
                bold_color_print("Exiting...", "red")
                break
            elif 1 <= choice <= offset:
                name, func = available_scripts[choice - 1]
                print("")
                line_title(f"Running Script: {name}")
                print("")
                func()
            elif offset < choice <= offset + len(available_visualizations):
                name, func = available_visualizations[choice - offset - 1]
                print("")
                line_title(f"Running Visualization: {name}")
                print("")
                func()
            else:
                bold_color_print("Invalid choice. Try Again.", "red")
    except KeyboardInterrupt:
        bold_color_print("Interrupted. Exiting", "red", new_line=True)


if __name__ == "__main__":
    main()
