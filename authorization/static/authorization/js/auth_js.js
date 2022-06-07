// Инициализируем экземпляр класса всплывающих уведомлений
let toast_notifocation = document.getElementById('toastNotification');
let toast_text = document.querySelector('.toast-text');
let toast = new bootstrap.Toast(toast_notifocation);

/* Если у формы есть ошибки, не отосящиеся к конкретным полям,
то отображает их в уведомлении внизу страницы.
*/
let non_field_errors = document.querySelectorAll('.non-field-error');
document.addEventListener('DOMContentLoaded', function() {
    if (!!non_field_errors) {
        for (let error of non_field_errors) {
            toast_text.innerHTML = error.innerHTML;
            toast.show();
        };
    };
});