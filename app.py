import os
from flask import Flask, render_template, jsonify, request, redirect
from __function__ import ToJPG, toTensor, predict
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


# image classifier 
@app.route('/what-is-this-animal' , methods=['GET', 'POST'])
def wsta_upload_page() :
    if request.method == 'POST' :
        image_file = request.files['imageFile']
        if image_file.filename.endswith('avif') :
            alert = 'Please do not upload .avif file'
            return render_template('upload-clf.html', alert=alert)
        
        # clear all images for reducing storage
        dir_path = 'static/files/clf-image'
        files_path = [ os.path.join(dir_path, image_name) for image_name in os.listdir(dir_path) if image_name != 'weights' ]
        [ os.remove(file) for file in files_path ]

        save_path = f'{dir_path}/{image_file.filename}'
        image_file.save(dst=save_path)
        # .any -> .jpg
        if not image_file.filename.endswith('jpg') :
            save_path = ToJPG(image_path=save_path)
        
        # prediction
        try :
            image = toTensor(image_path=save_path)
            probas, pred_class = predict(image)
            probas = probas*100
            confs_probas = probas[:5].tolist()
            confs_class = pred_class[:5].tolist()
            predict_texts = [f'{a:.2f}% {b}' for a,b in zip(confs_probas, confs_class)]
        except :
            return render_template('upload-clf.html', alert='something went wrong with the image')

        return render_template('predict-clf.html', image_url=save_path, predicts=predict_texts)

    return render_template('upload-clf.html')

if __name__ == '__main__' :
    app.run(debug=True)