
function navbarMenu(){
    const menu =  document.querySelector('.navbar-menu')
    menu.classList.toggle('active')
}

function pantallaCarga() {
    const carga = document.querySelector('.loader')
    carga.classList.add('active');
}

function modalCard(){
    const modal = document.querySelector('.modal')
    modal.classList.toggle('modal--active')
}

window.onclick = function(event) {
    const modal = document.querySelector('.modal')
    if (event.target == modal) {
        modal.classList.toggle('modal--active')
    }
}