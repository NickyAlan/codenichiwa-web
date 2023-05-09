const h1Tag = document.getElementById('h1Tag')
const selectBtn = document.getElementById('selectBtn')
const clearBtn = document.getElementById('clearBtn')
const pasteBtn = document.getElementById('pasteBtn')
const convertBtn = document.getElementById('convertBtn')
const inputText = document.getElementById('inputText')
const answerDiv = document.getElementById('answerDiv')
const loadingDiv = document.getElementById('loadingDiv')
const grammarWarning = document.getElementById('G')
const clickToCopyText = document.getElementById('C')

selectBtn.addEventListener('change', () => {
  const selectOption = selectBtn.options[selectBtn.selectedIndex]
  grammarWarning.style.display = 'none'
  clickToCopyText.style.display = 'none'
  h1Tag.innerText = selectOption.textContent
  answerDiv.innerHTML = ''
  if (selectBtn.value == 'G') {
      grammarWarning.style.display = 'block'
      inputText.value = ''
  }
})

clearBtn.addEventListener('click', () => {
  inputText.value = ''
  answerDiv.innerHTML = ''
  clickToCopyText.style.display = 'none'
  if (selectBtn.value != 'G') {
    grammarWarning.style.display = 'none'
  }
})

pasteBtn.addEventListener('click', async () => {
  let clipbordText = await navigator.clipboard.readText()
  inputText.value = clipbordText
})

convertBtn.addEventListener('click', () => {
  convertFunction()
})

inputText.onkeyup = (event) => {
  if (event.key == 'Enter' || selectBtn.value != 'G' ){
    convertFunction()
  }
  if (inputText.value.length == 0) {
    answerDiv.innerHTML = ''
    clickToCopyText.style.display = 'none'
  }
}

const convertFunction = async () => {
  let hiraganaList 
  let katakanaList
  let grammarList
  if (inputText.value != '') {
    if (selectBtn.value == 'R2H') {
      const response = await fetch(`/langStuff/api/R2H/${inputText.value}`)
      hiraganaList = await response.json()
      showAnswer(hiraganaList.results)
    }
    else if (selectBtn.value == 'R2K') {
      const response = await fetch(`/langStuff/api/R2K/${inputText.value}`)
      katakanaList = await response.json()
      showAnswer(katakanaList.results)
    }
    else {
      answerDiv.innerHTML = ''
      loadingDiv.style.display = 'flex'
      const response = await fetch(`/langStuff/api/G/${inputText.value}`)
      grammarList = await response.json()
      if (grammarList.results[0] == inputText.value) {
        grammarList.results[0] = '✓ ' + grammarList.results[0]
      }
      showAnswer(grammarList.results)
    }
  }
  loadingDiv.style.display = 'none'
}

const showAnswer = (answerList) => {
  if (answerList[0].length > 0) {
    idx = 0
    answerDiv.innerHTML = ''
    answerList.forEach(answer => {
      answerDiv.innerHTML += `<span id='${idx}'>${answer}</span>`
      idx++
    })
    answerDiv.querySelectorAll('span').forEach(span => {
      span.addEventListener('click', () => {
        navigator.clipboard.writeText(span.innerText)
      })
    })
    clickToCopyText.style.display = 'block'
  }
}