(function() {
    "use strict";

    // User stuff
    const style = document.getElementById('user-styles');
    if(localStorage.getItem('css')) {
        style.textContent = localStorage.getItem('css');
    }

    Array.from(document.querySelectorAll('#toolbar, #toolbar *')).forEach(e => {
        e.setAttribute('style', 'all: revert;'+(e.getAttribute('style') || ''));
    });

    document.getElementById('edit').addEventListener('click', () => {
        window.open('/editor', '_blank', 'height=570,width=520');
    });

    window.addEventListener('message', evt => {
        style.textContent = evt.data.css;
        localStorage.setItem('css', evt.data.css);
    });

    // Admin stuff
    const rate = document.getElementById('rater');
    rate.addEventListener('submit', async evt => {
        evt.preventDefault();

        const data = new FormData(rate);
        data.set('user', window.location.pathname.split('/').pop())
        const resp = await fetch('/admin/rate', {
            method: 'POST',
            body: data
        });

        rater.querySelector('.feedback').textContent = await resp.text();
    })
})();