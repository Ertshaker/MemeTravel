const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry.target.id + entry.intersectionRatio);
        if (entry.isIntersecting && !isScrolling) {
            console.log('ПРИВЕТ Я ТУТ ПОКА ТЫ СКРОЛИШЬСЯ')
            const currentSection = entry.target;
            isScrolling = true;
            scrollingBox.classList.add('no-scroll');
            currentSection.classList.add('show')
            currentSection.scrollIntoView({behavior: "smooth"});
            setTimeout(() => {
                isScrolling = false;
                scrollingBox.classList.remove('no-scroll');
            }, 500);
        } else {
            entry.target.classList.remove('show')
        }
    });
});

var scrollingBox = document.getElementById('sections-box');
let isScrolling = false;
const hiddenElements = document.querySelectorAll('.hidden');
hiddenElements.forEach((el) => observer.observe(el))

