"""Genera dashboard.html con las 5 figuras del análisis, una debajo de otra."""
from importlib import import_module

viz = import_module("02_visualizaciones")


def main():
    df = viz.cargar()
    fig1 = viz.fig1_top10(df)
    fig2, _ = viz.fig2_correlacion(df)
    fig3 = viz.fig3_scatter(df)
    fig4, _ = viz.fig4_barras_region(df)
    fig5 = viz.fig5_mapa(df)

    partes = []
    for fig in [fig1, fig2, fig3, fig4, fig5]:
        partes.append(fig.to_html(full_html=False, include_plotlyjs="cdn"))

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>World Happiness Report 2016 — Dashboard</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, Arial, sans-serif; max-width: 980px; margin: 32px auto; padding: 0 16px; color: #1a1a1a; }}
  h1 {{ font-size: 1.6rem; }}
  .fig {{ margin-bottom: 40px; }}
</style>
</head>
<body>
<h1>World Happiness Report 2016 — Dashboard</h1>
<p>Análisis de 157 países: qué componentes se asocian más con el Happiness Score. Código y datos en el repositorio.</p>
{"".join(f'<div class="fig">{p}</div>' for p in partes)}
</body>
</html>
"""
    with open("docs/dashboard.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Guardado docs/dashboard.html")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, "src")
    main()
