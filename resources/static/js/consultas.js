// Lista para mostrar y ocultar dinammicamente zonas de la pagina
let listaDivs = ['chart', 'chart2', 'estadisticas', 'basicasSinParametros', 'basicasConParametros', 'avanzadasSinParametros'];
//Distincion de consultas especiales para las graficas
let tipoAvanzadasConDosBarras = [6, 7, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25];
let tipoAvanzadasConDosDonuts = [15, 19];
let tipoAvanzadasConUnDonuts = [20, 21];
let tipoBasicasConDoshistogramas = [0, 1, 2, 3];
// Textos para los histogramas
let columnasPrecio = ["Gratuita", "(0$, 1$]", "(1$, 2$]", "(2$, 5$]", "(5$, 10$]", "(10$, +)"];
let columnasSize = ["(0MB, 10MB]", "(10MB, 50MB]", "(50MB, 100 MB]", "(100MB, +)"];
let columansNRating = ["(0, 1K]", "(1K, 50K]", "(50K, 100K]", "(100K, 1M]", "(1M, +)"];
let columnasRating = ["Unrated", "[1, 2)", "[2, 3)", "[3, 4)", "[4, 5)", "[5, 5]"];

//Consultas del sistema

function verEstadisticas() {
    let url = "/datosII/estadisticasSistema";
    $('#loader').show();
    $.ajax({
        url: url,
        type: 'GET',
        success: function (res) {
            $('#avanzadasConParamtros').hide();
            $('#estadisticas').html(res);
            mostrar("estadisticas", "estadisticaNombre");
        },
        error: function (res) {
            $('#loader').hide();
            alert("Error la conexión para comprobar la conexión.");
        }
    });
}

function consultaBasica(conParametros, tipo, titulo) {
    let url = "/datosII/basica";
    $('#loader').show();
    $.ajax({
        url: url,
        type: 'GET',
        data: {
            tipo: tipo,
            offset: 1
        },
        success: function (res) {
            $('#avanzadasConParamtros').hide();
            if (tipoBasicasConDoshistogramas.includes(tipo)) {
                crearDosGraficas(res['res'], 'bar', true, titulo, tipo);
            }
        },
        error: function (res) {
            $('#loader').hide();
            alert("Error la conexión para comprobar la conexión.");
        }
    });
}

function consultaAvanzada(tipo, titulo) {
    let url = "/datosII/avanzada";
    $('#loader').show();
    $.ajax({
        url: url,
        type: 'GET',
        data: {
            tipo: tipo,
            offset: 1
        },
        success: function (res) {
            $('#avanzadasConParamtros').hide();
            if (tipoAvanzadasConDosDonuts.includes(tipo)) {
                crearDosGraficas(res['res'], 'donut', false, titulo, tipo);
            } else if (tipoAvanzadasConDosBarras.includes(tipo)) {
                crearDosGraficas(res['res'], 'bar', false, titulo, tipo);
            } else if (tipoAvanzadasConUnDonuts.includes(tipo)) {
                crearGrafica(res['res'], 'donut', titulo);
            } else {
                crearGrafica(res['res'], 'bar', titulo);
            }
        },
        error: function (res) {
            $('#loader').hide();
            alert("Error la conexión para comprobar la conexión.");
        }
    });
}

function cargaGraficaContentRating(e) {
    let url = "/datosII/avanzada";
    $('#loader').show();
    let tipo = $('#consulta').val();
    $.ajax({
        url: url,
        type: 'GET',
        data: {
            tipo: tipo,
            contentRating: e
        },
        success: function (res) {
            crearDosGraficas(res['res'], 'bar', false, $('#consultaText').val(), tipo);
        },
        error: function (res) {
            $('#loader').hide();
            alert("Error la conexión para comprobar la conexión.");
        }
    });
}


function consultaAvanzadaConParametros(iden, text) {
    $('#estadisticaNombre').hide();
    $('#graficaNombre').show();
    $('#avanzadasConParamtros').show();
    ocultarResto("", "");
    $('#consulta').val(iden);
    $('#consultaText').val(text);
}

//Metodos principales para crear graficas

function crearGrafica(res, tipo, titulo) {
    let values;
    if (tipo === "donut") {
        values = obtenerListaGraficaUnDonuts(res);
    } else {
        values = obtenerListaGrafica(res);
    }
    dibujarUnaGrafica(values, tipo, titulo);
    mostrar('chart');
}

function crearDosGraficas(res, tipo, esHistograma, titulo, tipoHistograma) {
    let values;
    if (esHistograma) {
        values = obtenerListaGraficaDosHistogramas(res, tipoHistograma);
        let labels = obtenerLabels(tipoHistograma);
        dibujarDosHistogramas(values[0], values[1], labels, titulo);
    } else {
        values = obtenerListaGraficaDosDonuts(res);
        dibujarDosGraficas(values[0], values[1], tipo, titulo);
    }
    mostrar('chart', 'chart2');
}

// Mostrar y ocultar elementos dinamicamente

function mostrar(id, id2) {
    $('#' + id).show();
    $('#' + id2).show();
    if (id2 !== 'estadisticaNombre') {
        $('#estadisticaNombre').hide();
         $('#graficaNombre').show();
    } else {
        $('#graficaNombre').hide();
         $('#estadisticaNombre').hide();
    }
    ocultarResto(id, id2);
}


function ocultarResto(id, id2) {
    for (let i = 0; i < listaDivs.length; i++) {
        if (listaDivs[i] !== id && listaDivs[i] !== id2) {
            $('#' + listaDivs[i]).hide();
        }
    }
    $('#loader').hide();
}