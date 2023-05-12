projectLoadingDiv = document.getElementsByClassName('loading-project')[0]
projectDiv = document.getElementById('project')
dropdownmenuDiv = document.getElementById('dropdown-menu')

projectArr = [
    {'title': 'Youtube Caption Loader', 'desc': 'This web app utilizes Python for the backend and JavaScript for the front-end to dynamically load YouTube captions.', 'url': '/youtube-caption-loader', 'image': 'static/images/youtube-caption-loader.png'},
    {'title': 'LangStuff', 'desc': 'A languages app Romanji to Kana using Python dictionaries, and a grammar checker API integrated dynamically using JS for enhanced functionality.', 'url': '/langStuff', 'image': 'static/images/lang-stuff.png'},
    {'title': 'Reddit to Youtube', 'desc': 'Automating the scraping of Reddit videos and uploading to YouTube', 'url': 'https://github.com/NickygenN1/youtube-automate', 'image': 'static/images/r2y.png'},
]

const showProject = () => {
    for (const item of projectArr) {    
        projectDiv.innerHTML += `<div class="box">
        <img src="${item.image}">
        <div class="text">
        <h3>${item.title}</h3>
        <p>${item.desc}</p>
        <a href="${item.url}" target='_blank'>view</a>
        </div>
        </div>`
    }
}

function toggleFunc(x) {
    x.classList.toggle("change")
    if (dropdownmenuDiv.style.display == '') {
        dropdownmenuDiv.style.display = 'flex'
    }
    else {
        dropdownmenuDiv.style.display = ''
    }
}

showProject()
window.addEventListener('load', () => {
    projectLoadingDiv.style.display = 'none'
})