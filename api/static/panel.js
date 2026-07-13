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
    await cargarAdentro();
    await cargarAuditoria();
    await cargarHistorial();
    await cargarReglamentoVigente();
    
}
function cerrarSesion() {
    localStorage.removeItem('token');
    window.location.href = '/login-page';
}
async function cargarReglamentoVigente() {
    const respuesta = await fetch('/reglamento-vigente', {
        headers: { 'Authorization': 'Bearer ' + token }
    });

    if (respuesta.status === 401) {
        window.location.href = '/login-page';
        return;
    }

    const datos = await respuesta.json();
    const contenedor = document.getElementById('reglamento-vigente');

    if (!datos.reglamento) {
        contenedor.innerHTML = 'No hay reglamento vigente.';
        return;
    }

    contenedor.innerHTML = `
        <p><strong>Versión:</strong> ${datos.reglamento.nombre_version}</p>
        <p><strong>Ruta PDF:</strong> ${datos.reglamento.ruta_pdf}</p>
    `;
}
const formReglamento = document.getElementById('form-reglamento');

if (formReglamento) {
    formReglamento.addEventListener('submit', async function(event) {
        event.preventDefault();

        const nombreVersion = document.getElementById('nombre-version').value;
        const archivo = document.getElementById('archivo-reglamento').files[0];
        const mensaje = document.getElementById('mensaje-reglamento');

        if (!archivo) {
            mensaje.textContent = 'Selecciona un archivo PDF.';
            return;
        }

        const formData = new FormData();
        formData.append('nombre_version', nombreVersion);
        formData.append('archivo', archivo);

        const respuesta = await fetch('/reglamentos', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            body: formData
        });

        const datos = await respuesta.json();

        if (respuesta.ok) {
            mensaje.textContent = 'Reglamento subido correctamente.';
            document.getElementById('nombre-version').value = '';
            document.getElementById('archivo-reglamento').value = '';
            await actualizar_todo();
        } else {
            mensaje.textContent = datos.detail || 'Error al subir reglamento.';
        }
    });
}
actualizar_todo();
setInterval(actualizar_todo, 10000);