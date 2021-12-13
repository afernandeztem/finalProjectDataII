import pymongo

import mongo.mongo_utils as utils
from mongo.mongo_manager import app_collection


def get_all_generos() -> list:
    return app_collection.find().distinct("genres")


def get_all_content_ratings() -> list:
    return app_collection.find().distinct("content_rating")


def get_numero_aplicaciones() -> int:
    return app_collection.count()


def get_numero_aplicaciones_app_store() -> int:
    return app_collection.count({'available.app_store': True})


def get_numero_aplicaciones_google_play() -> int:
    return app_collection.count({'available.google_play': True})


def get_numero_aplicaciones_coincidentes() -> int:
    return app_collection.count({'available.google_play': True, 'available.app_store': True})


def get_numero_aplicaciones_gratuitas() -> int:
    return app_collection.count({'type': False})


def get_numero_aplicaciones_pago() -> int:
    return app_collection.count({'type': True})


def get_numero_aplicaciones_gratuitas_google_play() -> int:
    return app_collection.count({'type': False, 'available.google_play': True})


def get_numero_aplicaciones_pago_google_play() -> int:
    return app_collection.count({'type': True, 'available.google_play': True})


def get_numero_aplicaciones_gratuitas_app_store() -> int:
    return app_collection.count({'type': False, 'available.app_store': True})


def get_numero_aplicaciones_pago_app_store() -> int:
    return app_collection.count({'type': True, 'available.app_store': True})


def get_numero_aplicaciones_gratuitas_coincidentes() -> int:
    return app_collection.count({'type': False, 'available.app_store': True, 'available.google_play': True})


def get_numero_aplicaciones_pago_coincidentes() -> int:
    return app_collection.count({'type': True, 'available.app_store': True, 'available.google_play': True})


def get_precio() -> dict:
    returned = {'price_google_price': [], 'price_app_store': []}
    lista = list(app_collection.find({}, {'_id': 0, 'price.google_play': 1, 'price.app_store': 1}))
    for x in lista:
        price = x.get('price')
        if price:
            if price.get('google_play') is not None:
                returned['price_google_price'].append(price.get('google_play'))
            if price.get('app_store') is not None:
                returned['price_app_store'].append(price.get('app_store'))
    return returned


def get_size() -> dict:
    returned = {'size_google_play': [], 'size_app_store': []}
    lista = list(app_collection.find({}, {'_id': 0, 'size.google_play': 1, 'size.app_store': 1}))
    for x in lista:
        size = x.get('size')
        if size:
            if size.get('google_play') is not None:
                returned['size_google_play'].append(size.get('google_play'))
            if size.get('app_store') is not None:
                returned['size_app_store'].append(size.get('app_store'))
    return returned


def get_n_rating() -> dict:
    returned = {'n_rating_google_play': [], 'n_rating_app_store': []}
    lista = list(app_collection.find({}, {'_id': 0, 'n_rating.google_play': 1, 'n_rating.app_store': 1}))
    for x in lista:
        n_rating = x.get('n_rating')
        if n_rating:
            if n_rating.get('google_play') is not None:
                returned['n_rating_google_play'].append(n_rating.get('google_play'))
            if n_rating.get('app_store') is not None:
                returned['n_rating_app_store'].append(n_rating.get('app_store'))
    return returned


def get_rating() -> dict:
    returned = {'rating_google_play': [], 'rating_app_store': []}
    lista = list(app_collection.find({}, {'_id': 0, 'rating.google_play': 1, 'rating.app_store': 1}))
    for x in lista:
        rating = x.get('rating')
        if rating:
            if rating.get('google_play') is not None:
                returned['rating_google_play'].append(rating.get('google_play'))
            else:
                returned['rating_google_play'].append(None)
            if rating.get('app_store') is not None:
                returned['rating_app_store'].append(rating.get('app_store'))
            else:
                returned['rating_app_store'].append(None)
        else:
            returned['rating_google_play'].append(None)
            returned['rating_app_store'].append(None)

    return returned


