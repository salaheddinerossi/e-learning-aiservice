import os

import openai
import json

from dotenv import load_dotenv
from fastapi import HTTPException

# Load API key from .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)


def analyze_and_summarize_transcription(transcription: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. The transcript you're about to analyze comes from a video. Please offer three actionable pieces of advice to enhance the course content, presenting them politely with phrases like 'you might consider' or 'a beneficial approach could be'. For the summary, directly cover the key points made in the video, providing brief explanations where necessary, rather than prefacing with 'the video talks about'. Ensure the summary is comprehensive, highlighting main ideas and insights. Format your response in a structured manner: '{\"advice\": [\"Firstly, improving... might be beneficial\", \"Considering... could enhance\", \"Lastly, adopting... might provide new insights\"], \"summary\": \"Covering key topics such as..., which explains..., and also delves into..., offering insights on...\"}'"
                }
                ,
                {"role": "user", "content": transcription}
            ]
        )

        # Extracting the assistant's last response
        formatted_response = response.choices[0].message.content

        # Attempting to parse the formatted response as JSON
        parsed_response = json.loads(formatted_response)

        return {
            "advice": parsed_response["advice"],
            "summary": parsed_response["summary"],
            "transcription": transcription
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
