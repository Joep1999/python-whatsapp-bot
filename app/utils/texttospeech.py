from google.cloud import texttospeech
from google.oauth2 import service_account
import os
import json

# Load credentials JSON from env var
GOOGLE_CREDENTIALS = json.loads(os.environ["GOOGLE_CREDENTIALS"])

# Build credentials object
credentials = service_account.Credentials.from_service_account_info(GOOGLE_CREDENTIALS)

# Initialize client
client = texttospeech.TextToSpeechClient(credentials=credentials)

def text_to_speech_converter(text, filename="output.mp3"):
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB",
        name="en-GB-Standard-A",
    )

    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    with open(filename, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio was written to {filename}')

    return filename
