
import streamlit as st
import folium
from streamlit_folium import folium_static
import ee
import geemap.foliumap as geemap
import json
from google.oauth2 import service_account

def show_map():
    st.subheader("🌍 Übersichtskarte – Kriterienvisualisierung")

    # Earth Engine Auth mit st.secrets (aus secrets.toml)
    service_account_info = st.secrets["earthengine"]
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(json.dumps(service_account_info)),
        scopes=["https://www.googleapis.com/auth/earthengine"]
    )
    ee.Initialize(credentials)

    # Analysegebiet definieren
    region = ee.Geometry.Rectangle([8.4, 49.9, 8.9, 50.3])
    elevation = ee.Image('USGS/SRTMGL1_003').clip(region)
    slope = ee.Terrain.slope(elevation)

    substations = ee.FeatureCollection([
        ee.Feature(ee.Geometry.Point([8.566, 50.054]), {"name": "Kelsterbach"}),
        ee.Feature(ee.Geometry.Point([8.603, 50.070]), {"name": "Frankfurt SW"}),
        ee.Feature(ee.Geometry.Point([8.987, 50.081]), {"name": "Großkrotzenburg"})
    ])
    distance = substations.distance(10000).clip(region)

    elev_norm = elevation.subtract(80).divide(220).multiply(-1).add(1).clamp(0, 1)
    slope_norm = slope.lte(30).multiply(ee.Image(1).subtract(slope.divide(30)))
    dist_norm = distance.lte(10000).multiply(ee.Image(1).subtract(distance.divide(10000)))

    score = dist_norm.multiply(0.5).add(elev_norm.multiply(0.3)).add(slope_norm.multiply(0.2))
    score_vis = {"min": 0, "max": 1, "palette": ["red", "yellow", "green"]}

    m = geemap.Map(center=[50.1, 8.65], zoom=10)
    m.addLayer(score, score_vis, "Eignungsindex")
    m.addLayer(substations, {}, "Umspannwerke")
    m.addLayerControl()

    folium_static(m, width=1100, height=600)
