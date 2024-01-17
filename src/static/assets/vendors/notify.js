
function createNotify({
    title, message, theme, positionClass='nfc-top-right', closeOnClick=true, showDuration=5000
}) {
    // delete old notify elements
    document.querySelectorAll('.ncf-container').forEach((e) => {
        e.remove()
    })
    let id = `notify-${random_string(10)}`
    let notify_el = document.createElement('div')
    notify_el.id = `${id}`
    notify_el.className = `ncf-container ${positionClass}`
    notify_el.innerHTML = `
        <div class="ncf ${theme}"><p class="ncf-title">${title}</p><p class="nfc-message">${message || ''}</p></div>
    `
    document.body.append(notify_el)
    let element = document.getElementById(id)
    if (closeOnClick) {
        element.addEventListener('click', function () {
            element.remove()
        })
    }
    let show_duration_timeout = null
    try {
        clearTimeout(show_duration_timeout)
    } catch (e) {
    }
    show_duration_timeout = setTimeout(function () {
        element.remove()
    }, showDuration,)
}


function random_string(length) {
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
