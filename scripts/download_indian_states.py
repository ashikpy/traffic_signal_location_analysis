import requests
import os
import json
from osm2geojson import json2geojson
from config.indian_regions import state_names, union_territories

# Create output folder
os.makedirs("states_geojson", exist_ok=True)


OVERPASS_URL = "https://overpass-api.de/api/interpreter"

for state in union_territories + state_names:
    print(f"⏳ Downloading: {state}")

    query = f"""
    [out:json][timeout:60];
    area["name"="India"][admin_level=2]->.a;
    relation(area.a)["admin_level"="4"]["name"="{state}"];
    out body;
    >;
    out skel qt;
    """

    response = requests.post(OVERPASS_URL, data={"data": query})

    if response.status_code != 200:
        print(f"❌ Failed: {state} — HTTP {response.status_code}")
        continue

    osm_path = f"states_geojson/{state.replace(' ', '_')}.osm.json"
    geojson_path = f"states_geojson/{state.replace(' ', '_')}.geojson"

    # Save raw OSM JSON
    with open(osm_path, "w") as f:
        json.dump(response.json(), f, indent=2)

    # Convert to GeoJSON
    with open(osm_path) as f:
        osm_data = json.load(f)

    geojson = json2geojson(osm_data)

    with open(geojson_path, "w") as f:
        json.dump(geojson, f, indent=2)

    print(f"✅ Saved: {geojson_path}")
    os.remove(osm_path)

print("🎉 Done downloading all states.")
