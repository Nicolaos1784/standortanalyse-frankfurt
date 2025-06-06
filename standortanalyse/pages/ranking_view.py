
import streamlit as st
import pandas as pd

def show_ranking():
    st.subheader("📊 Ranking der besten Flächen")
    st.info("🔧 Dieser Bereich wird im nächsten Schritt mit echten Daten gefüllt.")
    # Beispielhafte Tabelle
    data = {
        "Fläche ID": [1, 2, 3],
        "Eignung (0–1)": [0.91, 0.88, 0.85],
        "Größe (m²)": [18000, 22000, 14500],
        "Entfernung Umspannwerk (m)": [320, 1100, 950]
    }
    df = pd.DataFrame(data)
    st.dataframe(df)
