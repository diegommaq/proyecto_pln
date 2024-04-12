import re
import pandas as pd
from fuzzywuzzy import process

"""
 Lectura y limpieza de datos de datos
"""
df_catalogo = pd.read_csv('catalogo.csv')
df_datos = pd.read_csv('datos.csv')

# Se descartan los datos del catálogo con clave mayor a 106
df_catalogo = df_catalogo[df_catalogo['CLAVE'] >= 106]

# Limpieza del catálogo
for i, fila in df_catalogo.iterrows():
    df_catalogo.loc[i, 'DESCRIPCIÓN'] = str(df_catalogo.loc[i, 'DESCRIPCIÓN'])[2:].replace('.', '').strip()

# Limpieza de los datos
for i, fila in df_datos.iterrows():
    for e in range(1,7):
        if str(df_datos.loc[i, f'E{e}']) == 'nan':
            # Se remplazan los valores "nan" por cadenas vacías
            df_datos.loc[i, f'E{e}'] = ''
        else:
            df_datos.loc[i, f'E{e}'] = str(df_datos.loc[i, f'E{e}']).replace('.', '').strip()

dict_catalogo = dict(zip(df_catalogo['DESCRIPCIÓN'], df_catalogo['CLAVE']))

"""
 Uso de fuzzywuzzy
"""

# Buscar valor con distancia más cercana
def search(value):
    return dict_catalogo.get(process.extractOne(value, dict_catalogo.keys())[0], None)

# Obtener clave de valor del catálogo mas cercano
for i, fila in df_datos.iterrows():
    for e in range(1,7):
        # Se excluyen los datos vacíos y numéricos
        if df_datos.loc[i, f'E{e}'] != '' and re.fullmatch("\d+", df_datos.loc[i, f'E{e}']) is None:
            clave = search(df_datos.loc[i, f'E{e}'])
            # print('Texto evaluado:', df_datos.loc[i, f'E{e}'])
            # print('Clave:', clave)
            df_datos.loc[i, f'E{e}'] = clave

df_datos.to_csv('datos_op2.csv', index=False)