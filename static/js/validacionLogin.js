function mostrarContrasena_login() {
    // Obtener los elementos de los campos de contraseña
    var passwordInput1 = document.getElementById("password1");

    // Comprobar si el tipo de entrada es "password"
    // Si es "password", cambiarlo a "text" para mostrar la contraseña
    // Si no es "password", cambiarlo de vuelta a "password" para ocultar la contraseña
    if (passwordInput1.type === "password") {
        passwordInput1.type = "text";
    } else {
        passwordInput1.type = "password";
    }
}