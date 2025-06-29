import pandas as pd
import plotly.express as px
import numpy as np
import plotly.io as pio
from utils.zoom_center_plotly import zoom_center


# Load your data
df = pd.read_csv('data/india.csv')

# Compute zoom and center dynamically
zoom, center = zoom_center(
    df['lon'].tolist(), df['lat'].tolist())

# Create the density map
fig = px.density_map(df, lat='lat', lon='lon',
                     radius=4,
                     zoom=zoom,
                     map_style='basic',
                     color_continuous_scale='rainbow',
                     center=center,
                     title='Density Map of Traffic Signals in India',
                     labels={'lat': 'Latitude', 'lon': 'Longitude'},
                     height=1080,
                     width=1080,
                     )
config = {
    'toImageButtonOptions': {
        'format': 'webp',  # one of png, svg, jpeg, webp
        'filename': 'test',
        'height': 1080,
        'width': 1080,
        'scale': 10}
}

fig.show(config=config)
