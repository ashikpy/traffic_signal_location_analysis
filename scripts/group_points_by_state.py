import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from utils.tabulate_dir import tabulate_files

# Paths
INDIA_CSV_PATH = "data/india.csv"
GEOJSON_FOLDER = "states_geojson"
OUTPUT_FOLDER = "data/state_csv"


def main():

    # Load all points
    df = pd.read_csv(INDIA_CSV_PATH)
    gdf_points = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")

    # Ensure output directory exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Loop through each state's GeoJSON file
    for filename in os.listdir(GEOJSON_FOLDER):
        if filename.endswith(".geojson"):
            region_name = filename.replace(".geojson", "")
            geojson_path = os.path.join(GEOJSON_FOLDER, filename)

            # Load polygon
            gdf_polygon = gpd.read_file(geojson_path).to_crs("EPSG:4326")

            # Spatial join: filter points inside the polygon
            within_state = gdf_points[gdf_points.within(
                gdf_polygon.geometry.union_all())]

            # Save to CSV

            out_df = within_state[['lat', 'lon']]  # only save lat/lon
            output_path = os.path.join(OUTPUT_FOLDER, f"{region_name}.csv")
            out_df.to_csv(output_path, index=False)
            print(f"Saved {len(out_df)} points to {output_path}")


if __name__ == "__main__":
    main()
