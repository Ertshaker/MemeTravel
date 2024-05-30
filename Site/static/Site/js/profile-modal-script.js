var addFriendModal = document.getElementById("add-friend-modal");
var addFriendButton = document.getElementById("add-friend-btn");
var closeButton = document.querySelector("#add-friend-modal .close");
var incomingRequestsModal = document.getElementById("incoming-requests-modal");
var sentRequestsModal = document.getElementById("sent-requests-modal");
var incomingCloseButton = document.querySelector("#incoming-requests-modal .close");
var sentCloseButton = document.querySelector("#sent-requests-modal .close");
var scrollPosition;

function openModal() {
    document.body.style.overflow = 'hidden';
    scrollPosition = window.scrollY;
}

function closeModal() {
    window.scrollTo(0, scrollPosition);
    document.body.style.overflow = 'visible';
}


document.getElementById("incoming-requests-btn").onclick = function () {
    openModal();
    incomingRequestsModal.style.display = "block";
    return false;
}

document.getElementById("sent-requests-btn").onclick = function () {
    openModal();
    sentRequestsModal.style.display = "block";
    return false;
}

incomingCloseButton.onclick = function () {
    closeModal();
    incomingRequestsModal.style.display = "none";
}

sentCloseButton.onclick = function () {
    closeModal();
    sentRequestsModal.style.display = "none";
}

addFriendButton.onclick = function () {
    openModal()
    addFriendModal.style.display = "block";
    return false;
}

closeButton.onclick = function () {
    closeModal()
    addFriendModal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target === incomingRequestsModal) {
        closeModal();
        incomingRequestsModal.style.display = "none";
    }
    if (event.target === sentRequestsModal) {
        closeModal();
        sentRequestsModal.style.display = "none";
    }
}

$(document).ready(function () {
    $('#add-friend-btn').on('click', function () {
        $('#add-friend-modal').show();
    });

    $('#add-friend-form').submit(function (e) {
        e.preventDefault();

        var formData = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: '/friends_add/',
            data: formData,
            success: function (response) {
                toastr.success(response.message);
                $('#add-friend-modal').hide(); // Скрыть модальное окно
                setTimeout(function () {
                    location.reload();
                }, 1500);
            },
            error: function (xhr) {
                var errorMessage = 'Произошла ошибка. Попробуйте еще раз.';
                if (xhr.status === 400) {
                    errorMessage = 'Форма заполнена неверно.';
                } else if (xhr.status === 404) {
                    errorMessage = 'Пользователь не найден.';
                } else if (xhr.status === 409) {
                    errorMessage = 'Заявка уже существует или вы уже друзья.';
                }
                toastr.error(errorMessage);
            }
        });
    });
});