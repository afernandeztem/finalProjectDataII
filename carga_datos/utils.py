import math


def is_nan(x):
    return type(x) is float and math.isnan(float(x))


def to_mega_bytes(x):
    try:
        if not is_nan(x):
            x = str(x)
            size = x[:-1]
            unit = x[-1].lower()
            if unit.isdigit() or unit == 'b':
                res = float(size) / 1000000
            elif unit == 'k':
                res = float(size) / 1000
            else:
                res = float(size)
        else:
            res = None
    except Exception:
        res = None
    return res


def get_content_rating(x, y):
    if is_nan(x) and is_nan(y):
        res = "Unrated"
    elif is_nan(x) and not is_nan(y):
        res = y
    elif not is_nan(x) and is_nan(y):
        res = x
    elif x == '':
        res = y
    else:
        x = int(x)
        y = int(y)
        if x >= y:
            res = str(y)
        else:
            res = str(x)
    if not res:
        res = "Unrated"
    return res


def get_genres(google, apple):
    genres = []
    if not is_nan(google):
        genres_google = google.split(';')
        for g in genres_google:
            if not is_nan(g):
                genres.append(g)
    if not is_nan(apple):
        genres.append(apple)
    return genres


def get_n_rating(google, apple):
    n_rating = {}
    total = 0.0
    if not is_nan(google):
        if not google[-1].isdigit():
            unit = google[-1].lower()
            if unit == 'm':
                google = float(google[:-1]) * 1000000
            else:
                raise Exception('Otra unidad en get_n_rating')
        else:
            google = float(google)
        n_rating['google_play'] = google
        total += google
    if not is_nan(apple):
        apple = float(apple)
        n_rating['app_store'] = apple
        total += apple
    if total != 0.0:
        n_rating['total'] = total
    else:
        n_rating = None
    return n_rating


def get_user_rating(google, apple):
    rating = {}
    total = 0.0
    divisor = 0.0
    if not is_nan(google):
        google = float(google)
        rating['google_play'] = google
        total += google
        divisor += 1.0
    if not is_nan(apple):
        apple = float(apple)
        rating['app_store'] = apple
        total += apple
        divisor += 1.0
    if total != 0.0:
        rating['total_average'] = total / divisor
    else:
        rating = None
    return rating


def get_price(google, apple):
    price = {}
    de_pago = False
    if not is_nan(google):
        if google == 'Everyone':
            google = 0.0
        else:
            google = float(google)
        if google > 0.0:
            de_pago = True
        price['google_play'] = google
    if not is_nan(apple):
        apple = float(apple)
        if apple > 0.0:
            de_pago = True
        price['app_store'] = apple
    return price, de_pago


def get_availability(google, apple):
    available = {'google_play': False, 'app_store': False}
    if not is_nan(google):
        available['google_play'] = True
    if not is_nan(apple):
        available['app_store'] = True
    return available