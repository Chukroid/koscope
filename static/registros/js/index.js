document.addEventListener("DOMContentLoaded", function () {
    const inputs = document.querySelectorAll('.form-seperator p input');
    const selects = document.querySelectorAll('.form-seperator p select');
    const inputFiles = document.querySelectorAll('.form-seperator p input[type=file]');

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
})