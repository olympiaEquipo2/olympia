

function validarFormulario(){


    let nombre = document.getElementById("nombre");
    let email = document.getElementById('email');
    let mensaje = document.getElementById('mensaje');
     
if(nombre.value == ""){
 alert('Por favor escriba su nombre entre 2 y 50 caracteres');
 nombre.focus();
 return
}else if(nombre.value.length<2 || nombre.value.length>50){
    alert('Por favor el nombre debe tener entre 2 y 50 letras')
    nombre.focus();
    return
}


if(!email.value.includes('@') || !email.value.includes('.') || email.value==''){
    alert('Ingrese un correo electronico valido');
    email.focus();
    return
}

if(mensaje.value.length == ''){
   alert('Por favor escriba un mensaje')
}
}