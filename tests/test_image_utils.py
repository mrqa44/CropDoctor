import unittest
import io
from PIL import Image
from utils.image_utils import process_image

class TestImageUtils(unittest.TestCase):
    def test_process_image_resizes_and_compresses(self):
        # Create a large dummy image (2000x2000 PNG)
        img = Image.new('RGB', (2000, 2000), color='green')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        original_bytes = img_byte_arr.getvalue()
        
        # Process it
        processed_bytes = process_image(original_bytes, max_size=(800, 800))
        
        # Verify it's significantly smaller
        self.assertLess(len(processed_bytes), len(original_bytes))
        
        # Verify it converted to JPEG and resized
        result_img = Image.open(io.BytesIO(processed_bytes))
        self.assertEqual(result_img.format, 'JPEG')
        self.assertLessEqual(result_img.size[0], 800)
        self.assertLessEqual(result_img.size[1], 800)

if __name__ == '__main__':
    unittest.main()
