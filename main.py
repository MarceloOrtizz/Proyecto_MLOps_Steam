import pandas as pd
from fastapi import FastAPI
import nltk
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

app = FastAPI()

#consulta_2 = pd.read_csv('./data/consultas/UserForGenre.csv.gz',compression='gzip')
nltk.download('stopwords')

@app.get('/')
def home():
    return {"API consultas Steam"}


@app.get('/PlayTimeGenre/{genero}')
def PlayTimeGenre(genero: str):  
  '''Debe devolver año con mas horas jugadas para dicho género.'''
  try:
    consulta_1 = pd.read_csv('./data/consultas/PlayTimeGenre.csv.gz',compression='gzip')
    year_max =consulta_1[consulta_1['genres'].str.contains(genero)][['year','playtime_forever']].groupby('year').sum().idxmax().iloc[0]
    return {f"Año de lanzamiento con más horas jugadas para Género {genero}" : {str(year_max)}}

  except Exception as e :
    return {f'ERROR: {e}'}
  
@app.get('/UserForGenre/{genero}')
def UserForGenre(genero: str):
  '''Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas desde el año de lanzamiento'''
  global consulta_2
  try:
    consulta_2 = pd.read_csv('./data/consultas/UserForGenre.csv.gz',compression='gzip')
    usuario=consulta_2[['user_id','year','playtime_forever']][consulta_2['genres'].str.contains(genero)].groupby('user_id').sum().sort_values('playtime_forever', ascending=False).reset_index().iloc[0,0]
    consulta_gb=consulta_2[['user_id','year','playtime_forever']][consulta_2['user_id']==usuario].groupby(['user_id','year']).sum().reset_index()
    dict_data = consulta_gb.to_dict(orient='records')
    lista = [{'Año': d['year'], 'Horas': int(round(d['playtime_forever'],0))} for d in dict_data]

    resultado = {"Usuario con más horas jugadas para Género {}".format(genero): usuario,
                "Horas jugadas": lista}
    return resultado
  
  except Exception as e :
    return {f'ERROR: {e}'}
  

@app.get('/UsersRecommend/{año}')
def UsersRecommend(year: int):
  '''Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.'''
  try:
    consulta_3 = pd.read_csv('./data/consultas/UsersRecommend.csv.gz',compression='gzip')
    recommend=consulta_3['app_name'][(consulta_3['year']==year) & (consulta_3['recommend']==True) & (consulta_3['sentiment_analysis']!=0)].value_counts().reset_index().head(3)
    result_list = [{"Puesto {}: {}".format(i + 1, row['app_name'])} for i, row in recommend.iterrows()]
    return result_list
  
  except Exception as e :
    return {f'ERROR: {e}'}
  
@app.get('/UsersNotRecommend/{año}')
def UsersNotRecommend(year: int):
  '''Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado.'''
  try:
    consulta_3 = pd.read_csv('./data/consultas/UsersRecommend.csv.gz',compression='gzip')
    recommend=consulta_3['app_name'][(consulta_3['year']==year) & (consulta_3['recommend']==False) & (consulta_3['sentiment_analysis']==0)].value_counts().reset_index().head(3)
    result_list = [{"Puesto {}: {}".format(i + 1, row['app_name'])} for i, row in recommend.iterrows()]
    return result_list
  
  except Exception as e :
    return {f'ERROR: {e}'}

@app.get('/sentiment_analysis/{año}')
def sentiment_analysis(year: int):
  '''Cantidad de reseñas de usuarios para el año dado.'''
  try:
    consulta_5 = pd.read_csv('./data/consultas/sentiment_analysis.csv.gz',compression='gzip')
    valores=consulta_5['sentiment_analysis'][consulta_5['year']==year].value_counts().reset_index()
    resultado = {'Negative': str(valores.loc[2, 'count']),
        'Neutral': str(valores.loc[1, 'count']),
        'Positive': str(valores.loc[0, 'count'])}
    
    return resultado

  except Exception as e :
    return {f'ERROR: {e}'}
  
@app.get('/sentiment_analysis/{año}')
def sentiment_analysis(year: int):
  '''Cantidad de reseñas de usuarios para el año dado.'''
  try:
    consulta_5 = pd.read_csv('./data/consultas/sentiment_analysis.csv.gz',compression='gzip')
    valores=consulta_5['sentiment_analysis'][consulta_5['year']==year].value_counts().reset_index()
    resultado = {'Negative': str(valores.loc[2, 'count']),
        'Neutral': str(valores.loc[1, 'count']),
        'Positive': str(valores.loc[0, 'count'])}
    
    return resultado

  except Exception as e :
    return {f'ERROR: {e}'}
  
@app.get('/recomendacion_juego/{id_de_producto}')
def recomendacion_juego(item_id :int):
  '''Ingresando el id de producto se recibie una lista con 5 juegos recomendados.'''
  try:
    consulta_ml_1 = pd.read_csv('./data/consultas/recomendacion_juego.csv.gz',compression='gzip')
    nombre_juego = consulta_ml_1.set_index('item_id').loc[item_id].values[0].split(',')[0]
    stop_words_steams = ['i', 'ii', 'iii','iv']
    stop = list(stopwords.words('english'))
    stop += stop_words_steams
    tf = TfidfVectorizer(stop_words=stop, token_pattern=r'\b[a-zA-Z]\w+\b' )
    data_vector = tf.fit_transform(consulta_ml_1['features'])
    data_vector_df = pd.DataFrame(data_vector.toarray(), index=consulta_ml_1['item_id'], columns = tf.get_feature_names_out())
    vector_similitud_coseno = cosine_similarity(data_vector_df.values)
    cos_sim_df = pd.DataFrame(vector_similitud_coseno, index=data_vector_df.index, columns=data_vector_df.index)
    juegos_similares = cos_sim_df.loc[item_id].nlargest(6)
    top5 = juegos_similares.iloc[1:6]
    resultado = consulta_ml_1.set_index('item_id').loc[top5.index]['features'].apply(lambda x: x.split(',')[0]).values
    mensaje = f"Como jugas {nombre_juego} te recomendamos:"
    juegos_recomendados_str = ', '.join(resultado)
    resultado_formateado = {mensaje: juegos_recomendados_str}
    return resultado_formateado
  except Exception as e :
    return {f'ERROR: {e}'}