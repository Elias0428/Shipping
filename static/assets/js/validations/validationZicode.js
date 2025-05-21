document.getElementById('zipcode').addEventListener('input', function() {
    const zipcode = this.value.trim(); // Elimina espacios en blanco
    if (zipcode.length === 5) { // Solo buscar cuando tenga 5 dígitos
        // 1️⃣ Consultar Zippopotam para obtener ciudad, estado y coordenadas
        fetch(`/api/zipcode/${zipcode}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("ZIP Code no encontrado");
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('city').value = data.city;
                document.getElementById('state').value = data.state;    
            })
    } else {
        limpiarCampos(); // Limpiar cuando el usuario borra los números
    }
});

// Función para limpiar los campos
function limpiarCampos() {
    document.getElementById('city').value = "";
    document.getElementById('state').value = "";
}
