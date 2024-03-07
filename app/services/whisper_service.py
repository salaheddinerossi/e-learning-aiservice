import openai
from openai import OpenAI

client = OpenAI(api_key='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')

def transcribe_audio_to_text_with_openai_api(audio_path: str) -> str:

    audio_file = open(audio_path, "rb")

    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

    return transcription.text
