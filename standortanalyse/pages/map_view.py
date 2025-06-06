
import streamlit as st
import folium
from streamlit_folium import folium_static
import ee
import geemap.foliumap as geemap

def show_map():
    st.subheader("🌍 Übersichtskarte – Kriterienvisualisierung")

    try:
        ee.Initialize()
    except:
        ee.Authenticate()
        ee.Initialize()

    region = ee.Geometry.Rectangle([8.4, 49.9, 8.9, 50.3])
    impervious = ee.Image("COPERNICUS/GLO_30/IMPERVIOUSNESS/2019").select("impervious").clip(region)
    elevation = ee.Image("USGS/SRTMGL1_003").clip(region)
    slope = ee.Terrain.slope(elevation)
    substations = ee.FeatureCollection([
        ee.Feature(ee.Geometry.Point([8.566, 50.054]), {"name": "Kelsterbach"}),
        ee.Feature(ee.Geometry.Point([8.603, 50.070]), {"name": "Frankfurt SW"}),
        ee.Feature(ee.Geometry.Point([8.987, 50.081]), {"name": "Großkrotzenburg"})
    ])
    distance = substations.distance(10000).clip(region)

    imperv_norm = impervious.divide(100).subtract(1).abs()
    slope_norm = slope.divide(30).subtract(1).abs()
    dist_norm = distance.divide(10000).subtract(1).abs()

    # Gewichtung
    score = dist_norm.multiply(0.5).add(imperv_norm.multiply(0.3)).add(slope_norm.multiply(0.2))
    score_vis = {'min': 0, 'max': 1, 'palette': ['red', 'yellow', 'green']}

    m = geemap.Map(center=[50.1, 8.65], zoom=10)
    m.addLayer(score, score_vis, "Eignungsindex")
    m.addLayer(substations, {}, "Umspannwerke")
    m.addLayerControl()

    folium_static(m, width=1100, height=600)
