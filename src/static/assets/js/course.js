// ---------------------------- Add video url to video section -------------------------- //
function setVidUrl(e) {
    let button = $(e);
    let url = button.data('url');

    let video = document.getElementById('courseVideo');
    video.classList.remove('d-none');
    video.pause();

    let videoSource = video.querySelector('source');
    videoSource.setAttribute('src', url);

    // Move to top
    document.body.scrollTop = document.documentElement.scrollTop = 0

    video.load();
    video.play();
}
// ------------------------- Add video url to video section -------------------------- //