# Ingresantes UNA Puno 2024-I

Dashboard narrativo de los 1.890 ingresantes a la Universidad Nacional del
Altiplano en el proceso 2024-I. Trabajo del curso de Visualización de Datos,
hecho en Streamlit.

**Dashboard:** [URL Streamlit Cloud]
**Dataset original:** [URL portal de transparencia UNAP]
**Shapefile:** INEI 2023, adaptado por geogpsperu

## La historia, en 3 secciones

Cada sección arranca con una pregunta y la responde con un gráfico.

**01 · ¿De dónde vienen?** La UNA Puno es casi exclusivamente puntana (94.8%),
pero al mirar las 13 provincias, la capital aporta solo el 30%; el 51% restante
viene de las otras 11. No es una universidad de la ciudad, es de la región.
Los 98 ingresantes de fuera de Puno se analizan aparte: no tienen perfil propio,
son goteo regional.

**02 · ¿Cómo se reparten?** En el agregado 55% masculino / 45% femenino, casi
paritario. Por carrera el rango es de 96 puntos: Educación Inicial 100%
femenina, Ing. Mecánica Eléctrica 4% femenina. La segregación vocacional es
total.

**03 · ¿Qué explica las brechas?** El % de colegios privados por provincia
correlaciona con el puntaje mediano, pero con excepciones fuertes (Yunguyo,
Moho). El origen escolar importa, no determina.

## Dataset

- 1.890 registros después de limpieza
- 25 columnas: demográficas, geográficas, académicas
- Proceso 2024-I (corte transversal, sin serie temporal)
- Licencia: Open Data Commons Attribution
- Ley N° 27806 (Transparencia y Acceso a la Información Pública)

Variables usadas: `SEXO`, `DEPARTAMENTO_PROCEDENCIA`, `PROVINCIA_PROCEDENCIA`,
`ESCUELA_PROFESIONAL`, `TIPO_COLEGIO`, `PUNTAJE`.

## Lo que nos encontramos limpiando

**El UBIGEO no sigue el estándar INEI.** El dataset usa el código `20` para
Puno (debería ser `21`) y las provincias están corridas desde la 2105: "Moho"
aparece con código de "San Román", por ejemplo. Resolvimos cruzando con el
shapefile por **nombre normalizado** (mayúsculas, sin tildes), no por código.
Verificamos que las 13 provincias de Puno coinciden.

**Un caso de doble ingreso.** El mismo DNI (z4843339) aparece dos veces porque
postuló por CEPREUNA (2306.01) y por Examen General (2572.05). Nos quedamos con
el puntaje más alto para no inflar el conteo territorial.

**TIPO_COLEGIO venía en 5 variantes.** "PÚBLICA DE GESTIÓN DIRECTA",
"PUBLICA DE GESTION DIRECTA", "PRIVADA", "PRIVADO", "PÚBLICA DE GESTIÓN
PRIVADA". Lo dejamos en 3 categorías. La tercera es un caso real (colegios
públicos administrados por privados, tipo Fe y Alegría), así que la mantuvimos
aparte.

**Un año de egreso imposible.** Un registro dice que egresó en 2029 pero el
examen es 2024. Queda en el dataset pero lo anotamos como limitación y lo
excluimos del análisis de gap educativo.

**Las 3 escalas de puntaje son comparables.** Ratio 1.20x entre el rango mayor
y el menor (General, CEPREUNA, Extraordinario). Se pueden usar juntos sin
filtrar.

**Solo hay un periodo.** El dataset cubre 2024-I. No podemos analizar
tendencias.

## Por qué no hicimos una sección sobre "externos"

Hay 98 ingresantes (5.2%) de fuera de Puno: Cusco 39, Arequipa 20, Lima 14,
Tacna 11, y 8 departamentos más con 1-3 casos. Analizamos si tenían perfil
propio y no: puntaje medio casi idéntico (1908 vs 1913), gap educativo también
(3.8 vs 3.4 años), y se reparten en 34 carreras sin concentración. Quedan como
gráfico secundario en la sección 01 pero no alcanzan para un análisis propio.

## Paleta

| Color | Hex | Uso |
|---|---|---|
| Azul petróleo | `#1C4E5C` | Territorio, mapas |
| Naranja quemado | `#D97B29` | Hallazgos (Yunguyo, Moho) |
| Gris arena | `#D9D2C5` | Fondo, neutro |
| Verde andino | `#6A8A3A` | Categorías secundarias |

El naranja solo aparece en los puntos que queremos destacar. Si lo usamos en
todos lados, deja de destacar.

## Cómo correrlo

```bash
git clone https://github.com/[usuario]/unapuno-dashboard.git
cd unapuno-dashboard
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py