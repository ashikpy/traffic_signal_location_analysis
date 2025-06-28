import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from tkinter.filedialog import askopenfilename


def main():
    input_file = askopenfilename()
    region_name = input("Enter the region name: ")

    df = pd.read_csv(input_file)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(
        df.lon, df.lat), crs="EPSG:4326")
    gdf = gdf.to_crs(epsg=3857)

    # Plot the data
    ax = gdf.plot(marker='o', color='red', markersize=2, figsize=(8, 8))
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=5)
    plt.title(f"Traffic Lights in {region_name}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    plt.show()


if __name__ == "__main__":
    main()
