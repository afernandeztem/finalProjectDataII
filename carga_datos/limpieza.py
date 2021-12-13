import pandas as pd

from mongo.mongo_manager import app_collection
from carga_datos.utils import to_mega_bytes, get_content_rating, get_genres, get_n_rating, get_user_rating, get_price, \
                              get_availability

# Configuración del layout por consola de la pantalla
pd.set_option('display.max_columns', None)

# Carga de Datasets y eliminación de columnas innecesarias
apple = pd.read_csv('../resources/AppleStore.csv', delimiter=',')
apple = apple.drop(['#', 'id', 'currency', 'ver', 'rating_count_ver', 'user_rating_ver',
                    'sup_devices.num', 'ipadSc_urls.num', 'lang.num',
                    'vpp_lic'], 1)

google = pd.read_csv('../resources/googleplaystore.csv', delimiter=',')
google = google.drop(['Android Ver', 'Category', 'Current Ver', 'Last Updated', 'Type', 'Installs'], 1)

# Comprobamos los valores NaN y Null de los datasts, y los sustituimos por otros valores
google['Content Rating'].fillna("Unrated", inplace=True)

apple.columns = ['name', 'size_apple', 'price_apple', 'n_rating_apple', 'rating_apple', 'content_rating_apple',
                 'genres']
google.columns = ['name', 'rating_google', 'n_rating_google', 'size_google', 'price_google', 'content_rating_google',
                  'genres']

# Eliminar entradas duplicadas por nombres
google = google.drop_duplicates(subset='name', keep="first")
apple = apple.drop_duplicates(subset='name', keep="first")

# Limpieza adicional de valores en algunas columnas
google = google.replace(to_replace="\$", regex=True, value="")
google['content_rating_google'] = google['content_rating_google'].replace(to_replace="[^\d]+", regex=True,
                                                                          value="")
apple['content_rating_apple'] = apple['content_rating_apple'].replace(to_replace="[^\d]+", regex=True,
                                                                      value="")

# Añadimos una columna para saber a posteriori qn qué tiendas está la aplicación
google['from_google'] = True
apple['from_apple'] = True

# Ponemos todos los nombres en minúscula para aumentar el porcentaje de ocurrencias entre ambos datasets en el merge
google['name'] = google['name'].str.lower()
apple['name'] = apple['name'].str.lower()

# Eliminamos las ocurrencias de nombres duplicadas, ya que se trata de distintas versiones de las aplicaciones y es un
# dato que no nos interesa
google = google.drop_duplicates(subset='name', keep="first")
apple = apple.drop_duplicates(subset='name', keep="first")

# Unión de ambos datasets, de acuerdo a la columna 'name'
merge = pd.merge(google, apple, on=['name'], how='outer')

documents = []

for row in merge.iterrows():
    doc = {}
    columns = row[1]
    # Name
    doc['name'] = columns['name']

    # Genres
    doc['genres'] = get_genres(columns['genres_x'], columns['genres_y'])

    # Sizes
    size = {}
    size_google = to_mega_bytes(columns['size_google'])
    if size_google:
        size.update({'google_play': size_google})
    size_apple = to_mega_bytes(columns['size_apple'])
    if size_apple:
        size.update({'app_store': size_apple})
    doc['size'] = size

    # Content rating
    content_rating = get_content_rating(columns['content_rating_google'], columns['content_rating_apple'])
    if content_rating:
        doc['content_rating'] = content_rating
    else:
        doc['content_rating'] = "Unrated"

    # N rating
    n_rating = get_n_rating(columns['n_rating_google'], columns['n_rating_apple'])
    if n_rating:
        doc['n_rating'] = n_rating

    # User rating
    user_rating = get_user_rating(columns['rating_google'], columns['rating_apple'])
    if user_rating:
        doc['rating'] = user_rating

    # Price
    price, pago = get_price(columns['price_google'], columns['price_apple'])
    if len(price) > 0:
        doc['price'] = price
        doc['type'] = pago

    # Availability
    availability = get_availability(columns['from_google'], columns['from_apple'])
    if len(availability) > 0:
        doc['available'] = availability
    documents.append(doc)

app_collection.insert_many(documents)
