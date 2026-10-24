# Ingresantes UNA Puno 2024-I

Análisis y visualización de los ingresantes a la Universidad Nacional del Altiplano (UNAP) en el proceso de admisión 2024-I.

- **Dashboard:** [https://unapuno-dashboard.streamlit.app/](https://unapuno-dashboard.streamlit.app/)
- **Repositorio:** [https://github.com/CristhianTicona/unapuno-dashboard.git](https://github.com/CristhianTicona/unapuno-dashboard.git)

## Información académica

- **Curso:** Visualización de Datos
- **Programa:** Maestría en Ciencia de Datos
- **Universidad:** Universidad Nacional del Altiplano - Puno

**Integrantes:**
- Cristhian Eddy Ticona Cutipa
- Russell Eulogio Carbajal Vilca
- Jean Carlos Carrasco Cutisaca

## El análisis

El dashboard se divide en tres partes, cada una respondiendo una pregunta específica sobre los 1.890 ingresantes:

1. **¿De dónde vienen?** La mayoría (94.8%) es de Puno, pero al mirar las 13 provincias, la capital aporta solo el 30%. El 51% restante viene de las otras 11 provincias, demostrando que no es una universidad centralizada en la ciudad, sino regional. También incluimos un gráfico de los 98 ingresantes que vienen de fuera de Puno para ver su comportamiento.
2. **¿Cómo se reparten?** En general, la proporción es casi paritaria (55% hombres, 45% mujeres). Sin embargo, al mirar por carrera, la brecha es enorme: Educación Inicial tiene 100% de mujeres y en Ingeniería Mecánica Eléctrica solo hay 4%.
3. **¿Qué explica las brechas?** Al cruzar el porcentaje de colegios privados de cada provincia con el puntaje mediano de ingreso, vemos que no hay una regla fija. Provincias como Yunguyo (casi sin colegios privados) tienen los mejores puntajes, mientras que Moho tiene un buen puntaje pero una muestra muy pequeña (23 ingresantes). El origen escolar importa, pero no determina el resultado.

## Fuentes de datos

- **Dataset:** [Plataforma Nacional de Datos Abiertos - Lista de Ingresantes UNAP 2024-I](https://www.datosabiertos.gob.pe/dataset/lista-de-ingresantes-durante-el-a%C3%B1o-2024-i-la-universidad-nacional-del-altiplano-una-puno)
- **Licencia:** Open Data Commons Attribution
- **Shapefile:** [Límite provincial político - geogpsperu](https://www.geogpsperu.com/2019/08/limite-provincial-politico-shapefile.html) (basado en INEI 2023). *Nota: el shapefile original fue recortado y convertido a GeoJSON para el uso en este proyecto.*
- **Marco legal:** Ley N° 27806 (Transparencia y Acceso a la Información Pública).

## Limpieza y problemas encontrados

Tuvimos que hacer varios ajustes al dataset original antes de poder graficarlo:

- **El UBIGEO estaba mal.** El dataset no usa el estándar INEI. Puno aparecía con el código `20` en lugar de `21`, y las provincias estaban desalineadas desde el código 2105 (por ejemplo, "Moho" aparecía con el código de "San Román"). Lo solucionamos cruzando el dataset con el shapefile usando los nombres normalizados (sin tildes, en mayúsculas) en lugar de los códigos.
- **1 caso de doble ingreso.** El mismo DNI aparecía dos veces porque la persona ingresó por CEPREUNA y por Examen General. Nos quedamos con el registro de mayor puntaje para no duplicar los conteos territoriales.
- **`TIPO_COLEGIO` tenía 5 variantes.** Había errores de tipeo y categorías mezcladas. Lo simplificamos en 3: Pública, Privada, y Pública de Gestión Privada (un caso real de colegios administrados por privados).
- **Un año de egreso imposible.** Un registro decía que el alumno egresó en 2029, siendo que el examen fue en 2024. Lo dejamos en el dataset pero lo excluimos de los análisis de tiempo y lo anotamos como limitación.
- **Escalas de puntaje.** Verificamos que los puntajes de General, CEPREUNA y Extraordinario son comparables (la diferencia entre sus rangos es mínima), así que pudimos usar todo el dataset junto.

### Nota sobre los ingresantes externos

Hay 98 ingresantes (5.2%) que vienen de otros departamentos (Cusco, Arequipa, Lima, Tacna, etc.). Analizamos sus datos y no tienen un perfil distinto: su puntaje promedio es casi igual al de los puneños (1908 vs 1913) y se reparten entre 34 carreras. Por eso no les dedicamos una sección completa, sino que quedan como un gráfico informativo dentro de la primera sección.

## Paleta de colores

Para mantener la consistencia visual y comunicativa, definimos una paleta basada en 5 colores sólidos y 2 escalas de degradado:

| Color | Hex | Uso en el dashboard | Criterio |
| :--- | :--- | :--- | :--- |
| Azul petróleo | `#1C4E5C` | Mapas, gráfico de barras de externos, porción GENERAL de la dona. | Seriedad institucional; evoca al Lago Titicaca. |
| Naranja quemado | `#D97B29` | Porción CEPREUNA de la dona, resaltado de casos atípicos (Moho, Yunguyo), y % privado alto. | Contraste fuerte para atraer la vista al dato clave o al hallazgo. |
| Verde andino | `#6A8A3A` | Porción EXTRAORDINARIO de la dona. | Diferenciar la tercera categoría sin competir con el naranja. |
| Azul acero | `#2E5C8A` | Barras de hombres (Sección 02) y tarjeta de "Ing. Mecánica Eléctrica". | Diferenciar la categoría masculina de forma limpia. |
| Magenta apagado | `#C6517C` | Barras de mujeres (Sección 02) y tarjeta de "Ed. Inicial". | Diferenciar la categoría femenina sin usar rosa pastel (poco legible). |

**Escalas continuas:**
Para los mapas y el gráfico de puntajes usamos gradientes que van desde tonos grises/azules claros (para los valores más bajos) hasta el azul petróleo o el naranja quemado (para los valores más altos). Esto permite leer rápidamente dónde están las concentraciones y las brechas sin necesidad de una leyenda compleja.

**La regla principal:** El naranja se reserva exclusivamente para destacar hallazgos (como Yunguyo y Moho en la Sección 03). Si lo usáramos en todos los gráficos, dejaría de llamar la atención.

## Estructura del proyecto

- `app.py`: código principal de Streamlit.
- `src/`: módulos auxiliares (carga de datos, gráficos y estilos).
- `data/`: archivos `.parquet`, `.csv` y `.geojson` con los datos ya procesados.
