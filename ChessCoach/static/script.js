document.getElementById("showpass").addEventListener("change", function() {
    if (this.checked) {
        document.getElementById("passinput").setAttribute("type","text");
        document.getElementById("passconfirminput").setAttribute("type","text");
    } else {
        document.getElementById("passinput").setAttribute("type","password");
        document.getElementById("passconfirminput").setAttribute("type","password");
    }
});
