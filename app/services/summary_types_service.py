import os
import openai
import json

from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables and API key
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)


def generate_summaries(transcription: str, summary_type: str, additional_instructions: str = '') -> dict:
    try:
        # Use f-strings for dynamic string construction
        system_message = f"""You are a helpful assistant. The transcript you're about to summarize comes from a video.
        Please generate a {summary_type} summary of the content. {additional_instructions}
        Ensure the summary captures the essence of the video, highlighting main ideas and insights.
        Format your response in a structured json format: '{{"summary": "Your summary here"}}'"""

        # Call the OpenAI API with the constructed system message and user's transcription
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": transcription}
            ]
        )

        # Extracting the assistant's last response
        formatted_response = response.choices[0].message.content

        # Attempting to parse the formatted response as JSON
        parsed_response = json.loads(formatted_response)

        # Access the "summary" key in the parsed JSON response
        if "summary" not in parsed_response:
            raise KeyError("The key 'summary' was not found in the API response.")
        summary = parsed_response["summary"]
    except json.JSONDecodeError as json_err:
        raise HTTPException(status_code=500, detail=f"Failed to decode JSON from API response: {json_err}")
    except KeyError as key_err:
        raise HTTPException(status_code=500, detail=f"Key error in parsing API response: {key_err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "summary": summary,
    }
