// Удаляет блок с твитом, если данный твит удален из закладок пользователя.
let bookmark_btns = document.querySelectorAll('.bookmark-btn');
for (let bookmark_btn of bookmark_btns) {
    bookmark_btn.addEventListener('click', function() {
        let tweet_id = parseInt(this.id.match(/\d+/));
        document.getElementById(`user-bookmark${tweet_id}`).remove();
    });
};