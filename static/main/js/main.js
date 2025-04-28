let notificacionHilo; // hilo para notificaciones

function notify(message,duration = 5,messagetype = "normal"){
    // primero asegurar que todo los parametros sean correcto
    if (!message){
        alert("Provide a message for the notification")
        return
    }

    const notificationContainer = document.getElementById("global-notification")
    if (messagetype == "error"){
        notificationContainer.classList.remove("not-success")
        notificationContainer.classList.add("not-error")
    }else if(messagetype == "success"){
        notificationContainer.classList.add("not-success")
        notificationContainer.classList.remove("not-error")
    }else{
        notificationContainer.classList.remove("not-success")
        notificationContainer.classList.remove("not-error")
    }
    notificationContainer.classList.add("show-not")
    notificationContainer.innerHTML = message

    // checar si hay otro hilo para cancelarlo
    if (notificacionHilo){
        clearTimeout(notificacionHilo)
    }

    notificacionHilo = setTimeout(() => {
        notificationContainer.classList.remove("show-not")
        notificationContainer.innerHTML = ""
    },duration*1000)
}