def get_aplicaciones_rating_descendente(limit: int = 5) -> list:
    return list(app_collection.find({}, {'_id': 0, 'name': 1, 'rating.total_average': 1}).sort('rating.total_average',
                                                                                               pymongo.DESCENDING).limit(
        limit))


def get_aplicaciones_rating_descendente_google_play(limit: int = 5) -> list:
    return list(app_collection.find({'available.google_play': True}, {'_id': 0, 'name': 1, 'rating.google_play': 1}).sort('rating.google_play',
                                                                                             pymongo.DESCENDING).limit(
        limit))


def get_aplicaciones_rating_descendente_app_store(limit: int = 5) -> list:
    return list(app_collection.find({'available.app_store': True}, {'_id': 0, 'name': 1, 'rating.app_store': 1}).sort('rating.app_store',
                                                                                           pymongo.DESCENDING).limit(
        limit))


def get_aplicaciones_price_descendente_google_play(limit: int = 5) -> list:
    return list(app_collection.find({'available.google_play': True}, {'_id': 0, 'name': 1, 'price.google_play': 1}).sort('price.google_play',
                                                                                            pymongo.DESCENDING).limit(
        limit))


def get_aplicaciones_price_descendente_app_store(limit: int = 5) -> list:
    return list(app_collection.find({'available.app_store': True}, {'_id': 0, 'name': 1, 'price.app_store': 1}).sort('price.app_store',
                                                                                          pymongo.DESCENDING).limit(
        limit))


def get_precio_medio_aplicaciones_por_genero_un_content_rating(content_rating) -> list:
    group = utils.aggregate_group({'_id': "$genres",
                                   'precio_google': utils.mongo_avg('$price.google_play'),
                                   'precio_appstore': utils.mongo_avg('$price.app_store')})
    project = utils.aggregate_project({'_id': 0, 'genre': '$_id', 'precio_google': 1, 'precio_appstore': 1})
    consulta_match_1 = {}
    consulta_match_2 = utils.mongo_or([{"price.google_play": {'$lt': 250}}, {'price.google_play': None}])
    unwind = utils.aggregate_unwind("$genres")
    sort = utils.aggregate_sort({'_id': 1})
    consulta_match_1['content_rating'] = content_rating
    mat_1 = utils.aggregate_match(consulta_match_1)
    mat_2 = utils.aggregate_match(consulta_match_2)
    query = [mat_1, unwind, mat_2, group, sort, project]
    res = list(app_collection.aggregate(query))
    return res


def get_size_medio_aplicaciones_por_genero_un_content_rating(content_rating) -> list:
    group = utils.aggregate_group({'_id': "$genres",
                                   'size_medio_google': utils.mongo_avg('$size.google_play'),
                                   'size_medio_appstore': utils.mongo_avg(
                                       '$size.app_store')})
    project = utils.aggregate_project({'_id': 0, 'genre': '$_id', 'size_medio_google': 1, 'size_medio_appstore': 1})
    consulta_match_1 = {}
    unwind = utils.aggregate_unwind("$genres")
    sort = utils.aggregate_sort({'_id': 1})
    consulta_match_1['content_rating'] = content_rating
    mat_1 = utils.aggregate_match(consulta_match_1)
    query = [mat_1, unwind, group, sort, project]
    res = list(app_collection.aggregate(query))
    return res


def get_ratings_medio_aplicaciones_por_genero_un_content_rating(content_rating) -> list:
    group = utils.aggregate_group({'_id': "$genres",
                                   'rating_medio_google': utils.mongo_avg('$rating.google_play'),
                                   'rating_medio_appstore': utils.mongo_avg(
                                       '$rating.app_store')})
    project = utils.aggregate_project({'_id': 0, 'genre': '$_id', 'rating_medio_google': 1, 'rating_medio_appstore': 1})
    consulta_match_1 = {}
    unwind = utils.aggregate_unwind("$genres")
    sort = utils.aggregate_sort({'_id': 1})
    consulta_match_1['content_rating'] = content_rating
    mat_1 = utils.aggregate_match(consulta_match_1)
    query = [mat_1, unwind, group, sort, project]
    res = list(app_collection.aggregate(query))
    return res


