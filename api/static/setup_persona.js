const rolUsuario = localStorage.getItem('rol');
let rostrosCapturados = 0;

function mostrarMensaje(texto) {
    document.getElementById('mensaje').textContent = texto;
}

function obtenerNombre() {
    return document.getElementById('nombre_persona').value.trim();
}

async function iniciarCamara() {
    const respuesta = await fetch('/setup/personas/camara/iniciar', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + token
        }
    });
    if (respuesta.status === 401) {
        manejarNoAutorizado();
        return;
    }
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
        mostrarMensaje("Primero escribe el nombre de la persona a registrar.");
        return;
    }

    const formData = new FormData();
    formData.append('nombre_persona', nombre);

    const respuesta = await fetch('/setup/personas/camara/rostro', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + token
        },
        body: formData
    });
    if (respuesta.status === 401) {
        manejarNoAutorizado();
        return;
    }
    const datos = await respuesta.json();

    if (respuesta.ok) {
    rostrosCapturados = datos.contador;

    document.getElementById('contador-rostros').textContent =
        `Rostros capturados: ${rostrosCapturados}/5`;

    mostrarMensaje(datos.mensaje);

    if (datos.completo === true) {
    document.getElementById('boton-tomar-rostro').disabled = true;
    mostrarMensaje("Fotos tomadas correctamente. Ya puedes registrar a la persona.");
}
} else {
    mostrarMensaje(datos.detail || 'Error al tomar rostro');
}
}

async function cancelarCamara() {
    const respuesta = await fetch('/setup/personas/camara/cancelar', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + token
        }
    });
    if (respuesta.status === 401) {
        manejarNoAutorizado();
        return;
    }
    const datos = await respuesta.json();

    rostrosCapturados = 0;
    document.getElementById('contador-rostros').textContent = 'Rostros capturados: 0/5';
    document.getElementById('boton-tomar-rostro').disabled = false;

    mostrarMensaje(datos.mensaje || 'Captura cancelada');
}

async function  cargarAutorizadores() {
     const respuesta = await fetch('/autorizadores', {
        headers: { 'Authorization': 'Bearer ' + token }
    });
    if (respuesta.status === 401) {
        manejarNoAutorizado();
        return;
    }
    const datos = await respuesta.json();
    const select = document.getElementById('autorizador_persona');
    select.innerHTML = '';
    for (const autorizador of datos.autorizadores) {
        const opcion = document.createElement('option');
        opcion.value = autorizador.id_autorizador;      // lo que se manda al backend
        opcion.textContent = autorizador.nombre_autorizador;  // lo que ve el operador
        select.appendChild(opcion);
    }
    
}
async function cargarDepartamentos(){
    const respuesta = await fetch('/departamentos', {
        headers: { 'Authorization': 'Bearer ' + token }
    });
    if (respuesta.status === 401) {
        manejarNoAutorizado();
        return;
    };
    const datos = await respuesta.json();
    const select = document.getElementById('nuevo-autorizador-departamento');
    select.innerHTML = '';
    for (const item of datos['departamentos']) {
    const opcion = document.createElement('option');
    opcion.value = item['id_departamento'];
    opcion.textContent = item['nombre_departamento'];
    select.appendChild(opcion);
    }

}
async function cargarOrganizaciones() {
    const tipo = document.getElementById('tipo').value;
    let url, clave, campoId, campoNombre;
    if (tipo === 'gobierno') {
    url = '/departamentos';
    clave = 'departamentos';
    campoId = 'id_departamento';
    campoNombre = 'nombre_departamento';
    } else {
    url = '/proveedores';
    clave = 'proveedores';
    campoId = 'id_proveedor';
    campoNombre = 'nombre_proveedor';
    }
    const respuesta = await fetch(url, {
        headers: { 'Authorization': 'Bearer ' + token }
    });
    if (respuesta.status === 401) {
        manejarNoAutorizado();
        return;
    }
    const datos = await respuesta.json();
    const select = document.getElementById('organizaciones');
    select.innerHTML = '';
    for (const item of datos[clave]) {
    const opcion = document.createElement('option');
    opcion.value = item[campoId];
    opcion.textContent = item[campoNombre];
    select.appendChild(opcion);
    }
}
async function registrarPersona() {
    const nombre = document.getElementById('nombre_persona').value.trim();
    const tipo = document.getElementById('tipo').value.trim();
    const telefono = document.getElementById('telefono_persona').value.trim();
    const idAutorizador = document.getElementById('autorizador_persona').value.trim();
    const correo = document.getElementById('correo_persona').value.trim();
    const organizaciones = document.getElementById('organizaciones').value.trim();

    if (!nombre || !tipo || !telefono || !idAutorizador || !correo || !organizaciones) {
        mostrarMensaje("Completa todos los campos.");
        return;
    }
    if (rostrosCapturados < 5) {
        mostrarMensaje("Debes capturar 5 fotos de rostro.");
        return;
    }
    const formData = new FormData();
    formData.append('nombre', nombre);
    formData.append('tipo', tipo);
    formData.append('telefono', telefono);
    formData.append('id_autorizador', idAutorizador);
    if (tipo === 'gobierno') {
        formData.append('id_departamento', organizaciones);
    } else {
        formData.append('id_proveedor', organizaciones);
    }
    formData.append('correo', correo);

    const respuesta = await fetch('/setup/personas/registrar', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + token
        },
        body: formData
    });
    if (respuesta.status === 401) {
        manejarNoAutorizado();
        return;
    }
    const datos = await respuesta.json();

    if (respuesta.ok) {
        mostrarMensaje(datos.mensaje + " ID: " + datos.id_persona);
        document.getElementById('nombre_persona').value = '';
        document.getElementById('tipo').value = '';
        document.getElementById('telefono_persona').value = '';
        document.getElementById('autorizador_persona').value = '';
        document.getElementById('correo_persona').value = '';
        document.getElementById('organizaciones').value = '';
        rostrosCapturados = 0;
        document.getElementById('contador-rostros').textContent = 'Rostros capturados: 0/5';
        document.getElementById('boton-tomar-rostro').disabled = false;
    } else {
        mostrarMensaje(datos.detail || 'Error al registrar persona');
    }
}

