document.addEventListener("DOMContentLoaded", function () {
    const inputs = document.querySelectorAll('.form-seperator p input');
    const selects = document.querySelectorAll('.form-seperator p select');
    const inputFiles = document.querySelectorAll('.form-seperator p input[type=file]');

    const descargarCredencial = document.getElementById("credencial-descargar");
    const credencialVista = document.getElementsByClassName("credencial")[0];

    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.classList.add('focused');
        });
        input.addEventListener('blur', () => {
            if (input.value !== '') {
                input.parentElement.classList.add('focused');
            } else {
                input.parentElement.classList.remove('focused');
            }
        });
    });

    selects.forEach(select => {
        select.previousElementSibling.style.display = 'none';
    });
    inputFiles.forEach(inputfile => {
        inputfile.previousElementSibling.style.display = 'none';
    });

    descargarCredencial.addEventListener("click", (e) => {
        e.preventDefault();

        html2canvas(credencialVista, {
            scale: 2, // Increases quality
            useCORS: true // Enables cross-origin images (if needed)
          }).then(canvas => {
            const link = document.createElement('a');
            link.download = 'credencial.png';
            link.href = canvas.toDataURL();
            link.click();
          });
    })
})