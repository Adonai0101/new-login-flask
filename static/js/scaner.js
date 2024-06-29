
const video = document.getElementById('qr-video');
const canvas = document.getElementById('qr-canvas');
const context = canvas.getContext('2d');

// Acceder a la cámara del dispositivo
navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
  .then(stream => {
    video.srcObject = stream;
    video.play();
    requestAnimationFrame(scanQRCode);
  })
  .catch(error => {
    console.error('No se pudo acceder a la cámara:', error);
  });

// Función para escanear el código QR
function scanQRCode() {
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
  const code = jsQR(imageData.data, imageData.width, imageData.height);
  
  var cont = 0;

  if (code) {
    cont = cont + 1;
    console.log('Contenido del código QR:', code.data);
  }
  // validacion para que lea solo una vez
  if( cont != 0){  
    pantallaCarga();
    console.log('Escaneado')

    var data = {
      'codigo' : code.data
    }

    const request = {
      method: 'POST', // Método de la solicitud
      headers: {
        'Content-Type': 'application/json', // Tipo de contenido (JSON en este caso)
      },
      body: JSON.stringify(data), // Convierte los datos a JSON y colócalos en el cuerpo de la solicitud
    };

    fetch('/scaner', request)
      .then(response => {
        if (!response.ok) {
          console.log('Esto entro al error ALV')
          window.location.href = "/scaner/error"
        }
        else{
          window.location.href = "/scaner/done";
        }

      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
  else{
    requestAnimationFrame(scanQRCode);
  }
  
}
