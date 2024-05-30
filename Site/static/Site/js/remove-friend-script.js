$(document).ready(function () {
        $('.remove-friend-button').on('click', function () {
            var friendId = $(this).data('friend-id');
            removeFriendRequest(friendId);
        });

        function removeFriendRequest(friendId) {
            $.ajax({
                url: '/remove_friend_request/',
                type: 'POST',
                data: {
                    friend_id: friendId,
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                },
                success: function (response) {
                    if (response.success) {
                        toastr.success('Друг теперь АНТИЗОМБИТЕЛЕН....');
                        setTimeout(function () {
                            location.reload();
                        }, 1500);
                    } else {
                        // Обработка ошибки
                        console.error(response.error);
                    }
                },
                error: function (xhr, status, error) {
                    // Обработка ошибки AJAX-запроса
                    console.error(error);
                }
            });
        }
    });