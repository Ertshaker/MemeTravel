$(document).ready(function () {
    $('.add-friend-button').on('click', function () {
        var friendId = $(this).data('friend-id');
        addFriendRequest(friendId);
    });

    function addFriendRequest(friendId) {
        var csrfToken = '{{ csrf_token }}';

        var deferred = $.Deferred();

        $.ajax({
            url: '/add_friend_request/',
            type: 'POST',
            data: {
                friend_id: friendId,
                csrfmiddlewaretoken: csrfToken
            }
        })
            .done(function (response) {
                if (response.success) {
                    deferred.resolve(response);
                    toastr.success('Запрос в друзья ЗОМБИТЕЛЕН!');
                    setTimeout(function () {
                        location.reload();
                    }, 2000);
                } else {
                    deferred.reject(response.error);
                    console.error(response.error);
                }
            })
            .fail(function (xhr, status, error) {
                deferred.reject(error);
                console.error(error);
            });

        return deferred.promise();
    }
});