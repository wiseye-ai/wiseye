console.log("hello world")

const video = document.getElementById("video-element")
const image = document.getElementById("img-element")
const captureBtn = document.getElementById("capture-btn")
const reloadBtn = document.getElementById("reload-btn")

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({video: true}).then((stream) => {
        video.srcObject = stream
        console.log(stream.getTracks())
    })
}
