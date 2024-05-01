function redirect(url) {
    window.location.href = url
}

function sendAjax({url, data, method = 'post', success, error}) {

    success = success || function (response) {
    }
    error = error || function (response) {
        createNotify(
            {
                title: 'ارور',
                message: 'مشکلی در ارسال درخواست وجود دارد لطفا اتصال خود را بررسی کنید',
                theme: 'error'
            }
        )
    }

    $.ajax(
        {
            url: url,
            data: JSON.stringify(data),
            type: method,
            headers: {
                'X-CSRFToken': window.CSRF_TOKEN
            },
            success: function (response) {
                success(response)
            },
            failed: function (response) {
                error(response)
            },
            error: function (response) {
                error(response)
            }
        }
    )
}

function getUrlParameter(sParam) {
    let sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;
    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
    return false;
}

function randomString(length = 15) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
        counter += 1;
    }
    return result;
}


function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function removeCookie(name) {
    document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}


// Convert date to jalali date
let all_datetime_convert = document.querySelectorAll('.datetime-convert')
for (let dt_el of all_datetime_convert) {
    let dt = dt_el.innerHTML || dt_el.value
    dt_el.setAttribute('datetime', dt)
    let dt_persian = new Date(dt).toLocaleDateString('fa-IR', {
        // hour: '2-digit',
        // minute: '2-digit'
    });
    if (dt_persian != 'Invalid Date') {
        dt_el.innerHTML = dt_persian
        dt_el.value = dt_persian
    }
}

// Convert digits to persian digits
const farsiDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];

let en_digits = document.querySelectorAll('.convert-digits');
for (let dt_el of en_digits) {
    let dt = dt_el.innerHTML || dt_el.value;
    dt_el.innerHTML = dt.toString().replace(/\d/g, x => farsiDigits[x]);
    dt_el.value = dt.toString().replace(/\d/g, x => farsiDigits[x]);
}


// Convert prices to int comma type
let all_spread_price = document.querySelectorAll('.spread-price')
for (let el of all_spread_price) {
    let price = el.innerHTML
    el.innerHTML = numberWithCommas(price)
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


// ---

let BtnRequestUnit = document.querySelectorAll(".btn-request-unit");
let Modal_RequestUnit = document.querySelectorAll(".modal-request-unit");
let overalyRequestUnit = document.querySelectorAll(".modal-request-unit .inner-modal");

BtnRequestUnit.forEach((item, index) => {
    item.addEventListener("click", () => {
        Modal_RequestUnit[index].classList.add("active");
    });
});
overalyRequestUnit.forEach((item, index) => {
    item.addEventListener("click", (e) => {
        if (e.target.className === "inner-modal") {
            Modal_RequestUnit[index].classList.remove("active");
        }
    });
});


// price elements
document.querySelectorAll('.price-el').forEach((el) => {
    let p = el.innerText
    el.setAttribute('price-val', p)
    el.innerHTML = numberWithCommas(p)
})

// full size element
document.querySelectorAll('.click-full-size').forEach(function (el) {
    el.addEventListener('click', function () {
        this.requestFullscreen();
    })
})


function togglePageLoading(title) {
    let loading = document.getElementById('page-loading')
    loading.querySelector('.loading-title').innerHTML = title
    loading.classList.toggle('active')
}