
import streamlit as st
import geemap
import ee

def show_export():
    st.subheader("📤 Exportieren der besten Flächen")
    try:
        ee.Initialize()
    except:
        ee.Authenticate()
        ee.Initialize()

    region = ee.Geometry.Rectangle([8.4, 49.9, 8.9, 50.3])
    threshold = st.slider("Minimale Eignung", 0.5, 1.0, 0.8, 0.01)

    score = ee.Image("COPERNICUS/GLO_30/IMPERVIOUSNESS/2019").select("impervious").clip(region).divide(100).subtract(1).abs()
    mask = score.gt(threshold)

    vectors = score.updateMask(mask).reduceToVectors(
        geometry=region,
        scale=100,
        geometryType="polygon",
        bestEffort=True,
        maxPixels=1e8,
        tileScale=4
    )

    filename = "exportierte_flaechen.geojson"
    geemap.ee_export_vector(vectors, filename=filename)
    st.success(f"✅ Export abgeschlossen: {filename}")
    with open(filename, "rb") as f:
        st.download_button("📥 Jetzt herunterladen", f, file_name=filename)
