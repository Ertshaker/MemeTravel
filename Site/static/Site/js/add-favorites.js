$(document).ready(function () {
    $('.add-to-favorites-button').on('click', function () {
        var memeId = $(this).data('meme-id');
        addToFavorites(memeId);
    });

    function addToFavorites(memeId) {
        $.ajax({
            url: '/add_to_favorites/',
            type: 'POST',
            data: {
                meme_id: memeId,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function (response) {
                if (response.success) {
                    toastr.success('Мем теперь ЗОМБИТЕЛЬНО ИЗБРАН....');
                    setTimeout(function () {
                        location.reload();
                    }, 2000);
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