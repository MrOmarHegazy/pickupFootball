let calendar = document.querySelector('.calendar')

let currDate = new Date()


document.querySelector('#prev-year').onclick = () => {
    
}


let dark_mode_toggle = document.querySelector('.dark-mode-switch')

dark_mode_toggle.onclick = () => {
    document.querySelector('body').classList.toggle('light')
    document.querySelector('body').classList.toggle('dark')
}