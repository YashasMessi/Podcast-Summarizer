import streamlit as st
import glob
import json
from api_04 import save_transcript, get_clean_time, read_file, upload_file

st.title("Podcast Summarization")
ch = st.sidebar.selectbox("Source", options=["url", 'upload'])

if ch =="url":
    url = st.text_input("Enter your url:")
    button = st.button("Summarize", on_click=save_transcript, args=(url,))

    if button:
        filename = url.split('/')[-1]+".json"

elif ch == 'upload':
    file = st.file_uploader("Upload", type=['mp3', 'mp4', 'wav'])
    button = st.button("Summarize")
    if button:
        file_url = upload_file(file)
        status = save_transcript(file_url)
        if status:
            filename = file_url.split('/')[-1]+".json"

else:
    print("Something happened!")
    filename=None
    button = False

if button:
    with open(filename, 'r') as f:
        data = json.load(f)

        chapters = data['chapters']
        convo = data['utterances']

        summary = ''''''
        conversation = ''''''

        for chp in chapters:
            heading = chp['gist'] + ' - ' + get_clean_time(chp['start'])
            summary += heading + '\n'
            summary += chp['summary'] + '\n\n'

            with st.expander(heading):
                st.write(chp['summary'])


        with st.expander("Conversation"):
            for sp in convo:
                conversation = "Speaker " + sp['speaker']+": " + sp['text']+ '\n'
                st.write(conversation)

        # _ = st.sidebar.download_button("Download Summary", summary, file_name="summary.txt")
        # _ = st.sidebar.download_button("Download Conversation", conversation, file_name="conversation.txt")
        _ = st.download_button("Download Summary", summary, file_name=filename.split('.')[0]+"_summary.txt")