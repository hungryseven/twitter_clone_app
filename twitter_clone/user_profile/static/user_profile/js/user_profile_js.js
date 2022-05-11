import {getCookie} from "/static/js/csrftoken.js";
import {createError, redirectToLogin} from "/static/js/fetch_utils.js";

const csrftoken = getCookie('csrftoken');

/* Добавляем класс 'active' тому элементу навигации, ссылка которого совпадает с текущей,
чтобы выделить выбранный пункт навигационной панели.
*/
const activeLink = window.location.href;
let nav_links = document.querySelectorAll('.nav-item.profile a');
nav_links.forEach(function(link) {
    if (link.href == activeLink) {
        link.parentElement.classList.add('active');
    };
});

let follow_btns = document.querySelectorAll('.follow-btn');

// AJAX-запрос с помощью fetch метода для добавления/удаления пользователей из подписок.
for (let follow_btn of follow_btns) {
    follow_btn.addEventListener('click', function(event) {
        event.preventDefault();
        let user_id = parseInt(this.id.match(/\d+/));
        
        /* 
        Если текущий пользователь уже подписался на данного пользователя(у кнопки будет класс "followed"),
        то отправится запрос на удаление пользователя из подсписок, иначе отправится запрос для добавления
        */
        if (follow_btn.classList.contains('followed')) {
            fetch('/friendship/destroy/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({'user_id': user_id})
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
                    this.classList.remove('followed');
                    this.innerHTML = 'Читать';
                })
                .catch(error => {
                    console.error(error.data.error);
                    redirectToLogin(error.data);
                });
        } else {
            fetch('/friendship/create/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({'user_id': user_id})
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
                    this.classList.add('followed');
                    this.innerHTML = 'Читаемые';
                })
                .catch(error => {
                    console.error(error.data.error);
                    redirectToLogin(error.data);
                });
        }
    });
};

// Скрипт для полей формы апдейта информации о пользователе.
const submit_btn = document.querySelector('.update-form-btn');
let fields = document.querySelectorAll('.form-floating input, .form-floating textarea');
for (let field of fields) {
    let counter = field.parentElement.querySelector('.counter');
    // Добавляем значение максимальной длины поля в счетчик.
    let max_length = counter.querySelector('.max-length');
    max_length.innerHTML = field.getAttribute('maxlength');

    // Добавляем значение текущей длины длины поля в счетчик.
    let current_length = counter.querySelector('.current-length');
    current_length.innerHTML = field.value.length;

    /* 
    Слушатель события по фокусу на поле,
    который делает счетчик символов видимым и добавляет другие события.
    */
    field.addEventListener('focus', function() {
        counter.classList.remove('visually-hidden');

        // Слушатель собития по изменения значения поля, который изменяет текущее значение счетчика символов.
        field.addEventListener('input', function() {
            current_length.innerHTML = field.value.length;

            /* 
            Для поля с именем профиля делаем проверку, что оно не пустое.
            Если оно пустое, то дизейблим кнопку формы.
            */
            if (field.name == 'profile_name' && field.value.length == 0) {
                submit_btn.disabled = true;
            } else if (field.name == 'profile_name' && field.value.length > 0) {
                submit_btn.disabled = false;
            };
        });

        // Слушатель события при потере фокуса на поле, который скрывает счетчик символов.
        field.addEventListener('blur', function() {
            counter.classList.add('visually-hidden');
        });
    });
};

/* Скрипт для файл инпута формы апдейта информации о пользователе.
Отображает превью загружаемой фотографии.
*/
const imageInput = document.querySelector('.image-input');
if (!!imageInput) {
    const photoPreview = document.querySelector('.photo-preview');
    imageInput.addEventListener('change', function() {
        // Создаем URL, отправленнойв файл инпут фотографии и отображаем ее в форме.
        photoPreview.src = URL.createObjectURL(imageInput.files[0]);
        
        // При загрузке фотографии освобождаем память.
        imageInput.addEventListener('load', function() {
            URL.revokeObjectURL(photoPreview.src);
        });
    });
};

/* AJAX-запрос с помощью fetch метода при загрузке DOM-дерева получает объект
с id пользователей, которые находятся в подписках у текущего, и применяет соответствующие классы и атрибуты для элементов.
*/
document.addEventListener('DOMContentLoaded', function() {
    fetch('/follow/api/', {
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            // Если нет ключа в объекте, то прекращаем выполнение функции
            if (!!data.followees == false) {
                return
            };
            
            for (let followee_id of data.followees) {
                let follow_btn = document.getElementById(`follow-btn${followee_id}`);
                if (!!follow_btn) {
                    follow_btn.classList.add('followed');
                    follow_btn.innerHTML = 'Читаемые';
                };
            };
        });
});