import {getCookie} from "/static/js/csrftoken.js";
import {createError, redirectToLogin} from "/static/js/fetch_utils.js";

const csrftoken = getCookie('csrftoken');

let textareas = document.querySelectorAll('.tweet-textarea');
let max_length = 140;
for (let textarea of textareas) {
    textarea.addEventListener('input', function() {
        let make_tweet_btn = this.parentNode.nextElementSibling.querySelector('.make-tweet-btn');
        let counter = this.parentNode.nextElementSibling.querySelector('.chars-counter');
        /* 
        Если 0 < длина текста <= 140, то кнопка создания твита активна,
        и счетчик оставшегося количества символов окрашивается в черный цвет.
        В противном случае, кнопка дизейблится, и счетчик окрашивается в красный цвет.
        */
        if (this.value.length > 0 && this.value.length <= max_length) {
            make_tweet_btn.disabled = false;
            counter.classList.remove('excess-length');
        } else {
            make_tweet_btn.disabled = true;
            counter.classList.add('excess-length');
        };

        // Если длина текста > 0, то отображаем счетчик с количеством оставшихся символов до максимально возможной длины твита.
        if (this.value.length > 0) {
            counter.classList.remove('visually-hidden');
            counter.innerHTML = max_length - this.value.length;
        } else {
            counter.classList.add('visually-hidden');
        }
    });
};

// Инициализируем экземпляр класса всплывающих уведомлений
let toast_notifocation = document.getElementById('toastNotification');
let toast_text = document.querySelector('.toast-text');
let toast = new bootstrap.Toast(toast_notifocation);

// AJAX-запрос с помощью fetch метода для лайка/дизлайка твитов.
let like_btns = document.querySelectorAll('.like-btn');
let likes_svg = {
    'not_like': 'M12 21.638h-.014C9.403 21.59 1.95 14.856 1.95 8.478c0-3.064 2.525-5.754 5.403-5.754 2.29 0 3.83 1.58 4.646 2.73.814-1.148 2.354-2.73 4.645-2.73 2.88 0 5.404 2.69 5.404 5.755 0 6.376-7.454 13.11-10.037 13.157H12zM7.354 4.225c-2.08 0-3.903 1.988-3.903 4.255 0 5.74 7.034 11.596 8.55 11.658 1.518-.062 8.55-5.917 8.55-11.658 0-2.267-1.823-4.255-3.903-4.255-2.528 0-3.94 2.936-3.952 2.965-.23.562-1.156.562-1.387 0-.014-.03-1.425-2.965-3.954-2.965z',
    'like': 'M12 21.638h-.014C9.403 21.59 1.95 14.856 1.95 8.478c0-3.064 2.525-5.754 5.403-5.754 2.29 0 3.83 1.58 4.646 2.73.814-1.148 2.354-2.73 4.645-2.73 2.88 0 5.404 2.69 5.404 5.755 0 6.376-7.454 13.11-10.037 13.157H12z'
}

for (let like_btn of like_btns) {
    like_btn.addEventListener('click', function(event) {
        event.preventDefault();
        let tweet_id = parseInt(this.id.match(/\d+/));
        let counter = document.getElementById(`likes-count${tweet_id}`);
        let svg = this.querySelector('svg');
        let svg_path = svg.querySelector('path');

        /* 
        Если твит уже лайкнут пользователем (у кнопки будет класс "liked"), то отправится запрос на удаление,
        иначе отправится запрос для добавления в понравившееся.
        */
        if (this.classList.contains('liked')) {
            fetch('/dislike/tweet/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({'tweet_id': tweet_id})
            })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    };
                    return response.json().then(error => {
                        let e = createError(response, error);
                        throw e;
                    });
                })
                .then(data => {
                    // Устанавливаем новое количество лайков на посте.
                    if (data.quantity == 0) {
                        counter.innerHTML = '';
                    } else {
                        counter.innerHTML = data.quantity;
                    };

                    // Меняем классы и атрибуты на кнопке, счетчике лайков и svg-иконке.
                    this.classList.remove('liked');
                    counter.classList.remove('like-active');
                    counter.classList.add('not-active');
                    svg.setAttribute('fill', 'CurrentColor');
                    svg_path.setAttribute('d', likes_svg.not_like);
                })
                .catch(error => {
                    console.error(error.data.error);
                    redirectToLogin(error.data);
                });
        } else {
            fetch('/like/tweet/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({'tweet_id': tweet_id})
            })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    };
                    return response.json().then(error => {
                        let e = createError(response, error);
                        throw e;
                    });
                })
                .then(data => {
                    // Устанавливаем новое количество лайков на посте.
                    counter.innerHTML = data.quantity;

                    // Меняем классы и атрибуты на кнопке, счетчике лайков и svg-иконке.
                    this.classList.add('liked');
                    counter.classList.remove('not-active');
                    counter.classList.add('like-active');
                    svg.setAttribute('fill', 'rgb(249, 24, 128)');
                    svg_path.setAttribute('d', likes_svg.like);
                })
                .catch(error => {
                    console.error(error.data.error);
                    redirectToLogin(error.data);
                });
        };
    });
};

