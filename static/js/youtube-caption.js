const urlInput = document.getElementById('urlInput')
const pasteBtn = document.getElementById('pasteBtn')
const convertBtn = document.getElementById('convertBtn')
const imageTag = document.getElementById('image')
const titleTag = document.getElementById('title')
const selectLang = document.getElementById('selectLang')
const selectLangBtn = document.getElementById('selectLangBtn')
const downloadBtn = document.getElementById('downloadBtn')
const selectLangDiv = document.getElementById('select-lang-option')
const loadingDiv = document.getElementsByClassName('loding-css')[0]
const readlImageDiv = document.getElementsByClassName('main-caption-show')[0]
const loadingImageDiv = document.getElementsByClassName('main-loading')[0]
const inputUrlCaption = document.getElementById('input-url-caption')
const errorDiv =document.getElementById('error')

urlInput.addEventListener('keydown', function(evnet) {
    if (evnet.key == 'Enter') {
        sendVideoId()
    }
})
const url2VideoId = () => {
    // youtube url -> youtube video id
    if (urlInput.value.includes("youtu")) {
        if (urlInput.value.includes("channel")) {
            video_id = urlInput.value.split('=')[1].split('&')[0]
        }
        else if (urlInput.value.includes("?t=")) {
            video_id = urlInput.value.split('/')[3].split('?')[0]
        }
        else if (urlInput.value.includes("?v=")) {
            video_id = urlInput.value.split('?v=')[1]
        }
        else {
            video_id = urlInput.value.split('/')[3]
        }
    }
    else {
        video_id = null
    }
    return video_id
}

const sendVideoId = async () => {
    loadingDiv.style.display = 'flex'
    errorDiv.innerText = ''
    video_id = url2VideoId()
    if (video_id) {
        const response = await fetch(`/youtube/api/${video_id}`)
        const json = await response.json()
        if (json.length > 3) {
            let imageUrl = json[0].image
            let title = json[1].title
            let channelName = json[2].channel_name
            imageTag.src = imageUrl
            titleTag.innerText = title

            for (let idx=3; idx<json.length; idx++) {
                    selectLang.innerHTML += 
                    `<option value="${json[idx].code}">${json[idx].lang}</option>`
                }
            inputUrlCaption.style.display = 'none'
            loadingImageDiv.style.display = 'none'
            readlImageDiv.style.display = 'flex'
        }
        else {
            errorDiv.innerText = 'this video does not have caption / generate by youtube'
        }
    }
    else {
        errorDiv.innerText = 'this url not from youtube'
    }
    loadingDiv.style.display = 'none'
}

pasteBtn.onclick = async () => {
    const clipboardText = await navigator.clipboard.readText()
    urlInput.value = clipboardText
}

convertBtn.onclick = () => {
    sendVideoId()
}

selectLangBtn.onclick = async () => {
    code = selectLang.value
    video_id = url2VideoId()
    const response = await fetch(`youtube/api/${video_id}/${code}`)
    const json = await response.json()
    if (json.status == 200) {
        selectLang.style.display = 'none'
        selectLangBtn.style.display = 'none'
        selectLangDiv.innerHTML += "<a href='/static/files/yt-caption.txt' id='downloadBtn' download>download</a>"
        selectLangDiv.innerHTML += "<a href='youtube-caption-loader'>download more</a>"
    }
}

