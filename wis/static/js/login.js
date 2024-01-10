function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

const video = document.getElementById("video-element")
const image = document.getElementById("img-element")
const captureBtn = document.getElementById("capture-btn")
const reloadBtn = document.getElementById("reload-btn")
const inputPass = document.getElementById("input-pass")
const submitBtn = document.getElementById("submit-btn")

let requestData = null;

reloadBtn.addEventListener("click", () => {
    window.location.reload()
})

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({video: true}).then((stream) => {
        video.srcObject = stream
        const {height, width} = stream.getTracks()[0].getSettings()
        // console.log(stream.getTracks()[0].getSettings())
        captureBtn.addEventListener("click", e=> {
            captureBtn.classList.add("not-visible")

            const track = stream.getVideoTracks()[0]
            const imageCapture = new ImageCapture(track)
            // console.log(imageCapture)
            imageCapture.takePhoto().then(blob => {
                // console.log("took photo:", blob)
                const img = new Image(width,height)
                img.src = URL.createObjectURL(blob)
                image.append(img)

                video.classList.add("not-visible")

                const reader = new FileReader()

                reader.readAsDataURL(blob)
                reader.onloadend = () => {
                    const base64data = reader.result
                    // console.log(base64data)

                    const fd = new FormData()
                    fd.append('csrfmiddlewaretoken', csrftoken)
                    fd.append("photo", base64data)

                    $.ajax({
                        type: "POST",
                        url: "/face-id/classify/",
                        enctype: "multipart/form-data",
                        data: fd,
                        processData: false,
                        contentType: false,
                        success: (resp) => {
                            inputPass.classList.remove("not-visible")
                            inputPass.classList.add("input-pass")
                            submitBtn.classList.remove("not-visible")
                            requestData = {"user_uuid": resp.user_uuid}
                            console.log(requestData)
                            {
                            submitBtn.addEventListener("click", e=> {
                                console.log("Submitted")
                                requestData.password = inputPass.value
                                $.ajax({
                                    type: "POST",
                                    url: "/face-id/log-activity/",
                                    enctype: "application/json",
                                    contentType: "application/json",
                                    headers: {"X-CSRFToken": getCookie("csrftoken")},
                                    data: JSON.stringify(requestData),
                                    processData: false,
                                    success: (resp) => {
                                            console.log("Rozpoznano")
                                        },
                                        error: (err) => {
                                            console.log(err)
                                        }
                                    })
                                })
                            }
                        },
                        error: (err) => {
                            console.log(err)
                        }
                    })
                }
            })
        })
    })
}
