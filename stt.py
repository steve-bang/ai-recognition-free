import speech_recognition as sr
from flask import Flask, request, jsonify
from textblob import TextBlob
from googletrans import Translator
from pydub import AudioSegment
import os


app = Flask(__name__)

def convert_to_wav(audio_file):
    if audio_file.filename.endswith('.mp3'):
        audio = AudioSegment.from_mp3(audio_file)
        wav_filename = 'temp_audio.wav'
        audio.export(wav_filename, format='wav')
        return wav_filename
    elif audio_file.filename.endswith('.wav'):
        return audio_file.filename
    else:
        raise ValueError('Unsupported file format')

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    try:
        audio_file_path = convert_to_wav(audio_file)
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text
    except Exception as e:
        print("Error:", e)
        return 'Cannot recognize audio file'

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text_api():
    try:
        audio_file = request.files['audio']
        # Save the audio file temporarily (optional)
        # audio_file.save('temp_audio.wav')

        text = speech_to_text(audio_file)
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/aai', methods=['POST'])
def speech_to_text_aai():
    try:
        audio_url = request.form.get('audio_url')
        
        aai.settings.api_key = 'KEY_AAI'
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_url)
        text = transcript.text
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/keywords', methods=['POST'])
def main_keywords():
    try:
        paragraph = request.form.get('text')
            # Create a TextBlob object
        blob = TextBlob(paragraph)
    
    # Extract noun phrases (main keywords) from the paragraph
        noun_phrases = blob.noun_phrases

    # Use a set to automatically remove duplicates
        unique_keywords = list(set(noun_phrases))
    
        return jsonify({'keywords': unique_keywords})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/translation', methods=['POST'])
def translate():
    try:
        content = request.form.get('content')
        language_code = request.form.get('languageCode')
        result = None
        if content is not None:
            translator = Translator()
            translated_content = translator.translate(content, dest=language_code)
            result = translated_content.text
        return jsonify({'text': result})
    except Exception as e:
        return jsonify({'text': 'The language code is not supported with {language_code}'.format(language_code=language_code)})


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=8801)
