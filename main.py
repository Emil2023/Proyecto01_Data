
from fastapi import FastAPI

#Importamos librerias

import pandas as pd
from typing import Union
import unicodedata as unicodedata
import json

#Clase de la api
app = FastAPI()

# Cargamos el archivo
df = pd.read_csv('movies_dataset_clean.csv')

df['release_date'] = pd.to_datetime(df['release_date'])
df['release_month'] = df['release_date'].dt.month_name()
df['release_day'] = df['release_date'].dt.day_name()
#Diccionario para el usario ingrese el mes en español
def traductor_mes():
    meses = {'January':'Enero', 'February':'Febrero', 'March':'Marzo', 'April':'Abril', 'May':'Mayo', 'June':'Junio', 'July':'Julio', 'August':'Agosto', 'September':'Septiembre', 'October':'Octubre', 'November':'Noviembre', 'December':'Diciembre'}
    df['release_month'] = df['release_month'].map(meses)
traductor_mes()
#Diccionario para el usario ingrese el dia en español
def traductor_dia():
    dias = {'Monday':'Lunes', 'Tuesday':'Martes', 'Wednesday':'Miercoles', 'Thursday':'Jueves', 'Friday':'Viernes', 'Saturday':'Sabado', 'Sunday':'Domingo'}
    df['release_day'] = df['release_day'].map(dias)
traductor_dia()


#Funcion 1 
@app.get('/cantidad_filmaciones_mes/{Mes}')
def cantidad_filmaciones_mes(mes):
    df_mes = df[df['release_month'] == mes]
    cantidad = len(df_mes)
    return {'mes':mes, 'cantidad':cantidad}


#Funcion 2
@app.get('/cantidad_filmaciones_dia/{Dia}')
def cantidad_filmaciones_dia(dia:str):
    # Obtiene la cantidad de películas estrenadas en el día especificado
    df_dia = df[df['release_day'] == dia]
    cantidad = len(df_dia)
    return {'dia':dia, 'cantidad':cantidad}

#Funcion 3
@app.get('/score_titulo/{titulo}')
def score_titulo(titulo: str):
    
    # Filtrar el DataFrame por el título de la filmación
    filtro_titulo = df['title'].str.lower() == titulo.lower()
    pelicula = df[filtro_titulo]
    
    if len(pelicula) == 0:
        return "No se encontró la película."
    
    # Obtener el título, el año de estreno y el score de la película
    titulo = pelicula['title'].values[0]
    año_estreno = pelicula['release_year'].values[0]
    score = pelicula['popularity'].values[0]
    
    #respuesta
    
    return {'titulo':titulo, 'anio':año_estreno, 'popularidad':score}

#Funcion 4
@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo:str):
    
    # Convertir el título de la filmación a minúsculas
    titulo_filtrar = titulo.lower()
    
    # Convertir la columna 'title' del DataFrame a minúsculas y filtrar
    filtro_titulo = df['title'].str.lower() == titulo_filtrar
    pelicula = df[filtro_titulo]
    
    if len(pelicula) == 0:
        return "No se encontró la película."
    
    # Obtener la cantidad de votos y el valor promedio de las votaciones
    votos = pelicula['vote_count'].values[0]
    
    if votos < 2000:
        return "La película no cumple con la cantidad mínima de valoraciones."
    
    promedio = pelicula['vote_average'].values[0]
    
    # Obtener el título y el año de estreno de la película
    titulo = pelicula['title'].values[0]
    año_estreno = pelicula['release_year'].values[0]
    
    #respuesta
    return {'titulo':titulo, 'anio':año_estreno, 'voto_total':votos, 'voto_promedio':promedio}

#Funcion 5
@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor: str):

    # Filtramos las filas donde el actor está presente en la columna 'elenco'
    filtro_actor = df['elenco'].str.contains(nombre_actor, case=False)
    peliculas_actor = df[filtro_actor]

    if len(peliculas_actor) > 0:
        cantidad_films = len(peliculas_actor)
        retorno_total = peliculas_actor['return'].sum()
        promedio_retorno = retorno_total / cantidad_films

        return {'actor':nombre_actor, 'cantidad_filmaciones':cantidad_films, 'retorno_total':retorno_total, 'retorno_promedio':promedio_retorno}

#Funcion 6 
@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):

    # Filtramos las filas donde el director está presente en la columna 'director'
    filtro_director = df['directores'].str.contains(nombre_director, case=False)
    peliculas_director = df[filtro_director]
    
    if len(peliculas_director) > 0:
        retorno_total_director = peliculas_director['return'].sum()
        
        peliculas = []
        
        for index, pelicula in peliculas_director.iterrows():
            titulo = pelicula['title']
            fecha_lanzamiento = pelicula['release_date']
            retorno_pelicula = pelicula['return']
            budget_pelicula = pelicula['budget']
            revenue_pelicula = pelicula['revenue']
            
            peliculas.append({
                'titulo': titulo,
                'fecha_lanzamiento': fecha_lanzamiento,
                'retorno_pelicula': retorno_pelicula,
                'budget_pelicula': budget_pelicula,
                'revenue_pelicula': revenue_pelicula
            })
        
        return {
            'director': nombre_director,
            'retorno_total_director': retorno_total_director,
            'peliculas': peliculas
        }
    else:
        return f"No se encontraron registros para el director {nombre_director}."
    




