 /* Función encargada de resgitrar y mostrar el contenido relacionado a 
la opción elegida por el usuario en el menú */
function saveElection() {
    // Se determina la elección del usuario a través del 'value' que tiene cada opción del menú
    let selection = document.getElementById("menu").value;
    // Guarda la opción seleccionada en un 'sessionStorage'
    sessionStorage.setItem("menuElection", selection);
    // Se llama a la función 'showContent' para mostrar el contenido correspondiente
    showContent();
}

// Esta función se encarga de mostrar el contenido relacionado con la elección del usuario
function showContent(){
    let electionSaved = sessionStorage.getItem("menuElection");
    let contents = document.querySelectorAll(".content");
    // Si el contenido no esta relacionado con la elección del usuario no se muestra
    contents.forEach(function (content) {
        content.style.display = "none";
    });

    // Verifica si el usuario ya eleigió algo en el menú 
    if(electionSaved) {
        /* Si el usuario si eleigió algo en el menú muestra el contenido relacionada a la elección
        se determina si está relacionado a través del id */
        let contentShowed = document.getElementById(electionSaved);
        // Verifica si hay contenido que mostrar
        if(contentShowed) {
            contentShowed.style.display = "block";
        }
    }
}

// Esto se ejecuta cuando la página ha terminado de cargar completamente
window.onload = function() {
    // Llama a la función 'showContent' para mostrar el contenido en la página
    showContent();
    
    // Obtiene el valor guardado en 'sessionStorage'
    let selection = sessionStorage.getItem("menuElection");
    
    // Verifica si hay un valor guardado en 'selection'
    if(selection) {
        document.getElementById("menu").value = selection;
    }
}


