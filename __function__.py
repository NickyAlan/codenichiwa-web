import requests
from youtube_transcript_api import YouTubeTranscriptApi

# youtube caption loader
def transcript_list(video_id) :
    try :
        transcripts_list = []
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        response = requests.get(f'https://youtu.be/{video_id}')
        transcripts_list.append({'image': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"})
        transcripts_list.append({'title': response.text.split('<title>')[1].split('</title>')[0][:-10]})
        transcripts_list.append({'channel_name': response.text.split('itemListElement')[1].split("}}]}")[0].split("name")[1].split('"')[-2]})
        for transcript in transcripts :
            # not automate caption from youtube
            if not transcript.is_generated :
                transcripts_list.append({
                    'lang': transcript.language,
                    'code': transcript.language_code,
                })
    except :
        transcripts_list = []
    return transcripts_list

def download_transcript(video_id, code) :
    transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
    caption = transcripts.find_transcript([code]).fetch()
    with open('static/files/yt-caption.txt', 'w', encoding='utf-8') as file :
        for line in caption :
            text = line['text'] 
            file.write(text + '\n')