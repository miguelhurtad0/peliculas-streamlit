import streamlit as st
import requests
import pandas as pd
import re

st.set_page_config(page_title="Películas", layout="wide")

# Estilos
st.markdown("""
<style>
.card {
    background-color: #1c1c1c;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 20px;
    color: white;
    transition: transform 0.2s ease;
}
.card:hover {
    transform: scale(1.03);
}
.titulo {
    font-size: 18px;
    font-weight: bold;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

st.title("🎬 Catálogo de Películas y Series")

# Busqueda
st.sidebar.header("Filtros")
nombre = st.sidebar.text_input("Buscar")
genero = st.sidebar.selectbox("Género", ["Todos", "Drama", "Comedy", "Action", "Romance", "Adventure", "Animation"])
buscar = st.sidebar.button("Buscar")


def limpiar_html(texto):
    return re.sub('<.*?>', '', texto) if texto else "Sin descripción"

# api
def obtener_datos(nombre):
    url = f"https://api.tvmaze.com/search/shows?q={nombre}"
    try:
        return requests.get(url).json()
    except:
        return []

# resultado
if nombre:
    data = obtener_datos(nombre)

    if data:
        tab_resultados, tab_estadisticas = st.tabs(["🔍 Resultados", "📊 Estadísticas"])

        with tab_resultados:
            cols = st.columns(3)
            idx_v = 0

            for item in data:
                show = item["show"]

                if genero != "Todos" and genero not in show.get("genres", []):
                    continue

                with cols[idx_v % 3]:
                    

                    if show.get("image"):
                        st.image(show["image"]["medium"])
                        
                     
                        

                    st.markdown(f"<div class='titulo'>{show['name']}</div>", unsafe_allow_html=True)

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        c1, c2 = st.columns([1,2])
                        with c1:
                            st.image("icons/calendar.png", width=16)
                        with c2:
                            f = show.get('premiered')
                            st.write(f[:4] if f else "N/A")

                    with col2:
                        c1, c2 = st.columns([1,2])
                        with c1:
                            st.image("icons/play.png", width=16)
                        with c2:
                            r = show.get('rating', {}).get('average')
                            st.write(r if r else "None")

                    with col3:
                        c1, c2 = st.columns([1,2])
                        with c1:
                            st.image("icons/flm.png", width=16)
                        with c2:
                            g = show.get('genres')
                            st.write(", ".join(g) if g else "N/A")

                    
                    resumen = show.get("summary")
                    clean = limpiar_html(resumen)
                    st.write(clean[:130] + "...")

                    st.markdown("</div>", unsafe_allow_html=True)

                idx_v += 1

        with tab_estadisticas:
            st.header("📊 Estadísticas de la búsqueda")

            df = pd.DataFrame([
                {
                    "Nombre": x['show']['name'],
                    "Popularidad": x['show'].get('weight', 0),
                    "Rating": x['show'].get('rating', {}).get('average') or 0,
                    "Duración": x['show'].get('averageRuntime', 0),
                    "Estado": x['show'].get('status', 'N/A')
                } for x in data
            ])

            
            st.subheader("🔥 Top 10 más populares")
            top = df.sort_values("Popularidad", ascending=False).head(10)
            st.bar_chart(top.set_index("Nombre")["Popularidad"])

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("⭐ Ratings")
                df_r = df[df['Rating'] > 0]
                if not df_r.empty:
                    st.bar_chart(df_r.set_index("Nombre")["Rating"])

            with col2:
                st.subheader("⏱️ Duración")
                st.line_chart(df.set_index("Nombre")["Duración"])

            st.subheader("🎬 Estado de Producción")
            estado_counts = df['Estado'].value_counts()
            st.write(estado_counts)

            st.subheader("📌 Resumen general")
            colA, colB, colC = st.columns(3)

            with colA:
                st.metric("Promedio Rating", round(df["Rating"].mean(), 2))

            with colB:
                st.metric("Duración Promedio", int(df["Duración"].mean()))

            with colC:
                st.metric("Total Resultados", len(df))

            st.subheader("📋 Datos completos")
            st.dataframe(df, use_container_width=True)

    else:
        st.error("No se encontraron resultados")
        
        
        
        
        
 #Miguel Baldelomar
 #Junior flores
 #Anthony Obregon