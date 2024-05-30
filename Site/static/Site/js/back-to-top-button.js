 var element = document.querySelector('#memes-box');
    element.onscroll = function () {
        scrollFunction();
    };

    function scrollFunction() {
        if (element.scrollTop > 20) {
            document.getElementById("back-to-top").style.display = "block";
            show("back-to-top", 300);

        } else {
            document.getElementById("back-to-top").style.display = "none";
            document.getElementById("back-to-top").style.opacity = 0;
        }
    }

    function show(id, speed) {
        let vars;
        var ID = setInterval(function () {
            (vars = Number(document.getElementById(id).style.opacity));
            if (vars > 1) {
                clearInterval(ID);
            }
            vars += 0.1;
            document.getElementById(id).style.opacity = vars;
        }, speed);
    }

    document.getElementById("back-to-top").onclick = function () {
        scrollToTop();
    };

    function scrollToTop() {
        element.scroll({top: 0, behavior: 'smooth'});
    }