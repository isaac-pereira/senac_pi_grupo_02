const hamburguer = window.document.querySelector("#hamburguer");

hamburguer.addEventListener("click", () => {
    let userLogin = window.document.querySelector("#list-main");

    hamburguer.classList.toggle("show");
    userLogin.classList.toggle("show");
});