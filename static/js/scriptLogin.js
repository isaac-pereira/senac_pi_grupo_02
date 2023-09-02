const hamburguer = window.document.querySelector(".hamburguer");
let errorAlert = window.document.querySelector(".alert");
let inputEmail = window.document.getElementById("email");
let inputSenha = window.document.getElementById("senha");


hamburguer.addEventListener("click", () => {
    let mnMain = window.document.querySelector("#menu-main");

    hamburguer.classList.toggle("show");
    mnMain.classList.toggle("show");
});

if (errorAlert.style.display !== "none") {
    inputEmail.style.border = "1px solid #f44336";
    inputEmail.style.backgroundColor = "transparent";

    inputSenha.style.border = "1px solid #f44336";
    inputSenha.style.backgroundColor = "transparent";
};