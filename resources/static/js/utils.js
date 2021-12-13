// Listas histograma
function obtenerListaGrafica(res) {
    let values = [];
    Object.keys(res).forEach(function (key) {
        let clave = key;
        if (clave === null) {
            clave = "Unrated";
        }
        values.push([clave, res[key]]);
    });
    return values;
}

function obtenerListaGraficaUnDonuts(res) {
    let values = [];
    for (let i = 0; i < res.length; i++) {
        let jsonActual = res[i];
        let keys = [];
        Object.keys(jsonActual).forEach(function (key) {
            keys.push(key);
        });
        let tipo = jsonActual[keys[0]];
        if (tipo === null) {
            tipo = "Unrated";
        }
        values.push([tipo, jsonActual[keys[1]]]);
    }
    return values;
}

function obtenerListaGraficaDosDonuts(res) {
    let values = [];
    let apple = [];
    let google = [];
    for (let i = 0; i < res.length; i++) {
        let jsonActual = res[i];
        let keys = [];
        Object.keys(jsonActual).forEach(function (key) {
            keys.push(key);
        });
        let tipo = jsonActual[keys[0]];
        if (tipo === null) {
            tipo = "Unrated";
        }
        let app_store = jsonActual[keys[1]];
        let google_play = jsonActual[keys[2]];
        if (app_store !== null && app_store > 0) {
            apple.push([tipo, app_store]);
        }
        if (google_play !== null && google_play > 0) {
            google.push([tipo, google_play]);
        }
    }
    values.push(apple);
    values.push(google);
    return values;
}

function obtenerListaGraficaDosHistogramas(res, tipo) {
    let values = [];
    let keys = [];
    Object.keys(res).forEach(function (key) {
        keys.push(key);
    });
    let google, apple;
    if (tipo === 0) {
        apple = filtrarPorPrecio(res[keys[0]]);
        google = filtrarPorPrecio(res[keys[1]]);
    } else if (tipo === 1) {
        apple = filtrarPorSize(res[keys[0]]);
        google = filtrarPorSize(res[keys[1]]);
    } else if (tipo === 2) {
        apple = filtrarPorRating(res[keys[0]]);
        google = filtrarPorRating(res[keys[1]]);
    } else {
        apple = filtrarPorNRating(res[keys[0]]);
        google = filtrarPorNRating(res[keys[1]]);
    }
    values.push(apple);
    values.push(google);
    return values;
}

// Filtrados para los histogramas

function filtrarPorPrecio(valores) {
    let resLista = [];
    let gratuita = 0;
    let uno = 0;
    let dos = 0;
    let cinco = 0;
    let diez = 0;
    let mas = 0;
    for (let i = 0; i < valores.length; i++) {
        let valor = valores[i];
        if (valor === null || valor === 0) {
            gratuita++;
        } else if (valor < 1) {
            uno++;
        } else if (valor < 2) {
            dos++;
        } else if (valor < 5) {
            cinco++;
        } else if (valor < 10) {
            diez++;
        } else {
            mas++;
        }
    }
    resLista.push("Precio");
    resLista.push(gratuita);
    resLista.push(uno);
    resLista.push(dos);
    resLista.push(cinco);
    resLista.push(diez);
    resLista.push(mas);
    return resLista;
}


function filtrarPorSize(valores) {
    let resLista = [];
    let poco = 0;
    let medio = 0;
    let grande = 0;
    let muyGrande = 0;
    for (let i = 0; i < valores.length; i++) {
        let valor = valores[i];
        if (valor === null || valor < 10) {
            poco++;
        } else if (valor < 50) {
            medio++;
        } else if (valor < 100) {
            grande++;
        } else if (valor > 100) {
            muyGrande++;
        }
    }
    resLista.push("Size");
    resLista.push(poco);
    resLista.push(medio);
    resLista.push(grande);
    resLista.push(muyGrande);
    return resLista;
}

function filtrarPorNRating(valores) {
    let resLista = [];
    let uno = 0;
    let cincuenta = 0;
    let cien = 0;
    let unoMenos = 0;
    let unoMas = 0;

    for (let val of valores) {
        if (val < 1000) {
            uno++;
        } else if (val < 50000) {
            cincuenta++;
        } else if (val < 100000) {
            cien++;
        } else if (val < 1000000) {
            unoMenos++;
        } else {
            unoMas++;
        }
    }
    resLista.push("N-Rating");
    resLista.push(uno);
    resLista.push(cincuenta);
    resLista.push(cien);
    resLista.push(unoMenos);
    resLista.push(unoMas);
    return resLista;
}

function filtrarPorRating(valores) {
    let resLista = [];
    let unrated = 0;
    let uno = 0;
    let dos = 0;
    let tres = 0;
    let cuatro = 0;
    let cinco = 0;

    for (let val of valores) {
        if (val === null || val.toString().toLowerCase() === "unrated") {
            unrated++;
        } else if (val >= 1 && val < 2) {
            uno++;
        } else if (val >= 2 && val < 3) {
            dos++;
        } else if (val >= 3 && val < 4) {
            tres++;
        } else if (val >= 4 && val < 5) {
            cuatro++;
        } else {
            cinco++;
        }
    }
    resLista.push("Rating")
    resLista.push(unrated);
    resLista.push(uno);
    resLista.push(dos);
    resLista.push(tres);
    resLista.push(cuatro);
    resLista.push(cinco);
    return resLista;
}

function obtenerLabels(tipoHistograma) {
    let labels = [];
    if (tipoHistograma === 0) {
        labels.push("Precio");
        labels.push(columnasPrecio);
    } else if (tipoHistograma === 1) {
        labels.push("Tamaño");
        labels.push(columnasSize);
    } else if (tipoHistograma === 2) {
        labels.push("Valoración del usuario");
        labels.push(columnasRating);
    } else {
        labels.push("Número de valoraciones");
        labels.push(columansNRating);
    }
    labels.push("Número de aplicaciones");
    return labels;
}
