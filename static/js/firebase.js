// Configuración de Firebase
const firebaseConfig = {
    apiKey: "AIzaSyDI8o3e4SQ7443IgAenULNo289yWkaEn5M",
    authDomain: "flask-firebase-auth-ad9fd.firebaseapp.com",
    projectId: "flask-firebase-auth-ad9fd",
    storageBucket: "flask-firebase-auth-ad9fd.appspot.com",
    messagingSenderId: "1050060206485",
    appId: "1:1050060206485:web:575fca153faa5a9d19c69c"
};

// Inicializar Firebase
firebase.initializeApp(firebaseConfig);

const auth = firebase.auth();

function loginWithGoogle() {
    pantallaCarga()
    const provider = new firebase.auth.GoogleAuthProvider();
    auth.signInWithPopup(provider).then((result) => {
        // Obtener el token del usuario
        result.user.getIdToken().then((idToken) => {
            // Enviar el token al servidor Flask
            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ idToken })
            }).then(response => response.json())
                .then(data => {
                    if (data.success) {
                        //alert('Login successful!');
                        window.location.href = '/panel';
                    } else {
                        alert('Login failed!');
                        pantallaCarga()
                    }
                });
        });
    }).catch((error) => {
        console.error(error);
    });
}