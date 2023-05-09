from flask import Flask, render_template, jsonify, request, redirect
from __function__ import transcript_list, download_transcript, Romanji2Hiragana, Romanji2Katakana, grammarChecker

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def homepage() :
    return render_template('home.html')

# youtube caption loader
@app.route('/youtube-caption-loader', methods=['GET', 'POST'])
def youtubepage() :
    return render_template('youtube-caption-loader.html')

@app.route('/youtube/api/<video_id>', methods=['GET', 'POST']) 
def youtube_api_transcript(video_id) :
    json = transcript_list(video_id)
    return jsonify(json)

@app.route('/youtube/api/<video_id>/<code>', methods=['GET', 'POST'])
def download_youtube_caption(video_id, code) :
    download_transcript(video_id, code)
    return jsonify({'status': 200})

# langStuff
@app.route('/langStuff', methods=['GET', 'POST'])
def langstuffpage() :
    return render_template('lang-convert.html')

@app.route('/langStuff/api/<C>/<text>')
def convertlangstuff(C, text) :
    if C == 'R2H' :
        results = Romanji2Hiragana(text)
    elif C == 'R2K' :
        results = Romanji2Katakana(text)
    else :
        results = grammarChecker(text)
    return jsonify(results)


if __name__ == '__main__' :
    app.run(debug=True)