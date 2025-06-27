from utils.tabulate_dir import tabulate_files
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
geojson_dir = os.path.join(base_dir, "..", "states_geojson")
output_dir = os.path.join(base_dir, "..", "output_maps")


def main():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    original_list, tabulated_list = tabulate_files(geojson_dir, "geojson")

    print("Available GeoJSON files:")
    print(tabulated_list)

    verfication = input(
        "Do you want to visualize the states? (Y/N): ").strip().upper()

    if verfication == "Y":
        print("The Regions maps will be saved to /output_maps dir.")
        for i, geojson_path in enumerate(original_list, 1):
            state_file = os.path.basename(geojson_path)
            state_name = state_file.replace(".geojson", "")
            print(f"[{i}/{len(original_list)}] Visualizing: {state_name}")

            try:
                df = gpd.read_file(geojson_path)
            except Exception as e:
                print(f"Failed to load {geojson_path}: {e}")
                continue

            state_name = os.path.basename(geojson_path).split(".")[0]

            gdf = gpd.GeoDataFrame(df, geometry=df.geometry, crs="EPSG:4326")
            gdf = gdf.to_crs(epsg=3857)

            ax = gdf.plot(color='lightblue',
                          edgecolor='black', figsize=(10, 10))
            ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

            plt.title(f"Map of {state_name}")
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            output_path = os.path.join(output_dir, f"{state_name}_map.png")
            plt.savefig(output_path, bbox_inches='tight')
            plt.close()
            print(f"Map saved for {state_name}")
    else:
        print("Visualization cancelled.")


if __name__ == "__main__":
    main()
else:
    print("This script is intended to be run as a standalone program.")
    print("Please run it directly to visualize the states.")
    print("Exiting...")
