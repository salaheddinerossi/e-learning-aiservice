import json
import os
from fastapi import HTTPException

from typing import List

import openai

from dotenv import load_dotenv
api_key = os.getenv('OPENAI_API_KEY')

load_dotenv()
from pydantic import BaseModel

from app.Models.CorrectionResponse import CorrectionResponse
from app.Models.StringQuestionDto import StringQuestionDto
client = openai.OpenAI(api_key=api_key)





def correct_multiple_choice_quiz(transcription: str, questions: List[StringQuestionDto]) -> CorrectionResponse:
    # Define the updated system prompt for multiple-choice quizzes
    system_prompt = (
        "Based on the student's responses to a set of explanatory questions and the provided transcription, assess their overall understanding. "
        "Do not correct the answers explicitly. Instead, offer general advice that can help improve their understanding and skills, "
        "focusing on areas for review and study, key concepts to revisit, and strategies for learning and reinforcement. "
        "The advice should guide the student towards resources or practices that strengthen their knowledge in areas where they showed uncertainty "
        "or misunderstanding and encourage exploration of topics that could enhance their programming abilities and confidence. "
        "Conclude your evaluation with a JSON-formatted response, including 'advices' as a list of strings for the suggestions "
        "and a 'mark' key for a numerical score from 0 to 10 reflecting the student's grasp of the material. "
        "Ensure the advice supports positive learning outcomes and fosters a supportive tone."
    )

    # Format the questions into a string that matches the expected input format for the system prompt
    questions_formatted = "\n\n".join(
        [f"Question {i+1}: {q.question}\nProvided Answer: {q.answer}\nCorrect Answer: {q.correctAnswer}" for i, q in enumerate(questions)]
    )

    # Construct the prompt message
    prompt_message = f"{system_prompt}\n\nTranscription: {transcription}\n\n{questions_formatted}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": prompt_message
                }
            ]
        )

        # Assuming the AI's response is a list of advices as expected
        advices = response.choices[0].message.content.strip().split("\n")
        return CorrectionResponse(advices=advices)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class BooleanQuestionDto(BaseModel):
    id: int
    question: str
    answer: bool
    correctAnswer: bool

def correct_true_false_quiz(transcription: str, questions: List[BooleanQuestionDto]) -> CorrectionResponse:
    # Define the system prompt for true/false quizzes
    system_prompt = (
        "After analyzing the student's responses to a Python programming quiz with true/false questions, generate general advice that can "
        "help improve their understanding and skills. The quiz covered basic to intermediate concepts. "
        "Based on the types of questions answered incorrectly, suggest areas for review and study without referencing specific questions. "
        "Offer strategies for learning and reinforcement. Provide advice that strengthens their knowledge in areas where they showed uncertainty. "
        "Maintain a positive and supportive tone."
    )

    # Format the questions for the system prompt
    questions_formatted = "\n\n".join(
        [f"Question {i+1}: {q.question}\nProvided Answer: {'True' if q.answer else 'False'}\nCorrect Answer: {'True' if q.correctAnswer else 'False'}"
         for i, q in enumerate(questions)]
    )

    # Construct the prompt message
    prompt_message = f"{system_prompt}\n\nTranscription: {transcription}\n\n{questions_formatted}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": prompt_message
                }
            ]
        )

        # Process the response from OpenAI to extract the advice
        advices = response.choices[0].message.content.strip().split("\n")
        return CorrectionResponse(advices=advices)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





class ExplanatoryQuestionDto(BaseModel):
    id: int
    question: str
    answer: str
    correctAnswer: str


class ExplanatoryQuestionsCorrectionResponse(BaseModel):
    advices: List[str] = []
    mark: float


def correct_explanatory_quiz(transcription: str,
                             questions: List[ExplanatoryQuestionDto]) -> ExplanatoryQuestionsCorrectionResponse:
    # Define the system prompt for explanatory quizzes
    system_prompt = (
        "After analyzing the student's responses to a set of explanatory questions based on the provided transcription, "
        "generate general advice to help improve their understanding and skills. Conclude with a numerical score from 0 to 10 "
        "to reflect the overall quality of the student's answers and their grasp of the concepts discussed. "
        "Provide your response in JSON format, including 'advices' as a list of strings and 'mark' as the numerical score."
    )

    # Format the questions for the system prompt
    questions_formatted = "\n\n".join(
        [f"Question {i + 1}: {q.question}\nStudent's Answer: {q.answer}" for i, q in enumerate(questions)]
    )

    # Construct the prompt message
    prompt_message = f"{system_prompt}\n\nTranscription: {transcription}\n\n{questions_formatted}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": prompt_message
                }
            ]
        )

        # Parse the AI's response, expected to be in JSON format
        correction_data = json.loads(response.choices[0].message.content)

        advices = correction_data.get("advices", [])
        mark = correction_data.get("mark", 0.0)  # Ensure mark is treated as a float

        return ExplanatoryQuestionsCorrectionResponse(advices=advices, mark=mark)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to decode AI response as JSON.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
