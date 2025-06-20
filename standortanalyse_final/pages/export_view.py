import streamlit as st
import pandas as pd
import geopandas as gpd

def show_export():
    st.subheader("📤 Export GeoJSON / CSV")

    # Beispiel: Dummy-Daten
    data = {
        "Name": ["Fläche A", "Fläche B"],
        "Eignung": [92, 85],
        "Koordinaten": ["50.1, 8.6", "50.0, 8.5"]
    }
    df = pd.DataFrame(data)

    st.dataframe(df)

    # CSV Export
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📄 CSV herunterladen", csv, "gewerbeflaechen.csv", "text/csv")

    # GeoJSON Export – nur wenn Geodaten vorhanden
    # gdf = gpd.GeoDataFrame(df, geometry=...)  # mit Geometrie-Spalte
    # geojson = gdf.to_json()
    # st.download_button("🌍 GeoJSON herunterladen", geojson, "gewerbeflaechen.geojson", "application/geo+json")
