
var nombre = document.getElementById("name");
var apellido = document.getElementById("adress");
var email = document.getElementById("email");
//var password = document.getElementById("password");


function validarContraseña(){
    const password =
    document.getElementById("password").value;
    const regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;

    const mensajeError=
    document.getElementById("mensajeError");


    if (regex.test(password)) {
        mensajeError.textContent="";
    } else {
        alert("La contraseña debe contener al menos 8 caracteres, una letra mayúscula, una letra minúscula y un número.");
    }


}