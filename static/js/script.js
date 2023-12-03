const activacionBarra = document.getElementById("barra-lateral-activar");
const barraLateral = document.querySelector(".barra-lateral"); //Obtenemos la referencia al primer elemento que coincida con ".barra-lateral"
const spans = document.querySelectorAll("span"); //Obtenemos la referencia de todos los elementos que coincida con "span"
const palanca = document.querySelector(".switch");
const circulo = document.querySelector(".circulo");
const menu = document.querySelector(".menu");
const main = document.querySelector("main");

menu.addEventListener("click",()=>{
    barraLateral.classList.toggle("max-barra-lateral");
    if(barraLateral.classList.contains("max-barra-lateral")){
        menu.children[0].style.display = "none";
        menu.children[1].style.display = "block";
    }
    else{
        menu.children[0].style.display = "block";
        menu.children[1].style.display = "none";  
    }
})

palanca.addEventListener("click",()=>{
    let body = document.body;
    body.classList.toggle("modo-oscuro-activado");
    circulo.classList.toggle("prendido");
})


activacionBarra.addEventListener("click",(event)=>{
    if (event.target.classList.contains("barra-lateral-activar")) {
    barraLateral.classList.toggle("mini-barra-lateral"); //Agrega clase si no la tiene
    main.classList.toggle("min-main");
    spans.forEach((span) => { //ForEach para recorrer todos los span
        span.classList.toggle("oculto"); //Agrega clase si no la tiene
    });
}})

document.addEventListener('DOMContentLoaded', function() {
    var goTopButton = document.getElementById('go-top');

    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            goTopButton.classList.add('active');
        } else {
            goTopButton.classList.remove('active');
        }
    });

    goTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    // Seleccionamos los botones de reserva y cancelación
    const botonesReserva = document.querySelectorAll('.agendar_reserva, .cancelar_reserva');
    
    // Iteraramos sobre los botones
    botonesReserva.forEach(boton => {
        boton.addEventListener('click', function(event) {
            // Obtenemos datos del curso, horario, idusuario y idcurso del botón presionado
            const curso = this.getAttribute('data-curso');
            const horario = this.getAttribute('data-horario');
            const idusuario = this.getAttribute('data-id-usuario');
            const idcurso = this.getAttribute('data-id-curso');
            const cursoEncoded = encodeURIComponent(curso);
            const horarioEncoded = encodeURIComponent(horario);
            const idusuarioEncoded = encodeURIComponent(idusuario);
            const idcursoEncoded = encodeURIComponent(idcurso);
            
            // Aquí vemos si es un botón de cancelación de reserva o de reserva
            const esCancelarReserva = this.classList.contains('cancelar_reserva');
            
            // Constantes
            let url;
            let method;
            let body;
            
            // Configuramos la solicitud según el tipo de botón presionado
            // Si presionamos el botón cancelar vamos a la url cancelar_reserva con los datos necesarios
            if (esCancelarReserva) {
                url = '/cancelar_reserva'; // URL para cancelar reserva
                method = 'DELETE'; // Método DELETE para /cancelar reserva 
                body = `idusuario=${idusuarioEncoded}&idcurso=${idcursoEncoded}&curso=${cursoEncoded}&horario=${horarioEncoded}`;
            // Si presionamos el botón reservar vamos a la url /reservar_lugar con los datos necesarios
            } else {
                url = '/reservar_lugar'; // URL para reservar
                method = 'POST'; // Método POST para reservar
                body = `idusuario=${idusuarioEncoded}&idcurso=${idcursoEncoded}&curso=${cursoEncoded}&horario=${horarioEncoded}`;
            }
            
            // Enviar solicitud al servidor
            fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: body,
            })
            .then(response => {
                if (response.ok) {
                    // Cambiamos el estado del botón según la acción realizada
                    if (esCancelarReserva) {
                        this.textContent = 'Reserva Cancelada'; // Cambiamos el texto del boton a 'Reserva Cancelada' (cuando vuelve a cargar la pagina vuelve e poner 'Reservar' en el boton)
                    } else {
                        this.textContent = 'Reservado'; // Cambiamos el texto del boton a 'Reservado'
                        this.disabled = true; // Deshabilitamos el botón
                    }
                    location.reload(); // Recargarmos la página de perfil
                } else {
                    console.log("El servidor nos responde o respondió con un error");
                }
            })
            .catch(error => {
                console.error('Error al realizar la reserva:', error); // Mostramos errores en la consola
            });
        });
    });
});