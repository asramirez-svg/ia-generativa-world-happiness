# Hallazgos — World Happiness Report 2016

Escenario del proyecto guiado: una consultora de salud quiere saber qué
características económicas y regionales se asocian con un Happiness Score
más alto, en base al Happiness Report 2016 (157 países).

## Qué más se correlaciona con el Happiness Score

| Componente | Correlación con Happiness Score |
|---|---|
| Economy (GDP per Capita) | 0.79 |
| Health (Life Expectancy) | 0.77 |
| Family | 0.74 |
| Freedom | 0.57 |
| Trust (Government Corruption) | 0.40 |
| Generosity | 0.16 |

El PBI per cápita, la esperanza de vida saludable y el apoyo familiar son,
con bastante distancia, los tres componentes más asociados al score. La
generosidad es el que menos se asocia — un país puede ser generoso sin que
eso se traduzca en un Happiness Score más alto.

*Nota metodológica:* estos componentes son, por construcción del índice,
**aportes directos** al propio Happiness Score (el score es aproximadamente
la suma de sus componentes), así que la correlación alta no es un hallazgo
causal — es parcialmente mecánica. Por eso se excluyó `Happiness Rank` del
análisis de correlación (correlaciona ≈ −1 con el score casi por definición,
al ser su ordenamiento).

## Diferencias por región

| Región | Happiness Score promedio |
|---|---|
| Sub-Saharan Africa | 4.14 |
| Southern Asia | 4.56 |
| Southeastern Asia | 5.34 |
| Central and Eastern Europe | 5.37 |
| Middle East and Northern Africa | 5.39 |
| Eastern Asia | 5.62 |
| Latin America and Caribbean | 6.10 |
| Western Europe | 6.69 |
| North America | 7.25 |
| Australia and New Zealand | 7.32 |

La brecha entre la región con mayor y menor promedio es de **3.19 puntos**
(Australia/NZ vs. Sub-Saharan Africa) — mayor que la diferencia entre el país
#1 (Denmark, 7.53) y el país #20 del ranking general.

Importante: un **pie chart de `Happiness Score` por región suma los
scores**, así que una región con muchos países (ej. Sub-Saharan Africa, con
~38 países) se ve "grande" en el pie sin que eso signifique que sea más
feliz — mide cantidad de países, no bienestar. Por eso el dashboard usa
**barras del promedio por región** en vez del pie sugerido por el prompt
original del proyecto guiado.

## Top y bottom 5

- **Más felices:** Denmark (7.53), Switzerland (7.51), Iceland (7.50),
  Norway (7.50), Finland (7.41) — los 5 son de Europa Occidental.
- **Menos felices:** Burundi (2.91), Syria (3.07), Togo (3.30), Afghanistan
  (3.36), Benin (3.48).

Los 3 países con menor score (Burundi, Syria, Togo) tienen en común
inestabilidad política o conflicto activo en 2016 — el score cae más por
baja confianza/libertad que solo por PBI bajo.

## Perú

Perú está en el puesto 64 de 157, con score 5.74 — por encima del promedio
de su región (Latin America and Caribbean, 6.10 es el promedio, así que Perú
queda **debajo** del promedio regional).

## Limitación del dataset

El dataset **no tiene variables demográficas** (edad, género, etc.) — solo
país, región y los componentes del índice. El enunciado original del
proyecto pedía evaluar si las características "demográficas, regionales y/o
económicas" se asocian con el bienestar; con estos datos solo se puede
responder la parte regional y económica.
