import os
import json
from typing import Dict, Any
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


def generate_challenge_with_ai(difficulty:str) -> Dict[str, Any]:
    model = OllamaLLM(model="mistral", temperature=0.5)

    system_prompt = """
    Your task is to generate a coding conceptual question can be of python, java, C++ or others, with multiple choice answers Each time, 
    pick a different topic and do not repeat previous questions.
    The question should be appropiate for the specified difficulty level.

    For easy questions: Focus on basic common programming concepts.
    For medium questions: Cover intermediate concepts like data structures, algorithms, or concepts of complex algorithms.

    Return the challenge in the following JSON structure:
    {{
        "title": "The question title, and the question itself",
        "options": ["Option 1","Option 2","Option 3","Option 4"],
        "correct_answer_id": 0, //index of the correct answer (0-3),
        "explanation": "Detailed explanation of why the correct answer is right"
    }}

    Make sure the options are plausible but with only one clearly correct answer
    """
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", f"Generate a {difficulty} difficulty coding challenge")
        ])
        chain = prompt | model
        response = chain.invoke({"difficulty": difficulty})
        response_json = json.loads(response)
        required_keys = ["title", "options", "correct_answer_id", "explanation"]
        for key in required_keys:
            if key not in response_json:
                raise ValueError(f"Missing key in response: {key}")
        return response_json    
    except Exception as e:
        print(f"Error: {e}")
        return {
            "title": "What is the output of print(2 + 2)?",
            "options": ["3", "4", "5", "22"],
            "correct_answer_id": 1,
            "explanation": "2 + 2 equals 4."
        }
    
if __name__ == "__main__":
    result = generate_challenge_with_ai("easy")
    print(result)