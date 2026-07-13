const token = localStorage.getItem('token');
const rolUsuario = localStorage.getItem('rol');

let rostrosCapturados = 0;

if (!token) {
    window.location.href = '/login-page';
}

if (rolUsuario !== "admin") {
    alert("Solo admin puede acceder al setup de operadores.");
    window.location.href = '/';
}

function mostrarMensaje(texto) {
    document.getElementById('mensaje').textContent = texto;
}

function obtenerNombre() {
    return document.getElementById('nombre').value.trim();
}

async function iniciarCamara() {
    const respuesta = await fetch('/setup/operadores/camara/iniciar', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + token
        }
    });

    const datos = await respuesta.json();

    if (respuesta.ok) {
    rostrosCapturados = 0;

    document.getElementById('contador-rostros').textContent = 'Rostros capturados: 0/5';
    document.getElementById('boton-tomar-rostro').disabled = false;

    mostrarMensaje(datos.mensaje);
} else {
    mostrarMensaje(datos.detail || 'Error al iniciar cámara');
}
}

async function tomarRostro() {
    const nombre = obtenerNombre();

    if (!nombre) {
        mostrarMensaje("Primero escribe el nombre del operador.");
        return;
    }

    const formData = new FormData();
    formData.append('nombre_operador', nombre);

    const respuesta = await fetch('/setup/operadores/camara/rostro', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + token
        },
        body: formData
    });

    const datos = await respuesta.json();

    if (respuesta.ok) {
    rostrosCapturados = datos.contador;

    document.getElementById('contador-rostros').textContent =
        `Rostros capturados: ${rostrosCapturados}/5`;

    mostrarMensaje(datos.mensaje);

    if (datos.completo === true) {
    document.getElementById('boton-tomar-rostro').disabled = true;
    mostrarMensaje("Fotos tomadas correctamente. Ya puedes registrar el operador.");
}
} else {
    mostrarMensaje(datos.detail || 'Error al tomar rostro');
}
}

async function cancelarCamara() {
    const respuesta = await fetch('/setup/operadores/camara/cancelar', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + token
        }
    });

    const datos = await respuesta.json();

    rostrosCapturados = 0;
    document.getElementById('contador-rostros').textContent = 'Rostros capturados: 0/5';
    document.getElementById('boton-tomar-rostro').disabled = false;

    mostrarMensaje(datos.mensaje || 'Captura cancelada');
}

async function registrarOperador() {
    const nombre = document.getElementById('nombre').value.trim();
    const username = document.getElementById('username').value.trim();
    const correo = document.getElementById('correo').value.trim();
    const rol = document.getElementById('rol').value;
    const password = document.getElementById('password').value;
    const pin = document.getElementById('pin').value;

    if (!nombre || !username || !correo || !rol || !password || !pin) {
        mostrarMensaje("Completa todos los campos.");
        return;
    }

    if (rostrosCapturados < 5) {
        mostrarMensaje("Debes capturar 5 fotos de rostro.");
        return;
    }

    const formData = new FormData();
    formData.append('nombre', nombre);
    formData.append('username', username);
    formData.append('correo', correo);
    formData.append('rol', rol);
    formData.append('password', password);
    formData.append('pin', pin);

    const respuesta = await fetch('/setup/operadores/registrar', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + token
        },
        body: formData
    });

    const datos = await respuesta.json();

    if (respuesta.ok) {
        mostrarMensaje(datos.mensaje + " ID: " + datos.id_usuario);

        document.getElementById('nombre').value = '';
        document.getElementById('username').value = '';
        document.getElementById('correo').value = '';
        document.getElementById('password').value = '';
        document.getElementById('pin').value = '';

        rostrosCapturados = 0;
        document.getElementById('contador-rostros').textContent = 'Rostros capturados: 0/5';
        document.getElementById('boton-tomar-rostro').disabled = false;
    } else {
        mostrarMensaje(datos.detail || 'Error al registrar operador');
    }
}


window.iniciarCamara = iniciarCamara;
window.tomarRostro = tomarRostro;
window.cancelarCamara = cancelarCamara;
window.registrarOperador = registrarOperador;

console.log("setup_operadores.js cargado correctamente");
console.log("tomarRostro:", typeof tomarRostro);