def get_numero_ratings_medio_aplicaciones_por_genero_un_content_rating(content_rating) -> list:
    group = utils.aggregate_group({'_id': "$genres",
                                   'numero_rating_medio_google': utils.mongo_avg('$n_rating.google_play'),
                                   'numero_rating_medio_appstore': utils.mongo_avg(
                                       '$n_rating.app_store')})
    project = utils.aggregate_project(
        {'_id': 0, 'genre': '$_id', 'numero_rating_medio_google': 1, 'numero_rating_medio_appstore': 1})
    consulta_match_1 = {}
    unwind = utils.aggregate_unwind("$genres")
    sort = utils.aggregate_sort({'_id': 1})
    consulta_match_1['content_rating'] = content_rating
    mat_1 = utils.aggregate_match(consulta_match_1)
    query = [mat_1, unwind, group, sort, project]
    res = list(app_collection.aggregate(query))
    return res


def get_precio_medio_aplicaciones(outliers: bool = False) -> dict:
    if outliers:
        consulta_match = utils.mongo_or([{"price.google_play": {'$lt': 250}}, {'price.google_play': None}])
        mat = utils.aggregate_match(consulta_match)
        query = [mat, utils.aggregate_group(
            {'_id': None, 'precio_google': utils.mongo_avg('$price.google_play'),
             'precio_appstore': utils.mongo_avg('$price.app_store')})]
    else:
        query = [utils.aggregate_group(
            {'_id': None, 'precio_google': utils.mongo_avg('$price.google_play'),
             'precio_appstore': utils.mongo_avg('$price.app_store')})]
    res = list(app_collection.aggregate(query))
    if res:
        res = res[0]
        res.pop('_id')
        return res
    else:
        return {}


def get_precio_medio_aplicaciones_pago(outliers: bool = False) -> dict:
    group = utils.aggregate_group({'_id': None,
                                   'precio_google': utils.mongo_avg('$price.google_play'),
                                   'precio_appstore': utils.mongo_avg(
                                       '$price.app_store')})
    if outliers:
        consulta_match = utils.mongo_or([{"price.google_play": {'$lt': 250}}, {'price.google_play': None}])
        consulta_match['type'] = True
        mat = utils.aggregate_match(consulta_match)
        query = [mat, group]
    else:
        query = [utils.aggregate_match({'type': True}), group]
    res = list(app_collection.aggregate(query))
    if res:
        res = res[0]
        res.pop('_id')
        return res
    else:
        return {}


def get_precio_medio_aplicaciones_coincidentes(outliers: bool = False) -> dict:
    group = utils.aggregate_group({'_id': None,
                                   'precio_google': utils.mongo_avg('$price.google_play'),
                                   'precio_appstore': utils.mongo_avg(
                                       '$price.app_store')})
    if outliers:
        consulta_match = {"price.google_play": {'$lt': 250}, 'available.google_play': True, 'available.app_store': True}
        mat = utils.aggregate_match(consulta_match)
        query = [mat, group]
    else:
        query = [utils.aggregate_match({'available.google_play': True, 'available.app_store': True}), group]
    res = list(app_collection.aggregate(query))
    if res:
        res = res[0]
        res.pop('_id')
        return res
    else:
        return {}


def get_precio_medio_aplicaciones_pago_coincidentes(outliers: bool = False) -> dict:
    group = utils.aggregate_group({'_id': None,
                                   'precio_google': utils.mongo_avg('$price.google_play'),
                                   'precio_appstore': utils.mongo_avg(
                                       '$price.app_store')})
    if outliers:
        consulta_match = {"price.google_play": {'$lt': 250}, 'type': True, 'available.google_play': True,
                          'available.app_store': True}
        mat = utils.aggregate_match(consulta_match)
        query = [mat, group]
    else:
        query = [utils.aggregate_match({'type': True, 'available.google_play': True, 'available.app_store': True}),
                 group]
    res = list(app_collection.aggregate(query))
    if res:
        res = res[0]
        res.pop('_id')
        return res
    else:
        return {}


