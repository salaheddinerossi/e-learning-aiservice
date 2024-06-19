from fastapi import HTTPException
import openai
from dotenv import load_dotenv
import os
import json

# Load API key from .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)


def generate_quiz_from_transcription(transcription: str, additional_instructions: str, question_type: str) -> dict:

    message_templates = {
        'multiple-choice': f"""
            "You are a helpful assistant tasked with generating a quiz from the given transcription. Please create multiple-choice questions in the following JSON format, ensuring they are relevant to the content provided. Your goal is to make the quiz both engaging and informative, directly reflecting the key points and details from the transcription.
            Take into account these instructions if they exist; if not, ignore them: {additional_instructions}" .

            {{
              "questions": [
                {{
                  "prompt": "<question prompt>",
                  "options": ["<option 1>", "<option 2>", "<option 3>", "<option 4>"],
                  "correctAnswer": "<correct option>"
                }}
                // Encourage the assistant to add more questions based on the transcription.
              ]
            }}
        """,
        'true_false': """
            "You are a helpful assistant tasked with generating a quiz from the given transcription. Please create true/false questions in the following JSON format, ensuring they are relevant to the content provided. Your goal is to make the quiz both engaging and informative, directly reflecting the key points and details from the transcription."

            {{
              "questions": [
                {{
                  "prompt": "<true/false question prompt>",
                  "options": ["True", "False"],
                  "correctAnswer": "<correct option>"
                }}
                // Encourage the assistant to add more questions based on the transcription.
              ]
            }}
        """,
        'explanatory': """
            "You are a helpful assistant tasked with generating a quiz from the given transcription. Please create explanatory questions in the following JSON format, ensuring they are relevant to the content provided. Your goal is to make the quiz both engaging and informative, directly reflecting the key points and details from the transcription."

            {{
              "questions": [
                {{
                  "prompt": "<explanatory question prompt>",
                  "correctExplanation": "<correct explanation>"
                }}
                // Encourage the assistant to add more questions based on the transcription.
              ]
            }}
        """
    }

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
