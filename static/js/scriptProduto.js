const hamburguer = window.document.querySelector("#hamburguer");

hamburguer.addEventListener("click", () => {
    let productScript = window.document.querySelector(".conteiner-links");

    hamburguer.classList.toggle("show");
    productScript.classList.toggle("show");
});