window.onmousemove = function (event) {
    document.body.style.backgroundPositionX = "-" + event.clientX/50 + "px"
    document.body.style.backgroundPositionY = "-" + event.clientY/50 + "px"
}