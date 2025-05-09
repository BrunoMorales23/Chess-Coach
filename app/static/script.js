setInterval(() => {
    const timestamp = Date.now();
    const filename = `ss_${timestamp}.webp`;

    fetch('/dynamic-index', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename: filename })
    })
    .then(() => {
        console.log("POST Primer paso done! Nombre de Archivo generado:", filename);

        return fetch('/dynamic-index', {
            method: 'GET'
        });
    })
    .then(response => response.json())
    .then(data => {
        console.log("GET Segundo paso done! Nombre del archivo recibido del backend:", data.filename);

        const img = document.getElementById('live-image');
        img.src = data.filename;

        console.log("Tablero actualizado!")

        return fetch('/dynamic-index', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: filename })
        });
    })
    .then(() => {
        console.log("DELETE Tercer paso done!, Ciclo completo realizado!");
    })
    .catch(error => {
        console.error("Error en alguna parte del ciclo:", error);
    });
}, 3000);