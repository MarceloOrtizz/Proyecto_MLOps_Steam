import pandas as pd
from fastapi import FastAPI

app = FastAPI()


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
    # Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}
  except Exception as e :
    return {f'ERROR: {e}'}
  

# @app.get('/UserForGenre/{genero}')
# def UserForGenre(genero: str):
#   try:
#     consulta_2 = pd.read_csv('./data/consultas/UserForGenre.csv.gz',compression='gzip')
#     usuario=consulta_2[consulta_2['genres'].str.contains(genero)].sort_values('playtime_forever', ascending=False).iloc[0,1]
#     consulta_2=consulta_2[['year','playtime_forever']][consulta_2['user_id']==usuario][consulta_2[['year','playtime_forever']][consulta_2['user_id']==usuario]['playtime_forever']>0.5]
#     # paso el df a diccionario
#     dict_data = consulta_2.to_dict(orient='records')
#     # aplano el diccionario en una lista
#     lista = [{'Año': d['year'], 'Horas': int(round(d['playtime_forever'],0))} for d in dict_data]
#     resultado = {"Usuario con más horas jugadas para Género {}".format(genero): usuario,
#                 "Horas jugadas": lista}
#     return resultado
  
#   except Exception as e :
#     return {f'ERROR: {e}'}

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