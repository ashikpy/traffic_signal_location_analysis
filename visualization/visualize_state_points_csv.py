import geopandas as gpd
from utils.tabulate_dir import tabulate_files
import matplotlib.pyplot as plt
import contextily as ctx
import os


CSVS_DIR = "data/state_csv"
OUTPUT_DIR = "output_maps/state_wise_traffic_maps"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():
    dir_list, tabluated_list = tabulate_files(CSVS_DIR, "csv")
    print("Available CSV files")
    print(tabluated_list)

    verification = input(
        "Do you want to visualize the traffic signals in each of the states? (Y/N): ").strip().upper()

    if verification == "Y":
        print("The traffic signal maps will be saved to /output_maps/state_wise_traffic_maps dir.")
        for i, csv_path in enumerate(dir_list, 1):
            state_file = os.path.basename(csv_path)
            state_name = state_file.replace(".csv", "")
            print(f"[{i}/{len(dir_list)}] Visualizing: {state_name}")

            try:
                df = gpd.read_file(csv_path)
            except Exception as e:
                print(f"Failed to load {csv_path}: {e}")
                continue

            gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(
                df.lon, df.lat), crs="EPSG:4326")
            gdf = gdf.to_crs(epsg=3857)

            if gdf.empty:
                print(f"Skipped {state_name}: GeoDataFrame is empty.")
                continue

            ax = gdf.plot(color='red',
                          edgecolor='black', figsize=(15, 15))
            ctx.add_basemap(
                ax, source=ctx.providers.OpenStreetMap.Mapnik)

            plt.title(f"Traffic Signals in {state_name}")
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            output_path = os.path.join(
                OUTPUT_DIR, f"{state_name}_traffic_map.png")
            plt.savefig(output_path, bbox_inches='tight')
            plt.close()
            print(f"Map saved for {state_name}")
    else:
        print("Visualization cancelled.")


if __name__ == "__main__":
    main()