async function agregarOrganizacion(){
    const nuevaOrganizacion = document.getElementById('nueva-organizacion').value.trim();
    const tipo = document.getElementById('tipo').value.trim();
    let url;
    if(tipo === 'gobierno'){
        url = '/departamentos';
    }else{
        url = '/proveedores';
    }
    const formData = new FormData();
    formData.append('nombre', nuevaOrganizacion)
    const respuesta = await fetch(url, {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + token },
        body: formData
    });
    if (respuesta.status === 401) {
        manejarNoAutorizado();
        return;
    }
    if (respuesta.ok) {
    cargarOrganizaciones();
    alert('Organización agregada correctamente');
    document.getElementById('nueva-organizacion').value = '';
    document.getElementById('form-nueva-organizacion').style.display = 'none';
} else {
    const datos = await respuesta.json();
    alert(datos.detail || 'Error al agregar organización');
}
    }

async function mostrarNuevaOrganizacion(){
    document.getElementById('form-nueva-organizacion').style.display = 'block';
}
async function  mostrarNuevoAutorizador() {
    document.getElementById('form-nuevo-autorizador').style.display = 'block';
    
}
async function agregarAutorizador(){
    const nombre = document.getElementById('nuevo-autorizador-nombre').value.trim();
    const puesto = document.getElementById('nuevo-autorizador-puesto').value.trim();
    const departamento = document.getElementById('nuevo-autorizador-departamento').value.trim();
    const correo = document.getElementById('nuevo-autorizador-correo').value.trim();
    const telefono = document.getElementById('nuevo-autorizador-telefono').value.trim();
    
    const formData = new FormData();
    formData.append('nombre', nombre)
    formData.append('puesto', puesto)
    formData.append('id_departamento', departamento)
    formData.append('correo', correo)
    formData.append('telefono', telefono)
    
    const respuesta = await fetch('/autorizadores',{
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + token },
        body: formData
    });
    if (respuesta.status === 401) {
        manejarNoAutorizado();
        return;
    }
    if (respuesta.ok) {
    cargarAutorizadores();
    alert('Autorizador agregado correctamente');
    document.getElementById('nuevo-autorizador-nombre').value = '';
    document.getElementById('nuevo-autorizador-puesto').value = '';
    document.getElementById('nuevo-autorizador-departamento').value = '';
    document.getElementById('nuevo-autorizador-correo').value = '';
    document.getElementById('nuevo-autorizador-telefono').value = '';
    document.getElementById('form-nuevo-autorizador').style.display = 'none';
    } else {
    const datos = await respuesta.json();
    alert(datos.detail || 'Error al agregar autorizador');
}
    }


window.iniciarCamara = iniciarCamara;
window.tomarRostro = tomarRostro;
window.cancelarCamara = cancelarCamara;
window.registrarPersona = registrarPersona;
document.getElementById('tipo').addEventListener('change', cargarOrganizaciones);
console.log("setup_personas.js cargado correctamente");
console.log("tomarRostro:", typeof tomarRostro);
cargarAutorizadores();
cargarOrganizaciones();
cargarDepartamentos();
window.mostrarNuevaOrganizacion = mostrarNuevaOrganizacion;
window.agregarOrganizacion = agregarOrganizacion;
window.mostrarNuevoAutorizador = mostrarNuevoAutorizador;
window.agregarAutorizador = agregarAutorizador;