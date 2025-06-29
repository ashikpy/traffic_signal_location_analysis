import geopandas as gpd
from utils.tabulate_dir import tabulate_files
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
import numpy as np

CSVS_DIR = "data/state_csv"
OUTPUT_DIR = "output_maps/state_wise_traffic_maps"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():
    dir_list, tabulated_list = tabulate_files(CSVS_DIR, "csv")
    print("Available CSV files")
    print(tabulated_list)

    verification = input(
        "Do you want to visualize the traffic signals in each state? (Y/N): ").strip().upper()

    if verification == "Y":
        print("Traffic signal maps will be saved to /output_maps/state_wise_traffic_maps")
        for i, csv_path in enumerate(dir_list, 1):
            state_file = os.path.basename(csv_path)
            state_name = state_file.replace(".csv", "")
            print(f"[{i}/{len(dir_list)}] Visualizing: {state_name}")

            try:
                df = gpd.read_file(csv_path)
            except Exception as e:
                print(f"Failed to load {csv_path}: {e}")
                continue

            # Create GeoDataFrame with proper CRS
            gdf = gpd.GeoDataFrame(
                df,
                geometry=gpd.points_from_xy(df.lon, df.lat),
                crs="EPSG:4326"
            )

            if gdf.empty:
                print(f"Skipped {state_name}: No valid data points.")
                continue

            # Setup figure with high quality settings
            fig = plt.figure(figsize=(12, 10), dpi=300)
            ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

            # Add high-resolution geographic features
            ax.add_feature(cfeature.LAND.with_scale(
                '10m'), facecolor='#f0f0f0')
            ax.add_feature(cfeature.OCEAN.with_scale(
                '10m'), facecolor='#a6cee3')
            ax.add_feature(cfeature.COASTLINE.with_scale('10m'), linewidth=0.7)
            ax.add_feature(cfeature.BORDERS.with_scale(
                '10m'), linestyle=':', linewidth=0.7)
            ax.add_feature(cfeature.STATES.with_scale('10m'), linewidth=0.5)

            # Plot traffic signals with proper styling
            gdf.plot(
                ax=ax,
                color='red',
                edgecolor='darkred',
                markersize=15,
                alpha=0.8,
                transform=ccrs.PlateCarree(),
                zorder=10
            )

            # Set dynamic viewport based on data extent
            minx, miny, maxx, maxy = gdf.total_bounds
            width = maxx - minx
            height = maxy - miny

            # Add buffer around points (10% of range or 1 degree if small)
            x_buffer = max(width * 0.1, 0.5)
            y_buffer = max(height * 0.1, 0.5)

            ax.set_extent([
                minx - x_buffer,
                maxx + x_buffer,
                miny - y_buffer,
                maxy + y_buffer
            ], crs=ccrs.PlateCarree())

            # Add gridlines and labels
            gl = ax.gridlines(
                draw_labels=True,
                linewidth=0.5,
                color='gray',
                alpha=0.5,
                linestyle='--'
            )
            gl.top_labels = False
            gl.right_labels = False
            gl.xlabel_style = {'size': 8}
            gl.ylabel_style = {'size': 8}

            plt.title(f"Traffic Signals in {state_name}", fontsize=16, pad=20)

            # Save high-quality output
            output_path = os.path.join(
                OUTPUT_DIR,
                f"{state_name}_outline_map.png"
            )
            plt.savefig(output_path, bbox_inches='tight', dpi=300)
            plt.close()
            print(f"High-quality map saved for {state_name}")
    else:
        print("Visualization cancelled.")


if __name__ == "__main__":
    main()
