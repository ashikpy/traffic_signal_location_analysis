import plotly.graph_objects as go
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from utils.zoom_center_plotly import zoom_center

# Load CSV (assumes columns: lat, lon)
df = pd.read_csv("data/india.csv")
coords = df[['lat', 'lon']].values

# Normalize
coords_scaled = StandardScaler().fit_transform(coords)

# Run DBSCAN
db = DBSCAN(eps=0.1, min_samples=5).fit(coords_scaled)
labels = db.labels_
df['cluster'] = labels

# Count and print number of points per cluster
cluster_counts = df['cluster'].value_counts().sort_index()
# Print the cluster having the most points
largest_cluster = cluster_counts.idxmax()
print(
    f"Largest cluster: {largest_cluster}th cluster with {cluster_counts.max()} points")

# Print the cluster having the least points
smallest_cluster = cluster_counts.idxmin()
print(
    f"Smallest cluster: {smallest_cluster}th cluster with {cluster_counts.min()} points")

# Print the number of clusters excluding noise
num_clusters = len(cluster_counts) - (1 if -1 in cluster_counts else 0)
print(f"Number of clusters (excluding noise): {num_clusters}")

# Print the number of noise points
num_noise = (labels == -1).sum()


# Prepare Plotly figure
fig = go.Figure()

sorted_labels = cluster_counts.sort_values(ascending=False).index.tolist()
for label in sorted_labels:
    cluster_data = df[df['cluster'] == label]
    if label == -1:
        fig.add_trace(go.Scattergeo(
            lon=cluster_data['lon'],
            lat=cluster_data['lat'],
            mode='markers',
            marker=dict(symbol='x', color='black'),
            name='Noise'
        ))
    else:
        fig.add_trace(go.Scattergeo(
            lon=cluster_data['lon'],
            lat=cluster_data['lat'],
            mode='markers',
            marker=dict(size=6),
            name=f'Cluster {label} ({len(cluster_data)})'
        ))
        # Draw bounding box
        min_lon, max_lon = cluster_data['lon'].min(), cluster_data['lon'].max()
        min_lat, max_lat = cluster_data['lat'].min(), cluster_data['lat'].max()
        fig.add_trace(go.Scattergeo(
            lon=[min_lon, max_lon, max_lon, min_lon, min_lon],
            lat=[min_lat, min_lat, max_lat, max_lat, min_lat],
            mode='lines',
            line=dict(color='green', width=2),
            name=f'Bounding Box {label}',
            showlegend=False
        ))

# Calculate bounding box areas and find the largest one
bbox_areas = {}
for label in sorted_labels:
    if label == -1:
        continue
    cluster_data = df[df['cluster'] == label]
    min_lon, max_lon = cluster_data['lon'].min(), cluster_data['lon'].max()
    min_lat, max_lat = cluster_data['lat'].min(), cluster_data['lat'].max()
    area = (max_lon - min_lon) * (max_lat - min_lat)
    bbox_areas[label] = area

largest_bbox_label = max(bbox_areas, key=bbox_areas.get)
print(
    f"Largest bounding box: Cluster {largest_bbox_label} with area {bbox_areas[largest_bbox_label]:.6f}")

fig.update_layout(
    title="DBSCAN Clustering (Plotly)",
    geo=dict(
        scope='asia',
        showland=True,
        landcolor="rgb(243, 243, 243)",
        countrycolor="rgb(204, 204, 204)",
    ),
    legend=dict(x=0.01, y=0.99)
)

fig.show()
