let chartscreated = {}
document.addEventListener("DOMContentLoaded", function () {
    const registroTotalEntrada = document.getElementById("registro-total-entrada")
    const registroTotalSalida = document.getElementById("registro-total-salida")
    const registroTotalChart1 = document.getElementById('registro-total-chart1').getContext('2d');
    const registroTotalChart2 = document.getElementById('registro-total-chart2').getContext('2d');

    const registroGeneroChart1 = document.getElementById('registro-genero-chart1').getContext('2d');
    const registroGeneroEntradaH = document.getElementById("registro-genero-hombre-entrada")
    const registroGeneroEntradaM = document.getElementById("registro-genero-mujer-entrada")
    const registroGeneroChart2 = document.getElementById('registro-genero-chart2').getContext('2d');
    const registroGeneroChart3 = document.getElementById('registro-genero-chart3').getContext('2d');
    const registroGeneroSalidaH = document.getElementById("registro-genero-hombre-salida")
    const registroGeneroSalidaM = document.getElementById("registro-genero-mujer-salida")
    const registroGeneroChart4 = document.getElementById('registro-genero-chart4').getContext('2d');

    const filtroBotones = document.getElementsByClassName("filtro-fecha");

    async function registros_totales(filtro){ // funcion para obtener (json) registros totales
        try {
            const res = await fetch(`/estadisticas/registro_totales/?filtro=${filtro || "d"}`);
            const data = await res.json();
            return data;
        } catch (err) {
            console.error('Error:', err);
        }
    }
    async function registro_generos(filtro){ // funcion para obtener (json) registros de generos
        try {
            const res = await fetch(`/estadisticas/registro_generos/?filtro=${filtro || "d"}`);
            const data = await res.json();
            return data;
        } catch (err) {
            console.error('Error:', err);
        }
    }

    async function updatePage(filtro){
        // elimniar todos los chats viejos
        for (const key in chartscreated){
            if (chartscreated[key]){
                chartscreated[key].destroy()
            }
        }

        
        // actualizando datos de registros totales
        const datosTotales = await registros_totales(filtro)
        const datosGeneros = await registro_generos(filtro)

        chartscreated[1] = new Chart(registroTotalChart1, {
            type: 'pie',
            data: {
                labels: ["Entradas","Salidas"],
                datasets: [{
                data: [datosTotales.total_entradas_1, datosTotales.total_salidas_1],
                backgroundColor: [
                    'rgb(54, 235, 99)',
                    'rgb(250, 255, 99)',
                ],
                hoverOffset: 4
                }]
            },
        });
        registroTotalEntrada.innerHTML = datosTotales.total_entradas_1
        registroTotalSalida.innerHTML = datosTotales.total_salidas_1
        chartscreated[2] = new Chart(registroTotalChart2, {
            type: 'line',
            data: {
                labels: Object.keys(datosTotales.entrada_lista_1),
                datasets: [{
                    label: "Entradas Registradas",
                    data: Object.values(datosTotales.entrada_lista_1),
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },{
                    label: "Salidas Registradas",
                    data: Object.values(datosTotales.salidas_lista_1),
                    fill: false,
                    borderColor: 'rgb(255, 0, 0)',
                    tension: 0.1
                }]
            },
        });

        // actualizando datos de registros de genero
        // entrada
        chartscreated[3] = new Chart(registroGeneroChart1, {
            type: 'pie',
            data: {
                labels: ["Entradas Hombre","Entradas Mujeres"],
                datasets: [{
                data: [datosGeneros.total_entradas_1, datosGeneros.total_entradas_2],
                backgroundColor: [
                    'rgb(54, 162, 235)',
                    'rgb(255, 99, 132)',
                ],
                hoverOffset: 4
                }]
            },
        });
        let total = datosGeneros.total_entradas_1 + datosGeneros.total_entradas_2
        registroGeneroEntradaH.innerHTML = ((datosGeneros.total_entradas_1 * 100)/total).toFixed(1) + "%"
        registroGeneroEntradaM.innerHTML = ((datosGeneros.total_entradas_2 * 100)/total).toFixed(1) + "%"
        chartscreated[4] = new Chart(registroGeneroChart2, {
            type: 'line',
            data: {
                labels: Object.keys(datosTotales.entrada_lista_1),
                datasets: [{
                    label: "Entradas de Hombres",
                    data: Object.values(datosGeneros.entrada_lista_1),
                    fill: false,
                    borderColor: 'rgb(0, 107, 230)',
                    tension: 0.1
                },{
                    label: "Entradas de Mujeres",
                    data: Object.values(datosGeneros.entrada_lista_2),
                    fill: false,
                    borderColor: 'rgb(255, 0, 217)',
                    tension: 0.1
                }]
            },
        });
        // salida
        chartscreated[5] = new Chart(registroGeneroChart3, {
            type: 'pie',
            data: {
                labels: ["Salidas Hombre","Salidas Mujeres"],
                datasets: [{
                data: [datosGeneros.total_salidas_1, datosGeneros.total_salidas_2],
                backgroundColor: [
                    'rgb(54, 162, 235)',
                    'rgb(255, 99, 132)',
                ],
                hoverOffset: 4
                }]
            },
        });
        total = datosGeneros.total_salidas_1 + datosGeneros.total_salidas_2
        registroGeneroSalidaH.innerHTML = ((datosGeneros.total_salidas_1 * 100)/total).toFixed(1) + "%"
        registroGeneroSalidaM.innerHTML = ((datosGeneros.total_salidas_2 * 100)/total).toFixed(1) + "%"
        chartscreated[6] = new Chart(registroGeneroChart4, {
            type: 'line',
            data: {
                labels: Object.keys(datosTotales.entrada_lista_1),
                datasets: [{
                    label: "Salidas de Hombres",
                    data: Object.values(datosGeneros.salidas_lista_1),
                    fill: false,
                    borderColor: 'rgb(0, 107, 230)',
                    tension: 0.1
                },{
                    label: "Salidas de Mujeres",
                    data: Object.values(datosGeneros.salidas_lista_2),
                    fill: false,
                    borderColor: 'rgb(255, 0, 217)',
                    tension: 0.1
                }]
            },
        });
    }
    // esperar para que pase eventos de actualizacion
    for (let boton of filtroBotones){
        boton.addEventListener("click", function(e) {
            e.preventDefault()
            let filtro = this.dataset.filtro;
            updatePage(filtro)
        })
    }
    updatePage()
})

