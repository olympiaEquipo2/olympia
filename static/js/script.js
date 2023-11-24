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