import geopandas as gpd
from utils.tabulate_dir import tabulate_files
import os


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
    geojson_dir = "geojson"
    target_ext = "data"

    # Check if these directories exist
    try:
        os.makedirs(geojson_dir, exist_ok=True)
        os.makedirs(target_ext, exist_ok=True)
    except Exception as e:
        print(f"Error creating directories: {e}")
        return

    # Tabulate the files in the directory
    orignal_list, tabulated_list = tabulate_files(geojson_dir, "geojson")

    if not orignal_list:
        print("No GeoJSON files found in the directory.")
        return
    else:
        print("Available GeoJSON files:")
        print(tabulated_list)

    try:
        index = int(input("Enter the index of the GeoJSON file to convert: "))
        if index < 0 or index >= len(orignal_list):
            raise IndexError("Index out of range.")
        geojson_path = orignal_list[index]
        print(f"Selected file: {geojson_path}")
        verification = input(
            f"Your C will be saved in the 'data' directory with the name {geojson_path.split('/')[-1].split('.')[0]}.csv Ok? (Y/N) "
        ).strip().upper()
        if verification != 'Y':
            print("Conversion cancelled.")
            return
        else:
            result = convert_geojson_to_csv(geojson_path, target_ext)
            print(result)
    except (ValueError, IndexError) as e:
        print(f"Invalid input: {e}")
        return


if __name__ == "__main__":
    main()
