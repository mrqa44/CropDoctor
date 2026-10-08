from PIL import Image
import io

def process_image(image_bytes: bytes, max_size: tuple = (800, 800)) -> bytes:
    """
    Resizes and compresses the image to save bandwidth and API quota.
    """
    img = Image.open(io.BytesIO(image_bytes))
    
    # Convert to RGB to avoid issues with PNG transparency when saving as JPEG
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    # Resize using high-quality downsampling
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    output = io.BytesIO()
    # Compress as JPEG
    img.save(output, format='JPEG', quality=85)
    return output.getvalue()
