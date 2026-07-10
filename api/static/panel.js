// Al cargar: verificar que haya token, si no, mandar al login
const token = localStorage.getItem('token');
if (!token) {
    window.location.href = '/login-page';
}

async function cargarAdentro() {
    const respuesta = await fetch('/adentro', {
        headers: { 'Authorization': 'Bearer ' + token }
    });
    if (respuesta.status === 401) {
        window.location.href = '/login-page';
        return;
    }
    const datos = await respuesta.json();
    const tbody = document.getElementById('tabla-adentro');
    tbody.innerHTML = '';
    for (const visita of datos.adentro) {
        const fila = document.createElement('tr');
        fila.innerHTML = `
            <td>${visita[0]}</td>
            <td>${visita[1]}</td>
            <td>${visita[2]}</td>
            <td>${visita[3]}</td>
        `;
        tbody.appendChild(fila);
    }
}

async function cargarHistorial() {
    const respuesta = await fetch('/visitas', {
        headers: { 'Authorization': 'Bearer ' + token }
    });
    if (respuesta.status === 401) {
        window.location.href = '/login-page';
        return;
    }
    const datos = await respuesta.json();
    const tbody = document.getElementById('tabla-historial');
    tbody.innerHTML = '';
    for (const v of datos.visitas) {
        const fila = document.createElement('tr');
        fila.innerHTML = `
            <td>${v[0]}</td>
            <td>${v[1]}</td>
            <td>${v[2]}</td>
            <td>${v[3]}</td>
            <td>${v[4]}</td>
            <td>${v[5] || '—'}</td>
            <td>${v[6]}</td>
            <td>${v[7]}</td>
            <td>${v[8]}</td>
            <td>${v[9] || '—'}</td>
        `;
        tbody.appendChild(fila);
    }
}
async function cargarAuditoria() {
    const respuesta = await fetch('/auditoria', {
        headers: { 'Authorization': 'Bearer ' + token }
    });
    if (respuesta.status === 401) {
        window.location.href = '/login-page';
        return;
    }
    const datos = await respuesta.json();
    const tbody = document.getElementById('tabla-auditoria');
    tbody.innerHTML = '';
    for (const a of datos.auditoria) {
        const fila = document.createElement('tr');
        fila.innerHTML = `
            <td>${a[0]}</td>
            <td>${a[1]}</td>
            <td>${a[2]}</td>
            <td>${a[3]}</td>
            <td>${a[4]}</td>
            <td>${a[5]}</td>
            <td>${a[6]}</td>
        `;
        tbody.appendChild(fila);
    }
}
async function actualizar_todo() {
    cargarAdentro();
    cargarAuditoria();
    cargarHistorial();
    
}
function cerrarSesion() {
    localStorage.removeItem('token');
    window.location.href = '/login-page';
}
cargarAuditoria();
cargarAdentro();
cargarHistorial();