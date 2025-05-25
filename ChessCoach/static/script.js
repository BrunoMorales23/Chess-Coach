let intervalId = null;
let isPaused = false;

function loop() {
    setInterval(() => {
        const timestamp = Date.now();
        const filename = `ss_${timestamp}.webp`;

        fetch('/game-live', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: filename })
        })
        .then(() => {
            console.log("POST Primer paso done! Nombre de Archivo generado:", filename);

            return fetch('/game-live', {
                method: 'GET'
            });
        })
        .then(response => response.json())
        .then(data => {
            console.log("GET Segundo paso done! Nombre del archivo recibido del backend:", data.filename);

            const img = document.getElementById('live-image');
            img.src = data.filename;

            console.log("Tablero actualizado!")

            return fetch('/game-live', {
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
    },);
}

intervalId = setInterval(loop, 3500);

document.getElementById('toggle-button').addEventListener('click', () => {
    if (isPaused) {
        intervalId = setInterval(ejecutarCiclo, 3500);
        document.getElementById('toggle-button').textContent = 'Pausar';
        isPaused = false;
        console.log("Intervalo reanudado");
    } else {
        // Pausar
        clearInterval(intervalId);
        intervalId = null;
        document.getElementById('toggle-button').textContent = 'Reanudar';
        isPaused = true;
        console.log("Intervalo pausado");
    }
});