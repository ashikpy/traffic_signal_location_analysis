import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


def run_dbscan(csv_path, eps=0.1, min_samples=5):
    df = pd.read_csv(csv_path)
    coords = df[['lat', 'lon']].values
    coords_scaled = StandardScaler().fit_transform(coords)

    db = DBSCAN(eps=eps, min_samples=min_samples).fit(coords_scaled)
    df['cluster'] = db.labels_

    return df
