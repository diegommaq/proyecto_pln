import re
import pandas as pd
import gensim
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

"""
 Uso de doc2vec
"""
# Creación del modelo
model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=40)

# Se contruye el corpus y un diccionario de clases
clases = {}
def map_corpus():
    id = -1
    for i, fila in df_catalogo.iterrows():
        id += 1
        tokens = str(df_catalogo.loc[i, 'DESCRIPCIÓN']).split()
        clases[id] = df_catalogo.loc[i, 'CLAVE']
        yield gensim.models.doc2vec.TaggedDocument(tokens, [id])
        
corpus = list(map_corpus())

# Se agrega el corpus al vocabulario del modelo
model.build_vocab(corpus)

# Entrenamiento del modelo
model.train(corpus, total_examples=model.corpus_count, epochs=model.epochs)

# Diccionario de datos
dict_catalogo = dict(zip(df_catalogo['DESCRIPCIÓN'], df_catalogo['CLAVE']))

# Buscar valor con distancia más cercana
def search(value):
    return process.extract(value, dict_catalogo.keys())

# Inferir vectores
for i, fila in df_datos.iterrows():
    for e in range(1,7):
        # Se excluyen los datos vacíos y numéricos
        if df_datos.loc[i, f'E{e}'] != '' and re.fullmatch("\d+", df_datos.loc[i, f'E{e}']) is None:
            vector = model.infer_vector(df_datos.loc[i, f'E{e}'].split())
            # Se obtienen el valor del catálogo más similar
            sims = model.dv.most_similar([vector], topn=len(model.dv))
            clave = search(df_datos.loc[i, f'E{e}'])
            # print('Texto evaluado:', df_datos.loc[i, f'E{e}'])
            # print('Más similar:', sims[0], df_catalogo[df_catalogo['CLAVE'] == clases[sims[0][0]]]['DESCRIPCIÓN'])

            if (sims[0][1] > clave[0][1]):
                print('d2v')
                df_datos.loc[i, f'E{e}'] = clases[sims[0][0]]
            else:
                print('fw')
                df_datos.loc[i, f'E{e}'] = dict_catalogo[clave[0][0]]

df_datos.to_csv('datos_op3.csv', index=False)