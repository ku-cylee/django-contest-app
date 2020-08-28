ClassicEditor
    .create(document.querySelector('#editor'))
    .catch();

document.getElementById('editor').removeAttribute('required');
