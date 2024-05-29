function checkWindowWidth() {
    const elements = document.querySelectorAll('.memes-horizontal-container'); // Замените на ваш селектор
    var kilroy = document.querySelector('.start-XX-block')
    const threshold = 768;
    console.log(window.innerWidth)
    elements.forEach(element => {
        if (window.innerWidth <= threshold) {
            element.classList.add('memes-vertical-container');
            kilroy.classList.add('memes-vertical-container');
        } else {
            element.classList.remove('memes-vertical-container');
            kilroy.classList.remove('memes-vertical-container');
        }
    })
}

window.onresize =  checkWindowWidth;

document.addEventListener('DOMContentLoaded', checkWindowWidth);