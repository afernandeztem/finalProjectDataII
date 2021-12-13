from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required

import mongo.repository.app_repository as app

datos_ii_bp = Blueprint('datos_II', __name__, template_folder='templates')


# @datos_ii_bp.route("/consultasAvanzadasContentRating", methods=['GET'])
# @login_required
# def consultas_avanzadas_content_rating():
#     return jsonify({'res': app.get_all_content_ratings()})


@datos_ii_bp.route("/estadisticasSistema", methods=['GET'])
@login_required
def estadistica_sistema():
    apps = app.get_numero_aplicaciones()
    apps_app_store = app.get_numero_aplicaciones_app_store()
    apps_google_play = app.get_numero_aplicaciones_google_play()
    apps_coindicentes = app.get_numero_aplicaciones_coincidentes()
    apps_gratuitas = app.get_numero_aplicaciones_gratuitas()
    apps_pago = app.get_numero_aplicaciones_pago()
    apps_gratuitas_gp = app.get_numero_aplicaciones_gratuitas_google_play()
    apps_pago_gp = app.get_numero_aplicaciones_pago_google_play()
    apps_gratuitas_ap = app.get_numero_aplicaciones_gratuitas_app_store()
    apps_pago_ap = app.get_numero_aplicaciones_pago_app_store()
    apps_gratuitas_co = app.get_numero_aplicaciones_gratuitas_coincidentes()
    apps_pago_co = app.get_numero_aplicaciones_pago_coincidentes()
    return render_template("estadisticasSistema.html", apps=apps, apps_app_store=apps_app_store,
                           apps_google_play=apps_google_play, apps_coindicentes=apps_coindicentes,
                           apps_gratuitas=apps_gratuitas, apps_pago=apps_pago, apps_gratuitas_gp=apps_gratuitas_gp,
                           apps_pago_gp=apps_pago_gp, apps_gratuitas_ap=apps_gratuitas_ap, apps_pago_ap=apps_pago_ap,
                           apps_gratuitas_co=apps_gratuitas_co, apps_pago_co=apps_pago_co)


@datos_ii_bp.route("/basica", methods=['GET'])
@login_required
def consulas_basicas_sin_parametros():
    tipo = int(request.values.get('tipo'))
    offset = int(request.values.get('offset'))
    if tipo == 0:
        res = app.get_precio()
    elif tipo == 1:
        res = app.get_size()
    elif tipo == 2:
        res = app.get_rating()
    elif tipo == 3:
        res = app.get_n_rating()
    elif tipo == 6:
        res = app.get_aplicaciones_rating_descendente()
    elif tipo == 7:
        res = app.get_aplicaciones_rating_descendente_app_store()
    elif tipo == 8:
        res = app.get_aplicaciones_rating_descendente_google_play()
    elif tipo == 9:
        res = app.get_aplicaciones_price_descendente_app_store()
    else:
        res = app.get_aplicaciones_price_descendente_google_play()
    return jsonify({'res': res})


@datos_ii_bp.route("/avanzada", methods=['GET'])
@login_required
def consulas_avanzadas():
    tipo = int(request.values.get('tipo'))
    content_rating = None
    if 21 < tipo < 26:
        content_rating = request.values.get('contentRating')
    if tipo == 0:
        res = app.get_precio_medio_aplicaciones(False)
    elif tipo == 1:
        res = app.get_precio_medio_aplicaciones(True)
    elif tipo == 2:
        res = app.get_precio_medio_aplicaciones_pago(False)
    elif tipo == 3:
        res = app.get_precio_medio_aplicaciones_pago(True)
    elif tipo == 4:
        res = app.get_precio_medio_aplicaciones_coincidentes()
    elif tipo == 5:
        res = app.get_precio_medio_aplicaciones_pago_coincidentes()
    elif tipo == 6:
        res = app.get_precio_medio_aplicaciones_por_generos(False)
    elif tipo == 7:
        res = app.get_precio_medio_aplicaciones_por_generos(True)
    elif tipo == 8:
        res = app.get_size_medio_aplicaciones()
    elif tipo == 9:
        res = app.get_size_medio_aplicaciones_coincidentes()
    elif tipo == 10:
        res = app.get_numero_ratings_medio_aplicaciones()
    elif tipo == 11:
        res = app.get_numero_ratings_medio_aplicaciones_coincidentes()
    elif tipo == 12:
        res = app.get_ratings_medio_aplicaciones()
    elif tipo == 13:
        res = app.get_ratings_medio_aplicaciones_coincidentes()
    elif tipo == 14:
        res = app.get_ratings_medio_aplicaciones_por_genero()
    elif tipo == 15:
        res = app.get_numero_ratings_medio_aplicaciones_por_genero()
    elif tipo == 16:
        res = app.get_precio_medio_aplicaciones_por_content_rating(False)
    elif tipo == 17:
        res = app.get_precio_medio_aplicaciones_por_content_rating(True)
    elif tipo == 18:
        res = app.get_ratings_medio_aplicaciones_por_content_rating()
    elif tipo == 19:
        res = app.get_numero_ratings_medio_aplicaciones_por_content_rating()
    elif tipo == 20:
        res = app.get_numero_aplicaciones_por_content_rating()
    elif tipo == 22:
        res = app.get_precio_medio_aplicaciones_por_genero_un_content_rating(content_rating)
    elif tipo == 23:
        res = app.get_size_medio_aplicaciones_por_genero_un_content_rating(content_rating)
    elif tipo == 24:
        res = app.get_numero_ratings_medio_aplicaciones_por_genero_un_content_rating(content_rating)
    elif tipo == 25:
        res = app.get_ratings_medio_aplicaciones_por_genero_un_content_rating(content_rating)
    else:
        res = app.get_numero_aplicaciones_por_genero()
    return jsonify({'res': res})
