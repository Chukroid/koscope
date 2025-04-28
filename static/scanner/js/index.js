let modalHilo;
let DebounceScaneo = false;

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("scan-matricula-form");
    const input = document.getElementById("scan-matricula-form-input");
    const modoCheckbox = document.getElementById("scanner-modo");
    const modoforzado = document.getElementById("force-registro");
    const modalCloseBtn = document.getElementById("modal-close-btn")
    
    const modalContainer = document.getElementById("modal-container");
    const modalImagen = document.getElementById("modal-imagen")
    const modalNombre = document.getElementById("modal-nombre")
    const modalMatricula = document.getElementById("modal-matricula")
    const modalGenero = document.getElementById("modal-genero")
    const modalGrado = document.getElementById("modal-grado")
    const modalGrupo = document.getElementById("modal-grupo")
    const modalEntrada = document.getElementById("modal-entrada")
    const modalSalida = document.getElementById("modal-salida")
  
    modalCloseBtn.addEventListener("click",function(e) {
        if (modalHilo){
            clearTimeout(modalHilo)
        }
        modalContainer.classList.add("modal-hide")
    })
    input.addEventListener('blur', () => {
        input.focus();
      });
    form.addEventListener("submit", function (e) {
        e.preventDefault(); // prevent actual form submit
  
        const matricula = input.value.trim();

        if (DebounceScaneo){
            input.value = ""
            return;
        }
        console.log("XD")
        DebounceScaneo = true

        let k = "";
            
        if (!matricula) {
            input.value = ""
            notify("Por favor, ingrese una matrícula.",5,"error")
            setTimeout(() => {
                DebounceScaneo = false
            }, 1000);
            return;
        }
        if (modoCheckbox.checked){
            k = "registrar-salida"
        }else{
            k = "registrar-entrada"
        }

        (async () => {
            try {
                const response = await fetch(`/${k}/?matricula=${encodeURIComponent(matricula)}&forced=${encodeURIComponent(modoforzado.checked)}`);
                const data = await response.json();
                
                if (!response.ok || !data.alumno) {
                    throw new Error(data.error || "Error occured");
                }

                modalImagen.src = data.alumno.imagen_alumno
                modalNombre.innerHTML = data.alumno.apellido_paterno+(data.alumno.apellido_materno ? " "+data.alumno.apellido_materno : "")+" "+data.alumno.nombre
                modalMatricula.innerHTML = data.alumno.matricula
                modalGenero.innerHTML = data.alumno.genero
                modalGrado.innerHTML = data.alumno.grado
                modalGrupo.innerHTML = data.alumno.grupo
                if (data.alumno.EntradaRegistrada){
                    modalEntrada.classList.remove("hidden")
                    modalSalida.classList.add("hidden")
                    modalEntrada.innerHTML = `Entrada Registrada: ${data.alumno.TiempoRegistrado}`
                }else{
                    modalEntrada.classList.add("hidden")
                    modalSalida.classList.remove("hidden")
                    modalSalida.innerHTML = `Salida Registrada: ${data.alumno.TiempoRegistrado}`
                }
                modalContainer.classList.remove("modal-hide")
                notify(data.message,5,"success")
                input.value = ""
                
                // cancelando cualquer otro hilo que ya habiamos creado
                if (modalHilo){
                    clearTimeout(modalHilo)
                }

                // crear un hilo para luego cerrar el modal
                modalHilo = setTimeout(() => {
                    modalContainer.classList.add("modal-hide")
                }, 5000);
            } catch (err) {
                input.value = ""
                notify(err.message,5,"error")
            }
        })();
        setTimeout(() => {
            DebounceScaneo = false
        }, 1000);
    });
  });
  