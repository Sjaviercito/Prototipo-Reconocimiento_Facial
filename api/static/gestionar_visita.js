let idOperador = null;

async function loginOperador() {
    const pin = document.getElementById('pin').value.trim();
    if (!pin) { alert('Escribe el PIN'); return; }

    const formData = new FormData();
    formData.append('pin', pin);

    const respuesta = await fetch('/gestionar-visita/login-operador', {
        method: 'POST',
        body: formData
    });

    const datos = await respuesta.json();
    if (!respuesta.ok) {
        alert(datos.detail || 'Error en login');
        return;
    }

    // login ok: guardar operador y cambiar de estado
    idOperador = datos.id_operador;
    document.getElementById('nombre-operador').textContent = datos.nombre;
    document.getElementById('seccion-login').style.display = 'none';
    document.getElementById('seccion-fichaje').style.display = 'block';
}

async function ficharVisitante() {
    const formData = new FormData();
    formData.append('id_operador', idOperador);

    const respuesta = await fetch('/gestionar-visita/procesar', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + token },
        body: formData
    });

    const datos = await respuesta.json();
    const resultado = document.getElementById('resultado');

    if (!respuesta.ok) {
        if (datos.detail.token){
            window.open(`/ver-qr/${datos.detail.token}`, '_blank')
            return;
        }
        resultado.textContent = datos.detail || 'Error al fichar';
        return;
    }

    resultado.textContent = `${datos.tipo.toUpperCase()}: ${datos.nombre} (visita ${datos.id_visita})`;
}

function cerrarSesion() {
    idOperador = null;
    document.getElementById('seccion-fichaje').style.display = 'none';
    document.getElementById('seccion-login').style.display = 'block';
    document.getElementById('pin').value = '';
}

window.loginOperador = loginOperador;
window.ficharVisitante = ficharVisitante;
window.cerrarSesion = cerrarSesion;