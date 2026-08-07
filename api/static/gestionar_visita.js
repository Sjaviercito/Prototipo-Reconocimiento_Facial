let idOperador = null;
let contador = null;
let guardarId = null;
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
    contador = 10;
    guardarId = setInterval(contadorFichajes, 1000)
}

async function ficharVisitante() {
    const formData = new FormData();
    formData.append('id_operador', idOperador);

    const respuesta = await fetch('/gestionar-visita/procesar', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + token },
        body: formData
    });
    if (respuesta.status === 401) {
        manejarNoAutorizado();
        return;
    }

    const datos = await respuesta.json();
    const resultado = document.getElementById('resultado');
    if (!respuesta.ok) {
        if (respuesta.status === 404){
            return
        }
        else{
            if (datos.detail.token){
            window.open(`/ver-qr/${datos.detail.token}`, '_blank')
            return;
        }
        resultado.textContent = datos.detail || 'Error al fichar';
        return;
        } 
    }
    if (datos.tipo === "cooldown"){
        return
    }else{
        resultado.textContent = `${datos.tipo.toUpperCase()}: ${datos.nombre} (visita ${datos.id_visita})`;
    }
    
}
async function cerrarSesion(){
    const formData = new FormData();
    formData.append('id_operador', idOperador);
    const respuesta = await fetch('/gestionar-visita/logout-operador', {
        method: 'POST',
        headers: {'Authorization': 'Bearer ' + token},
        body: formData
    });
    if (respuesta.status === 401) {
        manejarNoAutorizado();
        return;
    }
    const datos = await respuesta.json();
    if (respuesta.ok) {
        idOperador = null;
        document.getElementById('seccion-fichaje').style.display = 'none';
        document.getElementById('seccion-login').style.display = 'block';
        document.getElementById('pin').value = '';
        clearInterval(guardarId)
    }
    else{
        alert(datos.detail || 'No se pudo verificar tu identidad')
       
        }
    }

function contadorFichajes(){
    contador = contador -1;
    const resultado = document.getElementById('contador-fichajes')
    resultado.textContent = `${contador}`
    if (contador == 0){
        ficharVisitante()
        contador = 10;
    }
}
window.loginOperador = loginOperador;
window.ficharVisitante = ficharVisitante;
window.cerrarSesion = cerrarSesion;