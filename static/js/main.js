projectDiv = document.getElementById('project')
dropdownmenuDiv = document.getElementById('dropdown-menu')

for (let i=0; i<5; i++) {
    projectDiv.innerHTML += 
    `<div class="box">
    <img src="static/images/521-300x300.jpg" alt="">
    <div class="text">
    <h3>Title</h3>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique, sunt laboriosam? Ipsa quidem vitae nesciunt. Esse natus placeat harum voluptatum.</p>
      <a href="">view</a>
      </div>
    </div>`
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