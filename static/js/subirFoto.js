
var data = {
    'foto': '',
    'fotoKey': ''
}


// Obtenemos los elementos de la imagen y el input
const imagenCargar = document.getElementById('imagen-cargar');
const inputCargar = document.getElementById('input-cargar');
// Agregamos un evento clic a la imagen
imagenCargar.addEventListener('click', function () {
    // Simulamos un clic en el input oculto
    inputCargar.click();
});

// Agregamos un evento change al input para manejar el archivo seleccionado
inputCargar.addEventListener('change', function () {
    //funcion para mostrar pantalla de carga
    pantallaCarga()

    const file = inputCargar.files[0];
    console.log(file)

    const formData = new FormData();
    formData.append("file", inputCargar.files[0]);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
        .then(response => {
            if (!response.ok) {  // Verifica si la respuesta no es OK (estado diferente de 200-299)
                console.log('Error del servidor hwhhw')
            location.reload();
            }
            return response.json();  // Solo se convierte a JSON si la respuesta es OK
        })
        .then(data => {
            // Puedes recargar la lista de imágenes después de una subida exitosa
            console.log(data);
            update(data);
        })
        .catch(error => {
            console.log('Hubo un error en la subida de la imagen');
            console.error(error);
        });
});


async function update(data) {
    console.log('usando asyn')
    const url = '/cuenta/updatefoto';

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            console.log('error en la solicitud')
        }

        const responseData = await response.json();
        // La solicitud fue exitosa, aquí puedes manejar la respuesta del servidor
        console.log('Respuesta del servidor:', responseData);
        location.reload();
    } catch (error) {
        // Hubo un error en la solicitud, aquí puedes manejar el error
        console.log('wevos pra todos')
        console.error('Error al enviar la solicitud:');
    }
}

