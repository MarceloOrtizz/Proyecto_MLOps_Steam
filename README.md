<p align="center"><img src="images\henry.png"></p>

## <h1 align=center> Sistema de recomendaciones de Steam </h1>

¡Bienvenido al repositorio del sistema de recomendación de videojuegos de Steam!
Este proyecto comienza con el desafío de crear un sistema de recomendación de videojuegos desde cero que tenga aplicación en datos reales.

Se parte de datos que surgen de [3 archivos comprimidos](data/original), con diferentes formatos y distintas complicaciones para su lectura.

<p align="center"><img src="images\ETL.jpg" height=200></p>

En este proyecto comienzo con la información cruda, realizo el correspondiente [ETL](etl_eda) logrando organizar los datos limpios en [3 archivos ordenados](data/limpio/).

Partiendo de esos datos limpios procedo a filtrar y ordenar la información necesaria para responder específicamente a los endpoints solicitados:

<p align="center"><img src="images\filtrados.jpg" height=200></p>

# Funciones:
 <br>

+ def **PlayTimeGenre( *`genero` : str* )**:
    Debe devolver `año` con mas horas jugadas para dicho género.<br>

+ def **UserForGenre( *`genero` : str* )**:
    Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.<br>

+ def **UsersRecommend( *`año` : int* )**:
   Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales).<br>

+ def **UsersNotRecommend( *`año` : int* )**:
   Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos).<br>

+ def **sentiment_analysis( *`año` : int* )**:
    Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento. <br><br>

Estos endpoints son consumidos por la API usando [FastAPI](https://fastapi.tiangolo.com/) (es un marco web moderno para crear API RESTful en Python). Estas funciones consumen los [datos](etl_eda/ETL_consultas.ipynb) que ya fueron filtrados con la informacion necesaria para responder la consulta. <br>

# Estructura del Repositorio: <br>
/data: Contiene los datos utilizados en el proyecto. (originales, limpios y acotados para los endpoints).<br>
/etl_eda: Contiene los diferentes archivos jupyter notebook donde se realizan los ETL y EDA.<br>
main.py: contiene el codigo principal donde se usa el framework FastAPI para creal la API web.<br>
/models: Contiene el modelo de machine learning para la recomendación.<br>
/requierements.txt: el archivo donde se especifican las dependencias del proyecto.<br>

# Análisis Exploratorio de Datos (EDA)
Se llevó a cabo un análisis exploratorio ([EDA](etl_eda/EDA.ipynb)) para investigar relaciones, buscar outliers y descubrir patrones interesantes entre las variables que intervienen en el modelo. 

<p align="center"><img src="images\ml.jpg" height=200></p>

# Modelo de Aprendizaje Automático
Se implementó un sistema de recomendación ítem-ítem  (usando *similitud del coseno*). La API permite recibir un id de un juego y devuelve una lista con 5 juegos recomendados de caracteristicas similares.









