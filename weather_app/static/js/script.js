/**
 * Función encargada de guardar la elección del usuario en el menú
 */
function saveElection() {
    let selection = document.getElementById("menu").value;
    sessionStorage.setItem("menuElection", selection);
    showContent();
}

/**
 * Función que se encarga de decidir el contenido que se mostrará 
 * */
function showContent(){
    let electionSaved = sessionStorage.getItem("menuElection");

    let card = document.querySelectorAll(".second_card");
        card.forEach(function (second_card) {
            second_card.style.display = "none";
        });

    if(electionSaved === "flight_numberInput"){
        if(electionSaved) {
            let contentShowed = document.getElementById("second_card");
            if(contentShowed) {
                contentShowed.style.display = "block";
            }
        }

    } 
    let contents = document.querySelectorAll(".content");
    contents.forEach(function (content) {
        content.style.display = "none";
    });
    if(electionSaved) {
        let contentShowed = document.getElementById(electionSaved);
        if(contentShowed) {
            contentShowed.style.display = "block";
        }
    }
}

/**
 *  Cuando la ventana se carga completamente se llama a la
 * función showContent() y se recupera la elección del usuario 
 * para poder estar desplegando constantemente contenido dependiendo de su elección.
 */
window.onload = function() {
    showContent();
    let selection = sessionStorage.getItem("menuElection");
    if(selection) {
        document.getElementById("menu").value = selection;
    }
} 