// AJAX-запрос с помощью fetch метода для ретвита/анретвита.
let retweet_btns = document.querySelectorAll('.retweet-btn');
let retweets_svg = {
    'not_retweet': 'M23.77 15.67c-.292-.293-.767-.293-1.06 0l-2.22 2.22V7.65c0-2.068-1.683-3.75-3.75-3.75h-5.85c-.414 0-.75.336-.75.75s.336.75.75.75h5.85c1.24 0 2.25 1.01 2.25 2.25v10.24l-2.22-2.22c-.293-.293-.768-.293-1.06 0s-.294.768 0 1.06l3.5 3.5c.145.147.337.22.53.22s.383-.072.53-.22l3.5-3.5c.294-.292.294-.767 0-1.06zm-10.66 3.28H7.26c-1.24 0-2.25-1.01-2.25-2.25V6.46l2.22 2.22c.148.147.34.22.532.22s.384-.073.53-.22c.293-.293.293-.768 0-1.06l-3.5-3.5c-.293-.294-.768-.294-1.06 0l-3.5 3.5c-.294.292-.294.767 0 1.06s.767.293 1.06 0l2.22-2.22V16.7c0 2.068 1.683 3.75 3.75 3.75h5.85c.414 0 .75-.336.75-.75s-.337-.75-.75-.75z',
    'retweet': 'M23.615 15.477c-.47-.47-1.23-.47-1.697 0l-1.326 1.326V7.4c0-2.178-1.772-3.95-3.95-3.95h-5.2c-.663 0-1.2.538-1.2 1.2s.537 1.2 1.2 1.2h5.2c.854 0 1.55.695 1.55 1.55v9.403l-1.326-1.326c-.47-.47-1.23-.47-1.697 0s-.47 1.23 0 1.697l3.374 3.375c.234.233.542.35.85.35s.613-.116.848-.35l3.375-3.376c.467-.47.467-1.23-.002-1.697zM12.562 18.5h-5.2c-.854 0-1.55-.695-1.55-1.55V7.547l1.326 1.326c.234.235.542.352.848.352s.614-.117.85-.352c.468-.47.468-1.23 0-1.697L5.46 3.8c-.47-.468-1.23-.468-1.697 0L.388 7.177c-.47.47-.47 1.23 0 1.697s1.23.47 1.697 0L3.41 7.547v9.403c0 2.178 1.773 3.95 3.95 3.95h5.2c.664 0 1.2-.538 1.2-1.2s-.535-1.2-1.198-1.2z'
}

for (let retweet_btn of retweet_btns) {
    retweet_btn.addEventListener('click', function(event) {
        event.preventDefault();
        let tweet_id = parseInt(this.id.match(/\d+/));
        let counter = document.getElementById(`retweets-count${tweet_id}`);
        let svg = this.querySelector('svg');
        let svg_path = svg.querySelector('path');

        /* 
        Если твит уже ретвитнут пользователем (у кнопки будет класс "retweeted"), то отправится запрос на удаление,
        иначе отправится запрос для добавления в ретвитнутое.
        */
        if (this.classList.contains('retweeted')) {
            fetch('/cancel-retweet/tweet/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({'tweet_id': tweet_id})
            })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    };
                    return response.json().then(error => {
                        let e = createError(response, error);
                        throw e;
                    });
                })
                .then(data => {
                    // Устанавливаем новое количество ретвитов на посте.
                    if (data.quantity == 0) {
                        counter.innerHTML = '';
                    } else {
                        counter.innerHTML = data.quantity;
                    };

                    // Меняем классы и атрибуты на кнопке, счетчике ретвитов и svg-иконке.
                    this.classList.remove('retweeted');
                    counter.classList.remove('retweet-active');
                    counter.classList.add('not-active');
                    svg.setAttribute('fill', 'CurrentColor');
                    svg_path.setAttribute('d', retweets_svg.not_retweet);
                })
                .catch(error => {
                    console.error(error.data.error);
                    redirectToLogin(error.data);
                });
        } else {
            fetch('/retweet/tweet/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({'tweet_id': tweet_id})
            })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    };
                    return response.json().then(error => {
                        let e = createError(response, error);
                        throw e;
                    });
                })
                .then(data => {
                    // Устанавливаем новое количество ретвитов на посте.
                    counter.innerHTML = data.quantity;

                    // Меняем классы и атрибуты на кнопке, счетчике ретвитов и svg-иконке.
                    this.classList.add('retweeted');
                    counter.classList.remove('not-active');
                    counter.classList.add('retweet-active');
                    svg.setAttribute('fill', 'rgb(0, 186, 124)');
                    svg_path.setAttribute('d', retweets_svg.retweet);
                })
                .catch(error => {
                    console.error(error.data.error);
                    redirectToLogin(error.data);
                });
        };
    });
};

