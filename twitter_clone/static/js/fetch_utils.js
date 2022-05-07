// Функция создает и возвращает ошибку.
export function createError(response, data) {
    let e = new Error(data.error);
    e.data = data;
    e.data.status = response.status;
    return e;
};

// Функция редиректит на страницу логина при соответствующей ошибке.
export function redirectToLogin(error_data) {
    if (error_data.status == 401) {
        window.location.href = error_data.login_url;
    };
};