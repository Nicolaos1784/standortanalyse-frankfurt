import streamlit as st
import requests
import geopandas as gpd
from shapely.geometry import Point, LineString
import folium
from streamlit_folium import folium_static

def fetch_substations(bbox):
    """
    Holt Umspannwerke (power=substation) aus OSM.
    """
    query = f"""
    [out:json][timeout:25];
    (
      node["power"="substation"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      way["power"="substation"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      relation["power"="substation"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    );
    out center;
    """
    url = "http://overpass-api.de/api/interpreter"
    r = requests.get(url, params={'data': query})
    if r.status_code != 200:
        st.error("Fehler beim Laden der Umspannwerke.")
        return gpd.GeoDataFrame()

    data = r.json()
    points = []
    for el in data["elements"]:
        if "lat" in el and "lon" in el:
            point = Point(el["lon"], el["lat"])
        elif "center" in el:
            point = Point(el["center"]["lon"], el["center"]["lat"])
        else:
            continue
        points.append({
            "id": el["id"],
            "geometry": point,
            "tags": el.get("tags", {})
        })

    return gpd.GeoDataFrame(points, geometry="geometry", crs="EPSG:4326")

def fetch_power_lines(bbox):
    """
    Holt Stromleitungen (power=line) aus OSM.
    """
    query = f"""
    [out:json][timeout:25];
    way["power"="line"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    (._;>;);
    out body;
    """
    url = "http://overpass-api.de/api/interpreter"
    r = requests.get(url, params={'data': query})
    if r.status_code != 200:
        st.error("Fehler beim Laden der Stromleitungen.")
        return gpd.GeoDataFrame()

    data = r.json()
    nodes = {el["id"]: (el["lon"], el["lat"]) for el in data["elements"] if el["type"] == "node"}
    lines = []
    for el in data["elements"]:
        if el["type"] == "way":
            coords = [nodes[nid] for nid in el["nodes"] if nid in nodes]
            if len(coords) >= 2:
                lines.append({
                    "id": el["id"],
                    "geometry": LineString(coords),
                    "tags": el.get("tags", {})
                })

    return gpd.GeoDataFrame(lines, geometry="geometry", crs="EPSG:4326")

def show_map():
    st.subheader("🗺️ Karte: Umspannwerke & Stromleitungen")

    bbox = (49.9, 8.4, 50.3, 8.9)  # Großraum Frankfurt

    gdf_substations = fetch_substations(bbox)
    gdf_lines = fetch_power_lines(bbox)

    m = folium.Map(location=[50.1, 8.6], zoom_start=10)

    # Umspannwerke
    for _, row in gdf_substations.iterrows():
        name = row.get("tags", {}).get("name", "Umspannwerk")
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=name,
            icon=folium.Icon(color="red", icon="bolt")
        ).add_to(m)

    # Stromleitungen
    for _, row in gdf_lines.iterrows():
        folium.PolyLine(
            locations=[(pt[1], pt[0]) for pt in row.geometry.coords],
            color="blue",
            weight=2,
            opacity=0.6,
            tooltip="Stromleitung"
        ).add_to(m)

    folium_static(m)
