const menu_hamburger = document.querySelector(".menu-hamburger");
const nav_links = document.querySelector(".nav-links");
const content = document.querySelector(".content");
const body = document.querySelector("body");

menu_hamburger.addEventListener('click', ()=>{
    nav_links.classList.toggle('mobile-menu')
    body.classList.toggle('scroll-lock')
})