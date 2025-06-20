def show_ranking():
    st.set_page_config(page_title="Flächen-Ranking", layout="wide")
    st.title("📊 Flächen-Ranking")
    st.markdown("Hier sehen Sie eine Beispiel-Rangliste von potenziellen Gewerbeflächen:")

    # Beispielhafte Bewertungsdaten
    df = pd.DataFrame({
        "Fläche": ["Kelsterbach", "Frankfurt Süd", "Großkrotzenburg"],
        "Eignung (Score)": [0.91, 0.83, 0.78],
        "Distanz zum Umspannwerk (km)": [2.1, 5.4, 3.3],
        "Steigung (%)": [1.5, 4.2, 3.0],
        "Höhenlage (m)": [98, 132, 115]
    })

    df_sorted = df.sort_values("Eignung (Score)", ascending=False).reset_index(drop=True)

    st.dataframe(df_sorted, use_container_width=True)
