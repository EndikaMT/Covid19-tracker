import requests
import pandas as pd
from bs4 import BeautifulSoup

class TableParser:
       
    # Función en la que con Requests, obtenemos el código de la web y con BeautifulSoup obtenemos todo el contenido de la tabla específica en base al ID   
    def parse_source(self, source):
        response = requests.get(source)
        soup = BeautifulSoup(response.text, 'lxml') # Usamos lxml aunque también se podría usar "HTML.Parser", desconozco mucho las diferencias
        return [(table['id'],self.parse_table(table))\
                for table in soup.find_all('table',id="main_table_countries_today")]  # importante pasar en el soup el ID de la tabla para que no coja ninguna otra (posibles cambios en la web)
    
    # Una vez tenemos la tabla, con esta función vamos obteniendo columnas y celdas de la tabla
    def parse_table(self, table):
        num_columns = 0
        num_rows=0
        column_titles = []
    
        # Encontramos el número de filas y columnas además del título de estas últimas
        for row in table.find_all('tr'):
            # Determinamos cuántas filas tiene la tabla
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                num_rows+=1
                if num_columns == 0:
                    # Definimos de manera dinámica el número de columnas (no es necesario especificar el número de columnas en concreto)
                    num_columns = len(td_tags)
                        
            # Definimos el título de las distintas columnas
            th_tags = row.find_all('th') 
            if len(th_tags) > 0 and len(column_titles) == 0:
                for th in th_tags:
                    column_titles.append(th.get_text())
    
        # Añadimos las columnas de la tabla como columnas del dataframe de Pandas
        columns = column_titles if len(column_titles) > 0 else range(0,num_columns)
        df = pd.DataFrame(columns = columns,
                              index= range(0,num_rows))

        # Añadimos el resto del contenido
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker,column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1
                    
        # Limpieza de columnas y preprocesado
        for col in df:
            try:
                # Eliminamos separador de miles en formato americano
                df.replace(',','', regex=True, inplace=True)
                df.replace('N/A',0, regex=True, inplace=True)
                df.replace('\+','', regex=True, inplace=True)
                df.replace('\-','', regex=True, inplace=True)
                df.replace('', 0, regex=True, inplace=True)
                # Forzamos a que todos los valores de las columnas, si se puede, sea integers (números enteros)
                df[col] = df[col].astype(int)
            except ValueError:
                pass
        return df
