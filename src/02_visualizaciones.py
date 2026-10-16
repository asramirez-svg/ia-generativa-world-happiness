"""
Cinco visualizaciones Plotly sobre World Happiness Report 2016, siguiendo los
prompts de referencia del proyecto guiado del curso (IBM Generative AI for
Data Analytics), pero con el código escrito y verificado directamente.

Decisiones documentadas (ver docs/hallazgos.md para el detalle):
- "Top 10" = los 10 países con mejor Happiness Rank (rank 1 = más feliz).
- La matriz de correlación excluye Happiness Rank y los intervalos de
  confianza (no son "aportes" al score, son metadatos del ranking/encuesta).
- El pie chart de Happiness Score por región sería engañoso (suma los scores,
  así que las regiones con más países se ven más "felices" solo por tener más
  países) -> se reemplaza por barras del promedio por región, con una nota
  sobre esta decisión en el dashboard.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

CLEAN_PATH = "data/2016_clean.csv"
IMG_DIR = "img"


def cargar():
    return pd.read_csv(CLEAN_PATH)


def fig1_top10(df: pd.DataFrame):
    top10 = df.nsmallest(10, "Happiness Rank")
    fig = px.bar(
        top10, x="Country", y=["Economy (GDP per Capita)", "Health (Life Expectancy)"],
        barmode="group", title="Top 10 países más felices: PBI per cápita y esperanza de vida saludable",
        labels={"value": "Aporte al Happiness Score", "variable": "Componente"},
    )
    return fig


def fig2_correlacion(df: pd.DataFrame):
    cols = ["Economy (GDP per Capita)", "Family", "Health (Life Expectancy)",
            "Freedom", "Trust (Government Corruption)", "Generosity", "Happiness Score"]
    corr = df[cols].corr()
    fig = px.imshow(
        corr, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
        title="Correlación entre los componentes del Happiness Score",
    )
    fig.update_layout(width=800, height=600)
    return fig, corr


def fig3_scatter(df: pd.DataFrame):
    fig = px.scatter(
        df, x="Economy (GDP per Capita)", y="Happiness Score", color="Region",
        hover_name="Country", title="PBI per cápita vs. Happiness Score, por región",
    )
    return fig


def fig4_barras_region(df: pd.DataFrame):
    # Barras del promedio por región en vez de pie chart de la suma: un pie
    # de "Happiness Score" por región suma los scores, así que una región con
    # muchos países (ej. Sub-Saharan Africa) se ve más grande sin que eso
    # signifique que sea más feliz. El promedio por región sí es comparable.
    promedio = df.groupby("Region", as_index=False)["Happiness Score"].mean()
    promedio = promedio.sort_values("Happiness Score", ascending=True)
    fig = px.bar(
        promedio, x="Happiness Score", y="Region", orientation="h",
        title="Happiness Score promedio por región (no es un pie: ver nota en README)",
    )
    return fig, promedio


def fig5_mapa(df: pd.DataFrame):
    fig = px.choropleth(
        df, locations="Country", locationmode="country names",
        color="Economy (GDP per Capita)", hover_name="Country",
        hover_data={"Health (Life Expectancy)": True},
        color_continuous_scale="Viridis",
        title="PBI per cápita por país (tooltip: esperanza de vida saludable)",
    )
    return fig


def main():
    df = cargar()
    fig1 = fig1_top10(df)
    fig2, corr = fig2_correlacion(df)
    fig3 = fig3_scatter(df)
    fig4, promedio_region = fig4_barras_region(df)
    fig5 = fig5_mapa(df)

    for name, fig in [("fig1_top10", fig1), ("fig2_correlacion", fig2),
                       ("fig3_scatter", fig3), ("fig4_region", fig4), ("fig5_mapa", fig5)]:
        try:
            fig.write_image(f"{IMG_DIR}/{name}.png", scale=2)
            print(f"Guardado {IMG_DIR}/{name}.png")
        except Exception as e:
            # El mapa (fig5) necesita descargar el contorno del mundo desde
            # cdn.plot.ly para exportarse como PNG estático; si no hay acceso
            # a internet en este paso, se omite el PNG y queda solo en el
            # dashboard.html interactivo (que sí lo carga al abrirse).
            print(f"No se pudo exportar {name}.png como imagen estática: {e}")

    print("\nMatriz de correlación:")
    print(corr.round(2))
    print("\nHappiness Score promedio por región:")
    print(promedio_region.round(3).to_string(index=False))

    return fig1, fig2, fig3, fig4, fig5


if __name__ == "__main__":
    main()
