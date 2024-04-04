# Predicción de texto con base en catálogo

## Limpieza y pre-procesamiento de datos

**Consideraciones**
- Los datos del catálogo a considerar son a partir de la clave 106 en adelante.
- Cada uno de los valores del catálogo empiesa con la palabra _ES_.

**Proceso de lectura y limpieza de datos**
1. Leer los archivos de catálogo y de datos y almacenarlos en _dataframes_.
2. Del _dataframe_ del catálogo, excluir los valores cuya clave sea menor a 106.
3. Del _dataframe_ del catálogo, eliminar para todos los valores la primera palabra: "ES".
4. De ambos _dataframes_ (catálogo y datos) eliminar para todos los valores los signos de puntuación y los espacios en blanco al inicio y final del valor.

## Opcion 1: Doc2Vec

Archivo: **op1_word2vec.py**

**Proceso**
1. Se crea el modelo con los parámetro: *vector_size=50*, *min_count=2* y *epochs=40*.
2. Se crea un corpus y un vocabulario a partir del catálogo.
3. Se entrena el modelo con el corpus creado.
4. Para cada dato, se infiere un vector utilizando el modelo creado. **Nota**: Se excluyen los datos vacíos o que solo contengan valores numéricos.
5. A partir del vector, se obtiene el valor del catálogo más similar.