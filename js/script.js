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


/* API CLIMA */

document.addEventListener('DOMContentLoaded', function () {
    const url = 'https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid=512f8345dd32fc32c65d9e4a182c6806'; // Reemplaza esto con la URL de la API que deseas usar

    fetch(url)
        .then(response => response.json()) // Convierte la respuesta a formato JSON
        .then(data => {
            // Manipula los datos y muéstralos en la página
            const datosApiDiv = document.getElementById('datos-api');
            datosApiDiv.innerHTML = `Nombre: ${data.name}, Edad: ${data.age}`;
        })
        .catch(error => console.error('Error:', error));
});