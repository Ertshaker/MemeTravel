$(document).ready(function () {
        $('.remove-from-favorites-button').on('click', function () {
            var memeId = $(this).data('meme-id');
            removeFromFavorites(memeId);
        });

        function removeFromFavorites(memeId) {
            $.ajax({
                url: '/remove_from_favorites/',
                type: 'POST',
                data: {
                    meme_id: memeId,
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                },
                success: function (response) {
                    if (response.success) {
                        toastr.success('Мем теперь АНТИЗОМБИТЕЛЕН....');
                        setTimeout(function () {
                            location.reload();
                        }, 1500);
                    } else {
                        toastr.error(response.error);
                    }
                },
                error: function (xhr, status, error) {
                    toastr.error(error);
                }
            });
        }
    });