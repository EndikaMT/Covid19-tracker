import requests
import pandas as pd
from bs4 import BeautifulSoup
from html_table_parse_class import TableParser
import matplotlib.pyplot as plt


# Web en la que disponemos de la tabla a parsear.

source = "https://www.worldometers.info/coronavirus/"

# Llamamos a la clase y pasamos la función para obtener la información de la tabla en base al source espeficicado
 
html = TableParser()
table = html.parse_source(source)[0][1]

# Bloque de normalización y un poco de "preprocesado"

## Creamos la lista de elementos que vamos a descartar (en la tabla aparece subtotales que no queremos)
errors = ['Total:', '\nNorthAmerica\n', '\nEurope\n', '\nAsia\n', '\nSouthAmerica\n', '\nOceania\n', '\nAfrica\n', 'World', '\n\n', 'DiamondPrincess']

## Renombramos columnas con símbolos o caracteres raros que nos pueden dar problemas en el futuro
table.rename(columns={ table.columns[0]: "Country" }, inplace = True)
table.rename(columns={ table.columns[7]: "Critical" }, inplace = True)
table.rename(columns={ table.columns[11]: "Tests/1M pop" }, inplace = True)

## Dentro del dataframe, eliminamos los elementos cuyo valor de "country" esté dentro del listado de errores especificados
table = table[~table.Country.isin(errors)]

## Renombramos la tabla como table_clean para hacer el segundo bloque de preprocesado
table_clean = table

## Ordenamos el dataframe por mayor a menor número de casos detectados
table_clean = table_clean.sort_values('TotalCases', ascending=False)

## Con la función to_csv de Pandas, exportamos el dataframe sin exportar el número de indice de la tabla e indicando el separador
table_clean.to_csv("Covid19.csv", sep=';', index=False)
## Obtenemos un head para ver el formato de la tabla y los primeros elementos

table_clean = table_clean[:15]
print(table_clean)
table_clean['ActiveCases'] = table_clean['ActiveCases'].astype(int)
table_clean['TotalDeaths'] = table_clean['TotalDeaths'].astype(int)
table_clean['TotalRecovered'] = table_clean['TotalRecovered'].astype(int)
table_clean.set_index("Country", drop=True, inplace=True)
ax = table_clean[['TotalDeaths','ActiveCases','TotalRecovered']].plot(kind='bar', title ="COVID-19 by Country", figsize=(15, 10), legend=True, fontsize=12, stacked=True)
ax.set_xlabel("Countries", fontsize=12)
ax.set_ylabel("Cases", fontsize=12)
plt.show()