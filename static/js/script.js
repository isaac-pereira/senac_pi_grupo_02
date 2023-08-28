const hamburguer = window.document.querySelector(".hamburguer");

hamburguer.addEventListener("click", () => {
    let userLogin = window.document.querySelector(".login");
    let optionNav = window.document.querySelector(".section-body");

    hamburguer.classList.toggle("show");
    userLogin.classList.toggle("show");
    optionNav.classList.toggle("show");
});