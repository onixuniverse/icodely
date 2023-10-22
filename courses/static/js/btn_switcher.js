const status_step = document.querySelectorAll(".status")
const buttons = document.querySelectorAll(".btn_start")

for (let i = 0; i <= status_step.length - 1; i++){
    if (status_step[i].classList.contains('done')){
        buttons[i].classList.add('watch_button');
        buttons[i].innerHTML = 'Посмотреть';
    }

    if (status_step[i].classList.contains('unavailable')){
        buttons[i].classList.add('unavailable_button');
    }
}

