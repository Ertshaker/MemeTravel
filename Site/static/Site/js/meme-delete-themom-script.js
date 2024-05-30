$(document).ready(function() {
    $('#delete-meme-btn').click(function() {
        var memeId = $('#meme-id').val();
        var csrfToken = '{{ csrf_token }}';

        if (confirm('Вы уверены, что хотите удалить этот мем?')) {
            console.log("Отправка запроса на удаление мема с ID: " + memeId);
            $.ajax({
                url: '/meme/' + memeId + '/delete/',
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrfToken
                },
                success: function(response) {
                    console.log("Ответ сервера: ", response);
                    if (response.success) {
                        alert('Мем успешно удален');
                        window.location.href = '/encyclopedia/';
                    } else {
                        alert('Ошибка при удалении мема: ' + response.error);
                    }
                },
                error: function(xhr, status, error) {
                    console.log("Ошибка запроса: ", xhr.responseText);
                    alert('Ошибка при удалении мема');
                }
            });
        }
    });
});