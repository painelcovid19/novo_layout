
let cabecalho = document.querySelector("#cabecaaa")
let mainparte1 = document.querySelector(".parte1")
let menubotao = document.querySelector(".menu-icone")

let menutraco = document.getElementById('menulinha')
let menux = document.getElementById('menux')
let navega = document.getElementById('navegacao')

function abrefecha()
{
    menutraco.classList.toggle('ativo')
    menux.classList.toggle('ativo')
    navega.classList.toggle('ativo')
}

//Scroll do header

addEventListener('scroll', function rolou()
{
    if(this.window.scrollY > 0)
    {
        cabecalho.classList.add('ativo')
        mainparte1.classList.add('ativo')
    }
    else
    {
        cabecalho.classList.remove('ativo')
        mainparte1.classList.remove('ativo')
    }

})