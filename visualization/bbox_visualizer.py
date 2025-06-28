import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import box
import geopandas as gpd

# Define bounding box: (min_lat, min_lon, max_lat, max_lon)
min_lat, min_lon, max_lat, max_lon = 24.396308, -125.0, 49.384358, -66.93457

# Create bounding box geometry (Shapely uses (minx, miny, maxx, maxy) = (lon, lat, lon, lat))
bbox = box(min_lon, min_lat, max_lon, max_lat)
gdf = gpd.GeoDataFrame(geometry=[bbox], crs="EPSG:4326")

# Reproject to Web Mercator
gdf_web_mercator = gdf.to_crs(epsg=3857)

# Prepare corner points
corner_points = [
    (min_lon, min_lat),  # Bottom-left
    (min_lon, max_lat),  # Top-left
    (max_lon, min_lat),  # Bottom-right
    (max_lon, max_lat),  # Top-right
]

corner_gdf = gpd.GeoDataFrame(
    geometry=gpd.points_from_xy(
        [pt[0] for pt in corner_points],
        [pt[1] for pt in corner_points]
    ),
    crs="EPSG:4326"
).to_crs(epsg=3857)

# Plot
fig, ax = plt.subplots(figsize=(7, 7))
gdf_web_mercator.boundary.plot(ax=ax, edgecolor='red', linewidth=2)
corner_gdf.plot(ax=ax, color='blue', markersize=50)

# Annotate points
coords_labels = [
    ("Bottom-left", min_lat, min_lon),
    ("Top-left", max_lat, min_lon),
    ("Bottom-right", min_lat, max_lon),
    ("Top-right", max_lat, max_lon),
]
for i, (x, y) in enumerate(zip(corner_gdf.geometry.x, corner_gdf.geometry.y)):
    ax.text(x, y, f"P{i+1}", fontsize=10, color='black', ha='right')

ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=4)
ax.set_axis_off()
plt.title("Bounding Box Visualization with Corner Points")

legend_text = "\n".join([
    f"P1: Bottom-left ({min_lat:.2f}, {min_lon:.2f})",
    f"P2: Top-left ({max_lat:.2f}, {min_lon:.2f})",
    f"P3: Bottom-right ({min_lat:.2f}, {max_lon:.2f})",
    f"P4: Top-right ({max_lat:.2f}, {max_lon:.2f})",
])
plt.gcf().text(0.01, 0.01, legend_text, fontsize=9, va='bottom', ha='left')

plt.tight_layout()
plt.show()
