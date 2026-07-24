const token = localStorage.getItem('token');

if (!token) {
    localStorage.setItem('rutaDestino', window.location.pathname);
    window.location.href = '/login-page';
}