async function cargarBD() {
    const respuesta = await fetch('/admin/bd', {
        headers: { 'Authorization': 'Bearer ' + token }
    });

    if (respuesta.status === 401) {
        window.location.href = '/login-page';
        return;
    }

    const datos = await respuesta.json();
    const contenedor = document.getElementById('contenedor-bd');

    contenedor.innerHTML = '';

    for (const tabla of datos.tablas) {
        const seccion = document.createElement('section');

        let html = `
            <h2>${tabla.tabla}</h2>
            <table>
                <thead>
                    <tr>
        `;

        for (const columna of tabla.columnas) {
            html += `<th>${columna}</th>`;
        }

        html += `
                    </tr>
                </thead>
                <tbody>
        `;

        for (const registro of tabla.registros) {
            html += '<tr>';

            for (const valor of registro) {
                html += `<td>${valor === null ? '—' : valor}</td>`;
            }

            html += '</tr>';
        }

        html += `
                </tbody>
            </table>
        `;

        seccion.innerHTML = html;
        contenedor.appendChild(seccion);
    }
}


async function reiniciarBD() {
    const confirmar1 = confirm("¿Seguro que quieres reiniciar TODA la base de datos?");
    if (!confirmar1) return;

    const confirmar2 = confirm("Esto borrará usuarios, personas, visitas, auditoría, reglamentos y firmas. ¿Continuar?");
    if (!confirmar2) return;

    const respuesta = await fetch('/admin/bd', {
        method: 'DELETE',
        headers: { 'Authorization': 'Bearer ' + token }
    });

    const datos = await respuesta.json();

    if (respuesta.ok) {
        alert(datos.mensaje);
        await cargarBD();
    } else {
        alert(datos.detail || "Error al reiniciar la base de datos");
    }
}
console.log("admin.js cargado");
cargarBD();