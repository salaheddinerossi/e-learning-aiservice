from fastapi import HTTPException
import openai
from dotenv import load_dotenv
import os
import json

# Load API key from .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)


def generate_quiz_from_transcription(transcription: str, question_type: str) -> dict:
    message_templates = {
        'multiple-choice': "Your multiple choice template...",
        'true_false': "Your true/false template...",
        'explanatory': "Your explanatory questions template..."
    }

    if question_type not in message_templates:
        raise ValueError("Invalid question type provided.")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": message_templates[question_type]
                },
                {"role": "user", "content": transcription}
            ]
        )

        # Extract the assistant's response
        formatted_response = response.choices[0].message.content

        # Attempting to parse the formatted response as JSON
        quiz_questions = json.loads(formatted_response)

        return quiz_questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
