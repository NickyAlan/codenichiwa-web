import requests, json
from string import ascii_lowercase
from youtube_transcript_api import YouTubeTranscriptApi
from gingerit.gingerit import GingerIt

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

# langStuff
def text2syllables(text: str) :
    """
    convert long text to syllabels list
    """
    text = text.lower().replace(" ", "")
    syllables = []
    current_word = ""
    vowels = ['a','e','i','o','u']
    for char in text :
        current_word += char
        if char in vowels :
            syllables.append(current_word)
            current_word = ""

    alphabets = list(set(ascii_lowercase).difference(set(vowels+["y"])))
    ntext_word = [f'n{alphabet}' for alphabet in alphabets]
    for idx, syllable in enumerate(syllables) :
        if syllable[:2] in ntext_word :
            syllables.insert(idx, "n")
            syllables[idx+1] = syllables[idx+1][1:]
    
    # forgot last "n"
    if text[-1] == 'n': syllables.append("n") 
    return syllables

def map_kana(syllables: list, maper: dict) :
    '''
    convert romanji to kana string
    '''
    to_ = []
    try : 
        for syllable in syllables :
            if syllable[-1] == 'n' and len(syllable) >= 3 :
                syllable = syllable[:-1]
                kana_ = maper[syllable] + maper['n']
            elif syllable[-1] == 'i' and len(syllable) >= 3 and (syllable != 'chi' and syllable != 'shi'):
                syllable = syllable[:-1]
                kana_ = maper[syllable] + maper['i']
            elif syllable[2:] == 'su' and len(syllable) == 4 :
                if syllable[:-2] == 'de' :
                    kana_ = maper['de'] + maper['su']
                elif syllable[:-2] == 'ma' :
                    kana_ = maper['ma'] + maper['su']
            else :
                kana_ = maper[syllable] 
            to_.append(kana_)
    except :
        pass
        
    kana = ''.join(to_)
    return kana

def extract_ambiguous_kana(syllables: list) :
    '''
    extract ambigous list of possible kana text
    '''
    ambiguous_list = ['wa','su','zu', 'ja', 'ju', 'jo', 'ji', 'o']
    kana_convert_list = [syllables]
    for idx, char in enumerate(syllables) :
        if char in ambiguous_list :
            # masu or desu -> pass
            if char == 'su' and ((syllables[idx-1]=='ma') or (syllables[idx-1]=='de')) :
                continue
            else :
                if char == 'su' :
                    v2 = 'tsu'
                elif char == 'wa' :
                    v2 = 'ha'
                elif char == 'o' :
                    v2 = 'wo'
                else :
                    v2 = f'{char}2'
                
                v2_text = syllables.copy()
                v2_text[idx] = v2 
                kana_convert_list.append(v2_text)

    return kana_convert_list

def Romanji2Hiragana(text: str) :
    """ 
    convert romanji charecter to hiragana charecter
    
    Return :
        possible hiragana character list
    """
    with open('static/files/hiragana.json', encoding='utf-8') as file :
        hiragana = json.loads(file.read()) 
    syllables = text2syllables(text)
    ambiguous_list = extract_ambiguous_kana(syllables)
    convert_list = []
    for ambiguous_text in ambiguous_list :
        convert_list.append(map_kana(ambiguous_text, hiragana))
    return {'results': convert_list}

def Romanji2Katakana(text: str) :
    """ 
    convert romanji charecter to katakana charecter
    
    Return :
        possible katakana character list
    """
    with open('static/files/katakana.json', encoding='utf-8') as f :
        katakana = json.loads(f.read())
    syllables = text2syllables(text)
    ambiguous_list = extract_ambiguous_kana(syllables)
    convert_list = []
    for ambiguous_text in ambiguous_list :
        convert_list.append(map_kana(ambiguous_text, katakana))
    return {'results': convert_list}

def grammarChecker(text: str) :
    parser = GingerIt()
    corrected_text = parser.parse(text)
    return {'results': [corrected_text['result']]}
