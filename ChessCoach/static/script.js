document.getElementById("showpass").addEventListener("change", function() {
    if (this.checked) {
        document.getElementById("passinput").setAttribute("type","text");
        document.getElementById("passconfirminput").setAttribute("type","text");
    } else {
        document.getElementById("passinput").setAttribute("type","password");
        document.getElementById("passconfirminput").setAttribute("type","password");
    }
});

function handleFormError(message, inputId) {
    console.log("Error:", message);
    console.log(inputId)

    switch (inputId){
        case "id_email":
            document.getElementById("emailHelp").classList.add("d-none");
            document.getElementById("emailException").classList.remove("d-none");
            document.getElementById("emailInput").classList.add("alert", "alert-danger");
            break;
        case "id_username":
            document.getElementById("userException").classList.remove("d-none");
            document.getElementById("userInput").classList.add("alert", "alert-danger");
            break;
        default:
            document.getElementById("passwordAlert").classList.remove("d-none");
            document.getElementById("passinput").classList.add("alert", "alert-danger");
            document.getElementById("passconfirminput").classList.add("alert", "alert-danger");
    }
}