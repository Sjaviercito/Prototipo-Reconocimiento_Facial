async function hacerLogin() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const error = document.getElementById('error');

    const respuesta = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    if (respuesta.ok) {
        const datos = await respuesta.json();

        localStorage.setItem('token', datos.token);
        localStorage.setItem('rol', datos.rol);

        if (datos.rol === "admin") {
            window.location.href = '/';
        } else if (datos.rol === "operador") {
            window.location.href = '/operador';
        } else {
            window.location.href = '/';
        }

    } else {
        error.textContent = 'Usuario o contraseña incorrectos';
    }
}