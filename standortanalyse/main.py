
import streamlit as st
from pages.map_view import show_map
from pages.ranking_view import show_ranking
from pages.export_view import show_export

st.set_page_config(page_title="Gewerbeflächenanalyse Frankfurt", layout="wide")
st.title("📍 Standortanalyse Gewerbeflächen – Großraum Frankfurt")

menu = st.sidebar.radio("📂 Navigation", ["🌍 Karte", "📊 Ranking", "📤 Export"])

if menu == "🌍 Karte":
    show_map()
elif menu == "📊 Ranking":
    show_ranking()
elif menu == "📤 Export":
    show_export()
