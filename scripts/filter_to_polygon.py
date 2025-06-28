from tkinter.filedialog import askopenfilename
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx


def main():
    # Get the polygon of usa
    usa_polygon = askopenfilename(title="Select USA Polygon File",
                                  filetypes=[("GeoJSON files", "*.geojson")])

    if not usa_polygon:
        print("No file selected.")
        return
    print(f"USA Polygon File: {usa_polygon}")

    # Get the input file which needs to to be filtered
    input_file = askopenfilename(title="Select Input File")

    # the input file is a csv file with the columns 'lon' and 'lat'
    if not input_file:
        print("No input file selected.")
        return
    print(f"Input File: {input_file}")

    # Read the input file
    df = pd.read_csv(input_file)

    if 'lon' not in df.columns or 'lat' not in df.columns:
        print("Input file must contain 'lon' and 'lat' columns.")
        return

    # Read the USA polygon file
    usa_polygon_df = gpd.read_file(usa_polygon)
    if usa_polygon_df.empty:
        print("USA polygon file is empty or invalid.")
        return

    # Convert the input DataFrame to a GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(
        df.lon, df.lat), crs="EPSG:4326")
    gdf = gdf.to_crs(usa_polygon_df.crs)

    # Filter the points that are within the USA polygon
    gdf_filtered = gdf[gdf.geometry.within(
        usa_polygon_df.geometry.union_all())]

    if gdf_filtered.empty:
        print("No points found within the USA polygon.")
        return

    # Save the filtered data to a new CSV file
    output_file = input_file.replace(".csv", "_filtered.csv")
    gdf_filtered.to_csv(output_file, index=False)
    print(f"Filtered data saved to {output_file}")


if __name__ == "__main__":
    main()
