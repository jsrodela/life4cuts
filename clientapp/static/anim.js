function remove() {
    for (let obj of document.querySelectorAll('.anim')) {
        obj.classList.remove('anim');
        obj.classList.add('remove');
    }
    for (let obj of document.querySelectorAll('.click')) {
        obj.disabled = true
        obj.classList.remove('click')
    }
}