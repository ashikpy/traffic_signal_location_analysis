import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from tkinter.filedialog import askopenfilename


def main():
    input_file = askopenfilename()

    # Read the csv file

    df = pd.read_csv(input_file)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(
        df.lon, df.lat), crs="EPSG:4326")
    gdf = gdf.to_crs(epsg=3857)

    # Find the outliers based on the z-score
    gdf['z_score'] = (gdf['lat'] - gdf['lat'].mean()) / gdf['lat'].std()
    outliers = gdf[gdf['z_score'].abs() > 3]
    print(f"Number of outliers detected: {len(outliers)}")
    print(outliers[['lon', 'lat', 'z_score']])

    # Plot the data
    ax = gdf.plot(marker='o', color='red', markersize=2, figsize=(8, 8))
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=5)
    plt.title("Traffic Lights Outliers Detection")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.scatter(outliers['lon'], outliers['lat'],
                color='blue', label='Outliers', s=10)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