// AJAX-запрос с помощью fetch метода для добавления/удаления из закладок.
let bookmark_btns = document.querySelectorAll('.bookmark-btn');

for (let bookmark_btn of bookmark_btns) {
    bookmark_btn.addEventListener('click', function(event) {
        event.preventDefault();
        let tweet_id = parseInt(this.id.match(/\d+/));
        let btn_text = this.querySelector('.item-text');

        /* 
        Если твит уже в закладках у пользователя (у кнопки будет класс "bookmarked"), то отправится запрос на удаление,
        иначе отправится запрос для добавления в закладки.
        */
        if (this.classList.contains('bookmarked')) {
            fetch('/delete-from-bookmarks/tweet/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({'tweet_id': tweet_id})
            })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    }
                    return response.json().then(error => {
                        let e = createError(response, error);
                        throw e;
                    });
                })
                .then(data => {
                    // Меняем класс кнопки и ее текст.
                    this.classList.remove('bookmarked');
                    btn_text.innerHTML = data.btn_text;
                    // Вкладываем текст во всплывающее уведомление и вызываем его.
                    toast_text.innerHTML = data.success_message;
                    toast.show();
                })
                .catch(error => {
                    console.error(error.data.error);
                    redirectToLogin(error.data);
                });
        } else {
            fetch('/add-to-bookmarks/tweet/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({'tweet_id': tweet_id})
            })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    };
                    return response.json().then(error => {
                        let e = createError(response, error);
                        throw e;
                    });
                })
                .then(data => {
                    // Меняем класс кнопки и ее текст.
                    this.classList.add('bookmarked');
                    btn_text.innerHTML = data.btn_text;
                    // Вкладываем текст во всплывающее уведомление и вызываем его.
                    toast_text.innerHTML = data.success_message;
                    toast.show();
                })
                .catch(error => {
                    console.error(error.data.error);
                    redirectToLogin(error.data);
                });
        };
    });
};

/* Обработчик при клике на кнопку "Копировать ссылку на твит".
Копирует абсолютную ссылку твита в буфер обмена и выводит всплывающее уведомление об успешности действия.
*/
let copy_btns = document.querySelectorAll('.copy-tweet-btn');

// Инициализируем Clipboard для всех кнопок, которые копируют ссылки на твит в буфер обмена
new ClipboardJS('.copy-tweet-btn');

for (let copy_btn of copy_btns) {
    copy_btn.addEventListener('click', function(event) {
        event.preventDefault();
        toast_text.innerHTML = 'Скопировано в буфер обмена';
        toast.show();
    });
};

/* AJAX-запрос с помощью fetch метода при загрузке DOM-дерева получает объект
с id лайков, ретвитов и закладок пользователя и применяет соответствующие классы и атрибуты для элементов.
*/
document.addEventListener('DOMContentLoaded', function() {
    fetch('/actions/api/', {
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            // Если нет какого-то из ключей в объекте, то прекращаем выполнение функции
            if (!!data.likes == false || !!data.retweets == false || !!data.bookmarks == false) {
                return
            };

            for (let liked_id of data.likes) {
                let like_btn = document.getElementById(`like-btn${liked_id}`);
                let counter = document.getElementById(`likes-count${liked_id}`);

                // Если на странице существует кнопка лайка c текущим id, то проводим манипуляции с элементами.
                if (!!like_btn) {
                    like_btn.classList.add('liked');
                    counter.classList.remove('not-active');
                    counter.classList.add('like-active');
                    let svg = like_btn.querySelector('svg');
                    let svg_path = svg.querySelector('path');
                    svg.setAttribute('fill', 'rgb(249, 24, 128)');
                    svg_path.setAttribute('d', likes_svg.like);
                };
            };

            for (let retweeted_id of data.retweets) {
                let retweet_btn = document.getElementById(`retweet-btn${retweeted_id}`);
                let counter = document.getElementById(`retweets-count${retweeted_id}`);

                // Если на странице существует кнопка ретвита c текущим id, то проводим манипуляции с элементами.
                if (!!retweet_btn) {
                    retweet_btn.classList.add('retweeted');
                    counter.classList.remove('not-active');
                    counter.classList.add('retweet-active');
                    let svg = retweet_btn.querySelector('svg');
                    let svg_path = svg.querySelector('path');
                    svg.setAttribute('fill', 'rgb(0, 186, 124)');
                    svg_path.setAttribute('d', retweets_svg.retweet);
                };
            };
            
            for (let bookmarked_id of data.bookmarks) {
                let bookmark_btn = document.getElementById(`bookmark-btn${bookmarked_id}`);

                // Если на странице существует кнопка с закладкой c текущим id, то проводим манипуляции с элементами.
                if (!!bookmark_btn) {
                    let btn_text = bookmark_btn.querySelector('.item-text');
                    bookmark_btn.classList.add('bookmarked');
                    btn_text.innerHTML = 'Удалить твит из закладок';
                };
            };
        });
});