from pydantic import BaseModel, Field
from typing import List

class DiagnosisSchema(BaseModel):
    is_plant: bool = Field(description="True if the image clearly contains a plant or leaf. False if it is blurry, unrecognizable, or not a plant.")
    plant_name: str = Field(description="The name of the plant or crop identified.")
    problem: str = Field(description="The most likely problem (disease, pest, nutrient deficiency, or 'looks healthy').")
    confidence: str = Field(description="Confidence level of the diagnosis: 'low', 'medium', or 'high'.")
    alternative_possibilities: List[str] = Field(description="1-2 other possible issues if confidence is not high.")
    symptoms: List[str] = Field(description="Visible symptoms the diagnosis is based on.")
    severity: str = Field(description="Severity of the issue: 'mild', 'moderate', or 'severe'.")
    treatment_organic: List[str] = Field(description="Low-cost and organic treatment steps. MUST be first line of defense.")
    treatment_chemical: List[str] = Field(description="Chemical treatment options, including safety notes and following label instructions.")
    prevention: List[str] = Field(description="Tips to prevent this issue in the future.")
    expert_advice: str = Field(description="When and why to consult a local agriculture expert.")

SYSTEM_INSTRUCTION = """
You are a highly skilled agronomist assistant named AgriLens. 
Your job is to analyze images of plant leaves and diagnose diseases, pests, or deficiencies.

CRITICAL RULES:
1. If the image is blurry, unrecognizable, or does not contain a plant, set 'is_plant' to false and provide a polite message in the 'problem' field asking for a better photo. Do not guess.
2. Keep language simple, plain, and accessible for farmers with low technical skill.
3. ALWAYS prioritize low-cost, organic treatments before suggesting chemical ones. 
4. When suggesting chemicals, add strong safety warnings ("Follow product labels carefully", "Wear protective gear"). NEVER suggest exact dosages.
5. You must output valid JSON matching the exact schema provided.
6. Translate all your text answers into the language requested by the user: {language}.

Context provided by user:
- Suspected crop type (if any): {crop_type}
"""
