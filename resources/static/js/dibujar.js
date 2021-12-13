//Dibujar graficas

function dibujarDosHistogramas(apple, google, labels, titulo) {
    var apple_chart = c3.generate({
        bindto: '#chart',
        data: {
            columns: [
                apple
            ],
            type: 'bar'
        },
        axis: {
            x: {
                label: {
                    text: labels[0],
                    position: 'outer-center',
                },
                type: 'category',
                categories: labels[1],
                tick: {
                    centered: true
                }
            },
            y: {
                label: {
                    text: labels[2],
                    position: 'outer-middle'
                },
                min: 0,
                padding: {
                    top: 0,
                    bottom: 0
                }
            }
        },
        legend: {
            show: false
        }, title: {
            text: titulo + " - Apple"
        }
    });
    var google_chart = c3.generate({
        bindto: '#chart2',
        data: {
            columns: [
                google
            ],
            type: 'bar'
        },
        axis: {
            x: {
                label: {
                    text: labels[0],
                    position: 'outer-center',
                },
                type: 'category',
                categories: labels[1],
                tick: {
                    centered: true
                }
            },
            y: {
                label: {
                    text: labels[2],
                    position: 'outer-middle'
                },
                min: 0,
                padding: {
                    top: 0,
                    bottom: 0
                }
            }
        },
        legend: {
            show: false
        }, title: {
            text: titulo + " - Google"
        }
    });
    setTimeout(function () {
        google_chart.resize();
    }, 200);
    setTimeout(function () {
        apple_chart.resize();
    }, 200);
}

function dibujarDosGraficas(apple, google, tipo, titulo) {
    if(apple.length>0){
      var apple_chart = c3.generate({
        bindto: '#chart',
        data: {
            columns: [
                apple[0]
            ],
            type: tipo,
            onclick: function (d, i) {
            },
            onmouseover: function (d, i) {
            },
            onmouseout: function (d, i) {
            }
        },
        donut: {
            title: "Apple Chart"
        }, title: {
            text: titulo + " - Apple"
        },
        zoom: {
            enabled: true
        }
        });
      for (let i = 1; i < apple.length; i++) {
        apple_chart.load({
            columns: [apple[i]]
        });
        }
       setTimeout(function () {
        apple_chart.resize();
    }, 200);
    }
    if(google.length>0) {
        var google_chart = c3.generate({
            bindto: '#chart2',
            data: {
                columns: [
                    google[0]
                ],
                type: tipo,
                onclick: function (d, i) {
                },
                onmouseover: function (d, i) {
                },
                onmouseout: function (d, i) {
                }
            },
            donut: {
                title: "Google Chart"
            },
            title: {
                text: titulo + " - Google"
            },
            zoom: {
                enabled: true
            }
        });

        for (let i = 1; i < google.length; i++) {
            google_chart.load({
                columns: [google[i]]
            });
        }
        setTimeout(function () {
        google_chart.resize();
    }, 200);
    }
}

function dibujarUnaGrafica(values, tipo, titulo) {
    var chart = c3.generate({
        bindto: '#chart',
        data: {
            columns: [
                values[0]
            ],
            type: tipo
        },
        bar: {
            width: {
                ratio: 0.5
            }
        },
        title: {
            text: titulo
        }
    });
    for (let i = 1; i < values.length; i++) {
        chart.load({
            columns: [values[i]]
        });
    }
    setTimeout(function () {
        chart.resize();
    }, 200);
}