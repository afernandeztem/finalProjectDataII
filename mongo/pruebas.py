import mongo.repository.app_repository as app
import time


def test_index(func, *args):
    start_time = time.time()
    for x in range(500):
        func(*args)
    print(str(func.__name__)+": %s" % (time.time() - start_time))


print(app.get_numero_aplicaciones())
print(app.get_all_content_ratings())
test_index(app.get_all_generos)
test_index(app.get_all_content_ratings)
test_index(app.get_numero_aplicaciones)
test_index(app.get_numero_aplicaciones_pago)
test_index(app.get_numero_aplicaciones_gratuitas)
test_index(app.get_numero_aplicaciones_google_play)
test_index(app.get_numero_aplicaciones_gratuitas_google_play)
test_index(app.get_numero_aplicaciones_pago_google_play)
test_index(app.get_numero_aplicaciones_app_store)
test_index(app.get_numero_aplicaciones_gratuitas_app_store)
test_index(app.get_numero_aplicaciones_pago_app_store)
test_index(app.get_numero_aplicaciones_coincidentes)
test_index(app.get_numero_aplicaciones_gratuitas_coincidentes)
test_index(app.get_numero_aplicaciones_pago_coincidentes)
# test_index(app.get_precio)
# test_index(app.get_size)
# test_index(app.get_rating)
# test_index(app.get_n_rating)

# test_index(app.get_aplicaciones_rating_descendente)
# test_index(app.get_aplicaciones_rating_descendente_google_play)
# print(app.get_aplicaciones_rating_descendente_app_store())
# print(app.get_aplicaciones_price_descendente_google_play(20))
# print(app.get_aplicaciones_price_descendente_app_store(20))

test_index(app.get_precio_medio_aplicaciones, False)
test_index(app.get_precio_medio_aplicaciones, True)
test_index(app.get_precio_medio_aplicaciones_pago, False)
test_index(app.get_precio_medio_aplicaciones_pago, True)
test_index(app.get_precio_medio_aplicaciones_coincidentes)
test_index(app.get_precio_medio_aplicaciones_pago_coincidentes)
test_index(app.get_precio_medio_aplicaciones_por_generos, False)
test_index(app.get_precio_medio_aplicaciones_por_generos, True)
test_index(app.get_precio_medio_aplicaciones_por_content_rating, False)
test_index(app.get_precio_medio_aplicaciones_por_content_rating, True)
test_index(app.get_size_medio_aplicaciones)
test_index(app.get_size_medio_aplicaciones_coincidentes)
test_index(app.get_numero_ratings_medio_aplicaciones)
test_index(app.get_numero_ratings_medio_aplicaciones_coincidentes)
test_index(app.get_ratings_medio_aplicaciones_por_genero)
test_index(app.get_numero_ratings_medio_aplicaciones_por_genero)

test_index(app.get_ratings_medio_aplicaciones_por_content_rating)
test_index(app.get_numero_ratings_medio_aplicaciones_por_content_rating)
test_index(app.get_numero_aplicaciones_por_content_rating)
test_index(app.get_numero_aplicaciones_por_genero)

for i in app.get_all_content_ratings():
    print(i)
    test_index(app.get_precio_medio_aplicaciones_por_genero_un_content_rating, i)
    test_index(app.get_size_medio_aplicaciones_por_genero_un_content_rating, i)
    test_index(app.get_numero_ratings_medio_aplicaciones_por_genero_un_content_rating, i)
    test_index(app.get_ratings_medio_aplicaciones_por_genero_un_content_rating, i)
