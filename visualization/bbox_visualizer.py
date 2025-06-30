import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.csv_region_selector import csv_region_selector
import re

# NEED


def parse_bbox_string(bbox_str):
    matches = re.findall(r'(\w+)=([-+]?[0-9]*\.?[0-9]+)', bbox_str)
    return {k: float(v) for k, v in matches}


def bbox_visualzier(bbox, cluster_name, input_file, region_name):
    if isinstance(bbox, str):
        bbox = parse_bbox_string(bbox)

    df = pd.read_csv(input_file)

    # Filter by bounding box
    min_lon, min_lat = bbox['min_lon'], bbox['min_lat']
    max_lon, max_lat = bbox['max_lon'], bbox['max_lat']

    df_filtered = df[(df['lon'] >= min_lon) & (df['lon'] <= max_lon) &
                     (df['lat'] >= min_lat) & (df['lat'] <= max_lat)]

    # Plot using Plotly
    fig = px.scatter_map(df_filtered,
                         lat="lat",
                         lon="lon",
                         zoom=5,
                         title=f"Points in {cluster_name} in {region_name}",
                         height=600)
    fig.update_layout(map_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})

    fig.add_trace(go.Scattermap(
        mode="lines",
        lon=[min_lon, max_lon, max_lon, min_lon, min_lon],
        lat=[min_lat, min_lat, max_lat, max_lat, min_lat],
        line=dict(width=2, color='red'),
        name='Bounding Box'
    ))

    fig.show()


if __name__ == "__main__":
    example_bbox = "min_lon=6.03877, min_lat=47.76010, max_lon=11.09390, max_lat=53.68652"
    cluster_name = "Germany Cluster"
    bbox_visualzier(example_bbox, cluster_name)
