from openai import OpenAI

# Initialize the OpenAI client with your API key
client = OpenAI(api_key='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')


def transcribe_audio_to_text_with_timestamps(audio_path: str) -> str:
    try:
        with open(audio_path, "rb") as audio_file:
            # Request transcription in SRT format
            transcription_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="srt"
            )

            # Assuming the API call is successful and returns the SRT string directly
            transcription_srt = transcription_response  # This might need to be adjusted based on the actual method to access the response content

            return transcription_srt

    except Exception as e:
        # Log the specific error for debugging purposes
        print(f"Error during transcription: {e}")
        # Propagate a more specific error message if possible
        raise ValueError(f"An error occurred during transcription: {e}") from e

def transcribe_audio_to_text_with_openai_api(audio_path: str) -> str:

    audio_file = open(audio_path, "rb")

    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

    return transcription.text
