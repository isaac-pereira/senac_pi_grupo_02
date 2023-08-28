const hamburguer = window.document.querySelector(".hamburguer");

hamburguer.addEventListener("click", () => {
    let mnMain = window.document.querySelector("#menu-main");

    hamburguer.classList.toggle("show");
    mnMain.classList.toggle("show");
});