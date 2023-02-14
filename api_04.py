import requests
import json
import time
from api_secrets import API_KEY_ASSEMBLYAI
import pprint


transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'
headers_assemblyai = {
    "authorization": API_KEY_ASSEMBLYAI,
    "content-type": "application/json"
}

def transcribe(audio_url, auto_chapters, speaker_labels):
    transcript_request = {
        'audio_url': audio_url,
        'auto_chapters': auto_chapters,
        "speaker_labels": speaker_labels
    }

    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers_assemblyai)
    pprint.pprint(transcript_response.json())
    return transcript_response.json()['id']


def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers_assemblyai)
    return polling_response.json()
    


def get_transcription_result_url(url, auto_chapters, speaker_labels):
    transcribe_id = transcribe(url, auto_chapters, speaker_labels)
    while True:
        data = poll(transcribe_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']

        print("waiting for 40 seconds")
        time.sleep(40)
            

def save_transcript(audio_url):
    episode_id = audio_url.split('/')[-1]
    data, error = get_transcription_result_url(audio_url, auto_chapters=True, speaker_labels=True)
    if data:
        filename = episode_id + '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    elif error:
        print("Error: ",error)
        return False

def get_clean_time(start_ms):
    seconds = int((start_ms / 1000) % 60)
    minutes = int((start_ms / (1000 * 60)) % 60)
    hours = int((start_ms / (1000 * 60 * 60)) % 24)
    if hours > 0:
        start_t = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        start_t = f'{minutes:02d}:{seconds:02d}'
        
    return start_t


def read_file(total_data, chunk_size=5242880):
    while True:
        data = total_data.read(chunk_size)
        if not data:
            break
        yield data

def upload_file(file):
    headers = {'authorization': API_KEY_ASSEMBLYAI}
    response = requests.post('https://api.assemblyai.com/v2/upload',headers=headers, data=read_file(file))
    return response.json()['upload_url']

