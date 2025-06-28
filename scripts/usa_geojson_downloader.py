# took 45 mins

import requests
import time
import csv

# Bounding box for mainland USA
USA_BBOX = (24.396308, -125.0, 49.384358, -66.93457)
LAT_STEP = 1.0
LON_STEP = 1.0
OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def fetch_tile(s, w, n, e):
    query = f"""
    [out:json][timeout:120];
    node["highway"="traffic_signals"]({s},{w},{n},{e});
    out body;
    """
    try:
        response = requests.post(OVERPASS_URL, data=query)
        response.raise_for_status()
        return response.json().get("elements", [])
    except Exception as e:
        print(f"Failed for tile ({s},{w},{n},{e}): {e}")
        return []


def main():
    with open("USA.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "lat", "lon", "tags"])

        lat = USA_BBOX[0]
        while lat < USA_BBOX[2]:
            lon = USA_BBOX[1]
            while lon < USA_BBOX[3]:
                s, w = lat, lon
                n, e = lat + LAT_STEP, lon + LON_STEP
                print(f"Fetching tile: {s}, {w}, {n}, {e}")
                signals = fetch_tile(s, w, n, e)
                for node in signals:
                    writer.writerow([
                        node.get("id"),
                        node.get("lat"),
                        node.get("lon"),
                        str(node.get("tags", {}))
                    ])
                time.sleep(1)
                lon += LON_STEP
            lat += LAT_STEP

    print("Done: data saved to USA.csv")


if __name__ == "__main__":
    main()
