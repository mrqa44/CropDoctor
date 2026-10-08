import os
from google import genai
from google.genai import types
from PIL import Image
import io
import json

from prompts import DiagnosisSchema, SYSTEM_INSTRUCTION

import time

def analyze_plant_image(image_bytes: bytes, crop_type: str = "Not sure", language: str = "English", retries: int = 3) -> dict:
    """
    Analyzes the plant image using the Gemini API and returns a structured JSON diagnosis.
    Includes exponential backoff for rate limits.
    """
    client = genai.Client() 
    image = Image.open(io.BytesIO(image_bytes))
    instruction = SYSTEM_INSTRUCTION.format(language=language, crop_type=crop_type)
    
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=["Analyze this plant image and provide a diagnosis.", image],
                config=types.GenerateContentConfig(
                    system_instruction=instruction,
                    response_mime_type="application/json",
                    response_schema=DiagnosisSchema,
                    temperature=0.2, 
                )
            )
            
            if response.parsed:
                return response.parsed.model_dump()
            else:
                return json.loads(response.text)
                
        except Exception as e:
            error_msg = str(e)
            # Retry on rate limits (429) or server errors (500, 503)
            if any(code in error_msg for code in ["429", "503", "500"]):
                if attempt < retries - 1:
                    time.sleep(2 ** attempt) # Exponential backoff: 1s, 2s...
                    continue
            return {"error": f"Failed to analyze image after {attempt+1} attempts: {error_msg}"}

def ask_agronomist(question: str, context: dict, language: str = "English") -> str:
    """
    Follow-up chat feature where the farmer can ask specific questions about the diagnosis.
    """
    client = genai.Client()
    prompt = f"""
    You are AgriLens, an expert agronomist. The user has a follow-up question about their plant.
    
    Previous Diagnosis Context:
    - Plant: {context.get('plant_name')}
    - Problem: {context.get('problem')}
    - Treatments Suggested: {', '.join(context.get('treatment_organic', []))}
    
    User's Question: {question}
    
    Answer strictly in {language}. Keep it brief, friendly, practical, and highly relevant to a small-scale farmer.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Sorry, I couldn't process your question right now. Error: {str(e)}"

