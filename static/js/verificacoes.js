// let nome = prompt("Como você chama?")
//
// if (nome == null) {
//     alert("Recarregue a página")
// }
// else {
//     let correto = confirm("Você se chama" + nome + " ?")
//
// if (correto) {
//     alert(nome + " Bem vindo ao site de cursos")
// }
// else {
//     alert("Recarregue a página")
// }
// }

function limpaInputsLogin () {
    const inputEmail = document.getElementById('input-email')
    const inputSenha = document.getElementById('input-senha')

    inputEmail.value = ''
    inputSenha.value = ''
}

document.addEventListener("DOMContentLoaded", function () {
    const formLogin = document.getElementById('form-login')

    formLogin.addEventListener("submit", function (event) {
        const inputEmail = document.getElementById('input-email')
        const inputSenha = document.getElementById('input-senha')

        let temErro = false

        if (inputEmail.value === '') {
            inputEmail.classList.add('is-invalid')
            temErro = true
        }
        else {
            inputEmail.classList.remove('is-invalid')
        }
        if (inputSenha.value === '') {
            inputSenha.classList.add('is-invalid')
            temErro = true
        }
        else {
            inputSenha.classList.remove('is-invalid')
        }

        if (temErro) {
            event.preventDefault()
            alert("Preencha todos os campos")
        }

    })
})



