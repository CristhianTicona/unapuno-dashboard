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

## Por qué elegimos estos colores

Usamos 5 colores fijos y un par de degradados para los mapas. La idea era que los colores ayuden a entender el gráfico, no que sean solo decorativos:

| Color | Hex | Dónde se usa | Por qué |
| :--- | :--- | :--- | :--- |
| Azul petróleo | `#1C4E5C` | Mapas y gráfico de externos. | Es un color serio, que va bien con la temática del lago Titicaca. |
| Naranja quemado | `#D97B29` | Porción de CEPREUNA y casos especiales (Moho, Yunguyo). | Resalta fuerte. Lo usamos solo para llamar la atención sobre lo importante. |
| Verde andino | `#6A8A3A` | Porción de Extraordinario en la dona. | Sirve para diferenciar la tercera categoría sin tapar al naranja. |
| Azul acero | `#2E5C8A` | Barras de hombres y tarjeta de Ingeniería. | Diferencia la categoría masculina de forma clara. |
| Magenta apagado | `#C6517C` | Barras de mujeres y tarjeta de Educación Inicial. | Diferencia la categoría femenina sin usar rosa claro, que se lee mal en pantalla. |

**La regla principal:** el naranja solo aparece en los puntos que queremos que el profesor mire primero (como los casos raros de la Sección 03). Si lo usáramos en todos lados, ya no resaltaría nada.

## ¿Cómo está armado el código?

- `app.py`: es el archivo principal que arma la página en Streamlit.
- `src/`: acá están los archivos auxiliares (el que carga los datos, el que dibuja los gráficos y el que tiene los estilos).
- `data/`: los archivos `.parquet`, `.csv` y `.geojson` con los datos ya limpios.
