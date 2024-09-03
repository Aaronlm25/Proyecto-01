console.log("Conetsion etsitosa")

function saveElection() {
    let selection = document.getElementById("menu").value;
    sessionStorage.setItem("menuElection", selection);
    showContent();
}

function showContent(){
    let electionSaved = sessionStorage.getItem("menuElection");
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

window.onload = function() {
    showContent();
    let selection = sessionStorage.getItem("menuElection");
    if(selection) {
        document.getElementById("menu").value = selection;
    }
} 
