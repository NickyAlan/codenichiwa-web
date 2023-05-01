from flask import Flask, render_template, jsonify, request
from __function__ import transcript_list, download_transcript

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



if __name__ == '__main__' :
    app.run(debug=True)