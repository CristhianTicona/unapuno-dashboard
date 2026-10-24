# Ingresantes UNA Puno 2024-I

Este es el trabajo final del curso de Visualización de Datos. Armamos un dashboard interactivo con los datos de los 1.890 estudiantes que ingresaron a la Universidad Nacional del Altiplano (UNAP) en el proceso 2024-I.

- **Dashboard:** [https://unapuno-dashboard.streamlit.app/](https://unapuno-dashboard.streamlit.app/)
- **Repositorio:** [https://github.com/CristhianTicona/unapuno-dashboard.git](https://github.com/CristhianTicona/unapuno-dashboard.git)

## Datos del grupo

- **Curso:** Visualización de Datos
- **Maestría:** Ciencia de Datos
- **Universidad:** Universidad Nacional del Altiplano - Puno

**Integrantes:**
- Cristhian Eddy Ticona Cutipa
- Russell Eulogio Carbajal Vilca
- Jean Carlos Carrasco Cutisaca

## ¿Qué muestra el dashboard?

Dividimos el trabajo en tres partes, cada una con una pregunta y su gráfico:

1. **¿De dónde vienen?** Casi todos los ingresantes son de Puno (94.8%). Pero cuando miramos las 13 provincias, la capital (Puno) solo aporta el 30%. El otro 51% viene de las demás provincias. O sea, la universidad no es solo de la ciudad, es de toda la región. Además, agregamos un gráfico aparte para ver a los 98 ingresantes que vienen de otros departamentos del Perú.
2. **¿Cómo se reparten?** En total, la proporción es casi igual: 55% hombres y 45% mujeres. Pero si miramos carrera por carrera, la diferencia es enorme. Educación Inicial tiene 100% de mujeres, mientras que Ingeniería Mecánica Eléctrica tiene solo 4%.
3. **¿Qué explica las brechas?** Cruzamos el porcentaje de colegios privados de cada provincia con el puntaje mediano de sus ingresantes. Descubrimos que no hay una regla fija. Por ejemplo, Yunguyo casi no tiene colegios privados pero tiene los mejores puntajes. El tipo de colegio importa, pero no lo define todo.

## ¿De dónde sacamos los datos?

- **Datos de los ingresantes:** [Plataforma Nacional de Datos Abiertos](https://www.datosabiertos.gob.pe/dataset/lista-de-ingresantes-durante-el-a%C3%B1o-2024-i-la-universidad-nacional-del-altiplano-una-puno)
- **Licencia del dataset:** Open Data Commons Attribution.
- **Mapa (shapefile):** [Límite provincial de geogpsperu](https://www.geogpsperu.com/2019/08/limite-provincial-politico-shapefile.html) (basado en INEI 2023). Tuvimos que recortar el mapa original y pasarlo a GeoJSON para que funcione bien en el dashboard.
- **Ley de Transparencia:** Ley N° 27806.

## Problemas que encontramos al limpiar los datos

El archivo original tenía varios errores que tuvimos que arreglar antes de graficar:

- **Los códigos de ubicación (UBIGEO) estaban mal.** Puno aparecía con el código `20` en vez del `21`, y las provincias estaban corridas (por ejemplo, "Moho" tenía el código de "San Román"). Lo solucionamos cruzando los datos con el mapa usando los **nombres** de las provincias, no los códigos.
- **Había un caso de doble ingreso.** La misma persona (mismo DNI) aparecía dos veces porque postuló por CEPREUNA y también por Examen General. Nos quedamos con el puntaje más alto para no contarla dos veces en el mapa.
- **El tipo de colegio estaba mal escrito.** Había 5 formas distintas de escribir "pública" o "privada". Lo resumimos en 3 categorías para que se entienda mejor.
- **Un año de egreso imposible.** Un registro decía que el alumno salió del colegio en el año 2029 (siendo que el examen fue en 2024). Lo dejamos ahí pero lo sacamos de los análisis de tiempo.
- **Los puntajes se podían comparar.** Revisamos que los puntajes de General, CEPREUNA y Extraordinario se midieran en la misma escala, así que pudimos usar todo junto sin problemas.

### ¿Por qué no hicimos una sección solo para los externos?

Hay 98 ingresantes (5.2%) que no son de Puno. Revisamos si tenían algo especial, pero no: su puntaje promedio es casi igual al de los puneños (1908 vs 1913) y se reparten en 34 carreras distintas. Como no eran un grupo con un perfil diferente, decidimos dejarlos como un gráfico secundario en la primera sección.

## Paleta de colores

Usamos una paleta fija para que el dashboard sea consistente. La idea es que un mismo color siempre signifique lo mismo, así el lector no tiene que adivinar qué está mirando.

| Color | Hex | Dónde se usa exactamente |
| :--- | :--- | :--- |
| Azul petróleo | `#1C4E5C` | - En los mapas (provincias y departamentos con más ingresantes).<br>- En las barras de ingresantes de otros departamentos.<br>- En la porción "GENERAL" del gráfico de dona.<br>- En las barras de los hombres (Sección 02). |
| Naranja quemado | `#D97B29` | - En la porción "CEPREUNA" del gráfico de dona.<br>- Para resaltar los casos atípicos de la Sección 03 (Moho, Yunguyo).<br>- En los porcentajes más altos de colegios privados. |
| Verde andino | `#6A8A3A` | - En la porción "EXTRAORDINARIO" del gráfico de dona. |
| Magenta apagado | `#C6517C` | - En las barras de las mujeres (Sección 02). |
| Azul acero | `#2E5C8A` | - En las barras de los hombres (Sección 02) y en la etiqueta de la carrera "Ing. Mecánica Eléctrica". |

**Regla de uso:** El naranja se usa únicamente para señalar cosas que queremos que el lector mire con atención (como los casos raros de Moho y Yunguyo). El resto de los colores se mantienen fijos para cada categoría, de modo que si en el mapa un departamento es oscuro, en el gráfico de barras ese mismo tono signifique lo mismo.

Para los mapas y el gráfico de la Sección 03, usamos un degradado (de gris claro a azul petróleo, o de azul claro a naranja) porque los valores son continuos. Esto ayuda a ver de un vistazo dónde están los puntajes más bajos y los más altos.

## ¿Cómo está armado el código?

- `app.py`: es el archivo principal que arma la página en Streamlit.
- `src/`: acá están los archivos auxiliares (el que carga los datos, el que dibuja los gráficos y el que tiene los estilos).
- `data/`: los archivos `.parquet`, `.csv` y `.geojson` con los datos ya limpios.