def get_precio_medio_aplicaciones_por_generos(outliers: bool = False) -> list:
    group = utils.aggregate_group({'_id': "$genres",
                                   'precio_google': utils.mongo_avg('$price.google_play'),
                                   'precio_appstore': utils.mongo_avg(
                                       '$price.app_store')})
    unwind = utils.aggregate_unwind("$genres")
    project = utils.aggregate_project({'_id': 0, 'genre': '$_id', 'precio_google': 1, 'precio_appstore': 1})
    sort = utils.aggregate_sort({'_id': 1})
    if outliers:
        consulta_match = utils.mongo_or([{"price.google_play": {'$lt': 250}}, {'price.google_play': None}])
        mat = utils.aggregate_match(consulta_match)
        query = [mat, unwind, group, sort, project]
    else:
        query = [unwind, group, sort, project]
    res = list(app_collection.aggregate(query))
    return res


def get_precio_medio_aplicaciones_por_content_rating(outliers: bool = False) -> list:
    group = utils.aggregate_group({'_id': "$content_rating",
                                   'precio_google': utils.mongo_avg('$price.google_play'),
                                   'precio_appstore': utils.mongo_avg(
                                       '$price.app_store')})
    project = utils.aggregate_project({'_id': 0, 'content_rating': '$_id', 'precio_google': 1, 'precio_appstore': 1})
    sort = utils.aggregate_sort({'_id': 1})
    if outliers:
        consulta_match = utils.mongo_or([{"price.google_play": {'$lt': 250}}, {'price.google_play': None}])
        mat = utils.aggregate_match(consulta_match)
        query = [mat, group, sort, project]
    else:
        query = [group, sort, project]
    res = list(app_collection.aggregate(query))
    return res


def get_size_medio_aplicaciones() -> dict:
    group = utils.aggregate_group({'_id': None,
                                   'size_medio_google': utils.mongo_avg('$size.google_play'),
                                   'size_medio_appstore': utils.mongo_avg(
                                       '$size.app_store')})
    query = [group]
    res = list(app_collection.aggregate(query))
    if res:
        res = res[0]
        res.pop('_id')
        return res
    else:
        return {}


def get_numero_ratings_medio_aplicaciones() -> dict:
    group = utils.aggregate_group({'_id': None,
                                   'n_rating_medio_google': utils.mongo_avg('$n_rating.google_play'),
                                   'n_rating_medio_appstore': utils.mongo_avg(
                                       '$n_rating.app_store')})
    query = [group]
    res = list(app_collection.aggregate(query))
    if res:
        res = res[0]
        res.pop('_id')
        return res
    else:
        return {}


def get_ratings_medio_aplicaciones() -> dict:
    group = utils.aggregate_group({'_id': None,
                                   'rating_medio_google': utils.mongo_avg('$rating.google_play'),
                                   'rating_medio_appstore': utils.mongo_avg(
                                       '$rating.app_store')})
    query = [group]
    res = list(app_collection.aggregate(query))
    if res:
        res = res[0]
        res.pop('_id')
        return res
    else:
        return {}


def get_size_medio_aplicaciones_coincidentes() -> dict:
    group = utils.aggregate_group({'_id': None,
                                   'size_medio_google': utils.mongo_avg('$size.google_play'),
                                   'size_medio_appstore': utils.mongo_avg(
                                       '$size.app_store')})
    query = [utils.aggregate_match({'available.google_play': True, 'available.app_store': True}), group]
    res = list(app_collection.aggregate(query))
    if res:
        res = res[0]
        res.pop('_id')
        return res
    else:
        return {}


def get_numero_ratings_medio_aplicaciones_coincidentes() -> dict:
    group = utils.aggregate_group({'_id': None,
                                   'n_rating_medio_google': utils.mongo_avg('$n_rating.google_play'),
                                   'n_rating_medio_appstore': utils.mongo_avg(
                                       '$n_rating.app_store')})
    query = [utils.aggregate_match({'available.google_play': True, 'available.app_store': True}), group]
    res = list(app_collection.aggregate(query))
    if res:
        res = res[0]
        res.pop('_id')
        return res
    else:
        return {}


