import unittest
from unittest.mock import patch, MagicMock
from prompts import DiagnosisSchema

class TestGeminiClient(unittest.TestCase):
    
    @patch('services.gemini_client.genai.Client')
    def test_analyze_plant_image_success(self, MockClient):
        """Tests that the client successfully extracts and returns the JSON payload."""
        # Setup mock behavior
        mock_instance = MockClient.return_value
        mock_response = MagicMock()
        
        # Mock the parsed model dump from Pydantic
        expected_output = {
            "is_plant": True,
            "plant_name": "Wheat",
            "problem": "Leaf Rust",
            "confidence": "high",
            "alternative_possibilities": [],
            "symptoms": ["Orange spots on leaves"],
            "severity": "moderate",
            "treatment_organic": ["Remove infected leaves"],
            "treatment_chemical": ["Apply appropriate fungicide"],
            "prevention": ["Plant resistant varieties"],
            "expert_advice": "Consult if it spreads rapidly."
        }
        mock_response.parsed.model_dump.return_value = expected_output
        mock_instance.models.generate_content.return_value = mock_response

        # Import locally to apply patch
        from services.gemini_client import analyze_plant_image
        from PIL import Image
        import io
        
        # Create a tiny dummy image
        img = Image.new('RGB', (10, 10))
        fp = io.BytesIO()
        img.save(fp, format='JPEG')
        
        # Call the function
        result = analyze_plant_image(fp.getvalue())
        
        # Assertions
        self.assertTrue(result["is_plant"])
        self.assertEqual(result["plant_name"], "Wheat")
        self.assertEqual(result["problem"], "Leaf Rust")
        self.assertIn("treatment_organic", result)

if __name__ == '__main__':
    unittest.main()
