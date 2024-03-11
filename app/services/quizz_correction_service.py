from fastapi import HTTPException
import openai
import json
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)

def correct_quiz(transcription: str, quiz: str, quiz_type: str) -> dict:
    # Define system prompts for different quiz types
    system_prompts = {
        'multiple-choice': (
            "You are a helpful assistant. Your task is to review and correct the multiple-choice quiz based on the provided content, "
            "ensuring the answers accurately reflect the information given. After reviewing each question, determine if the provided "
            "answer is exactly the same as the correct answer based on the content. Use a Boolean check for this comparison: return 'true' "
            "if the answers match (indicating the original answer was correct) and 'false' if they do not match (indicating the original "
            "answer was incorrect). Once all questions have been assessed, calculate a final score out of 10, with each correct answer "
            "contributing equally towards a perfect score. Return your response in a structured JSON format that includes the corrected "
            "quiz questions, their Boolean correctness, and the final grade. The expected JSON response format is: "
            "{\"evaluation\": {\"questions\": [{\"question\": \"Example question\", \"provided_answer\": \"A\", \"correct_answer\": \"A\", "
            "\"correctness\": true}], \"score_details\": {\"total_questions\": 1, \"correct_answers\": 1, \"incorrect_answers\": 0, "
            "\"score\": 10}, \"final_grade\": \"10 out of 10\"}}"
        ),
        'true_false': (
            "You are a helpful assistant. Your task is to review and correct the true/false quiz based on the provided content, ensuring the "
            "answers accurately reflect the information given. For each question, determine if the provided answer ('True' or 'False') matches "
            "the correct answer based on the content. Use a Boolean check for this comparison: return 'true' if the answers match (indicating the "
            "original answer was correct) and 'false' if they do not match (indicating the original answer was incorrect). After reviewing all "
            "questions, calculate a final score out of 10, with each correct answer contributing equally towards a perfect score. Return your "
            "response in a structured JSON format that includes the corrected quiz questions, their Boolean correctness, and the final grade. "
            "An example of the expected JSON response format is: "
            "{\"evaluation\": {\"questions\": [{\"question\": \"Is the Earth flat?\", \"provided_answer\": \"False\", \"correct_answer\": \"False\", "
            "\"correctness\": true}], \"score_details\": {\"total_questions\": 1, \"correct_answers\": 1, \"incorrect_answers\": 0, \"score\": 10}, "
            "\"final_grade\": \"10 out of 10\"}}"
        ),

        'explanatory': (
            "You are a helpful assistant. Your task for each explanatory question is to identify what is missing in the student's response "
            "and grade it out of 10. Consider the completeness, accuracy, and depth of the answer. Then, calculate the average score for "
            "the quiz. The response should be formatted in JSON, listing each question, the student's answer, the missing elements or "
            "feedback for improvement, the grade for each question, and the overall average score. Format your response as: "
            "{\"evaluation\": {\"questions\": [{\"question\": \"Example question\", \"student_answer\": \"Partial explanation\", "
            "\"feedback\": \"Missing key concept explanation.\", \"grade\": 7}], \"average_score\": \"7 out of 10\"}}"
        )
    }

    if quiz_type not in system_prompts:
        raise ValueError(f"Unsupported quiz type: {quiz_type}")

    try:
        prompt_message = {
            "role": "system",
            "content": system_prompts[quiz_type]
        }

        user_message = {
            "role": "user",
            "content": f"Content: {transcription}\n\nQuiz: {quiz}"
        }

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[prompt_message, user_message]
        )

        formatted_response = json.loads(response.choices[0].message.content)

        # For explanatory quizzes, process the response to calculate the average score if necessary
        if quiz_type == 'explanatory':
            # Implement any specific logic for processing explanatory quiz responses
            pass  # This is a placeholder for actual implementation

        return formatted_response
    except json.JSONDecodeError:
        raise ValueError("Failed to decode the response from OpenAI as JSON.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
