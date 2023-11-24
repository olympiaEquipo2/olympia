/*
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
*/
// Obtener el formulario y el mensaje de error por su ID
const form = document.getElementById('registroForm');
const mensajeError = document.getElementById('mensajeError');

// Agregar un evento al formulario cuando se envíe

form.addEventListener('submit', function (event) {
    // Prevenir el comportamiento predeterminado de envío del formulario
    event.preventDefault();
    
    // Obtener los valores de las contraseñas desde los campos de contraseña
    const password1 = document.getElementById('password1').value;
    const password2 = document.getElementById('password2').value;

    // Verificar si las contraseñas no coinciden
    if (password1 !== password2) {
        // Mostrar un mensaje de error si las contraseñas no coinciden
        mensajeError.textContent = 'Las contraseñas no coinciden';
    } else {
        // Las contraseñas coinciden y las demas validaciones estan bien, proceder a enviar el formulario
        if(validarRegistro()){
            return this.submit()
        }
        
    }
})
/*          
        // Obtener el elemento para mostrar el estado del formulario
        const status = document.getElementById('form-status');

        // Obtener los datos del formulario para enviar
        const formData = new FormData(form);

        // URL proporcionada por Formspree para enviar el formulario
        const url = 'https://formspree.io/f/mwkdaajv';
    
        // Enviar el formulario utilizando la función fetch
        
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        })
        .then(response => {
            // Si se envía correctamente, mostrar un mensaje de agradecimiento y restablecer el formulario
            status.innerHTML = '¡Gracias por registrarte!';
            form.reset();
        })
        .catch(error => {
            // Si hay algún error al enviar el formulario, mostrar un mensaje de error
            status.innerHTML = 'Hubo un problema al enviar el formulario.';
        });
    }
});
*/
function validarRegistro(){
    let nombre = document.getElementById("nombre");
    let apellido = document.getElementById("apellido");
    let email = document.getElementById('email');
    if(nombre.value == ""){
        alert('Por favor escriba su nombre entre 2 y 50 caracteres');
        nombre.focus();
        return false
    }else if(nombre.value.length<2 || nombre.value.length>50){
        alert('Por favor el nombre debe tener entre 2 y 50 letras')
        nombre.focus();
        return false
        }

    if(apellido.value == ""){
        alert('Por favor escriba su/s apellido/s entre 2 y 50 caracteres');
        nombre.focus();
        return false
    }else if(apellido.value.length<2 || apellido.value.length>50){
        alert('Por favor el nombre debe tener entre 2 y 50 letras')
        nombre.focus();
        return false
    }


    if(!email.value.includes('@') || !email.value.includes('.') || email.value==''){
        alert('Ingrese un correo electronico valido');
        email.focus();
        return false
    }



    return true
}

function mostrarContrasena() {
    // Obtener los elementos de los campos de contraseña
    var passwordInput1 = document.getElementById("password1");
    var passwordInput2 = document.getElementById("password2");

    // Comprobar si el tipo de entrada es "password"
    // Si es "password", cambiarlo a "text" para mostrar la contraseña
    // Si no es "password", cambiarlo de vuelta a "password" para ocultar la contraseña
    if (passwordInput1.type === "password") {
        passwordInput1.type = "text";
    } else {
        passwordInput1.type = "password";
    }

    // Realizar lo mismo para el segundo campo de contraseña (passwordInput2)
    if (passwordInput2.type === "password") {
        passwordInput2.type = "text";
    } else {
        passwordInput2.type = "password";
    }
}