def get_ratings_medio_aplicaciones_coincidentes() -> dict:
    group = utils.aggregate_group({'_id': None,
                                   'rating_medio_google': utils.mongo_avg('$rating.google_play'),
                                   'rating_medio_appstore': utils.mongo_avg(
                                       '$rating.app_store')})
    query = [utils.aggregate_match({'available.google_play': True, 'available.app_store': True}), group]
    res = list(app_collection.aggregate(query))
    if res:
        res = res[0]
        res.pop('_id')
        return res
    else:
        return {}


def get_ratings_medio_aplicaciones_por_genero() -> list:
    unwind = utils.aggregate_unwind("$genres")
    group = utils.aggregate_group({'_id': "$genres",
                                   'rating_medio_google': utils.mongo_avg('$rating.google_play'),
                                   'rating_medio_appstore': utils.mongo_avg(
                                       '$rating.app_store')})
    project = utils.aggregate_project({'_id': 0, 'genre': '$_id', 'rating_medio_google': 1, 'rating_medio_appstore': 1})
    sort = utils.aggregate_sort({'_id': 1})
    query = [unwind, group, sort, project]
    res = list(app_collection.aggregate(query))
    return res


def get_numero_ratings_medio_aplicaciones_por_genero() -> list:
    unwind = utils.aggregate_unwind("$genres")
    group = utils.aggregate_group({'_id': "$genres",
                                   'numero_rating_medio_google': utils.mongo_avg('$n_rating.google_play'),
                                   'numero_rating_medio_appstore': utils.mongo_avg(
                                       '$n_rating.app_store')})
    project = utils.aggregate_project(
        {'_id': 0, 'genre': '$_id', 'numero_rating_medio_google': 1, 'numero_rating_medio_appstore': 1})
    sort = utils.aggregate_sort({'_id': 1})
    query = [unwind, group, sort, project]
    res = list(app_collection.aggregate(query))
    return res


def get_ratings_medio_aplicaciones_por_content_rating() -> list:
    group = utils.aggregate_group({'_id': "$content_rating",
                                   'rating_medio_google': utils.mongo_avg('$rating.google_play'),
                                   'rating_medio_appstore': utils.mongo_avg(
                                       '$rating.app_store')})
    project = utils.aggregate_project(
        {'_id': 0, 'content_rating': '$_id', 'rating_medio_google': 1, 'rating_medio_appstore': 1})
    sort = utils.aggregate_sort({'_id': 1})
    query = [group, sort, project]
    res = list(app_collection.aggregate(query))
    return res


def get_numero_ratings_medio_aplicaciones_por_content_rating() -> list:
    group = utils.aggregate_group({'_id': "$content_rating",
                                   'numero_rating_medio_google': utils.mongo_avg('$n_rating.google_play'),
                                   'numero_rating_medio_appstore': utils.mongo_avg(
                                       '$n_rating.app_store')})
    project = utils.aggregate_project(
        {'_id': 0, 'content_rating': '$_id', 'numero_rating_medio_google': 1, 'numero_rating_medio_appstore': 1})
    sort = utils.aggregate_sort({'_id': 1})
    query = [group, sort, project]
    res = list(app_collection.aggregate(query))
    return res


def get_numero_aplicaciones_por_content_rating() -> list:
    group = utils.aggregate_group({'_id': "$content_rating",
                                   'total': utils.mongo_sum(1)})
    project = utils.aggregate_project(
        {'_id': 0, 'content_rating': '$_id', 'total': 1})
    sort = utils.aggregate_sort({'total': -1})
    query = [group, sort, project]
    res = list(app_collection.aggregate(query))
    return res


def get_numero_aplicaciones_por_genero() -> list:
    unwind = utils.aggregate_unwind("$genres")
    group = utils.aggregate_group({'_id': "$genres", 'total': utils.mongo_sum(1)})
    project = utils.aggregate_project(
        {'_id': 0, 'genre': '$_id', 'total': 1})
    sort = utils.aggregate_sort({'total': -1})
    query = [unwind, group, sort, project]
    res = list(app_collection.aggregate(query))
    return res
