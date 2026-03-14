import os
from PIL import Image

def compress_images(directory, quality=75):
    supported_formats = ('.png', '.jpg', '.jpeg')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_formats):
                filepath = os.path.join(root, file)
                try:
                    img = Image.open(filepath)
                    original_size = os.path.getsize(filepath)
                    
                    if file.lower().endswith('.png'):
                        # Using optimize=True for PNG
                        img.save(filepath, optimize=True)
                    else:
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")
                        img.save(filepath, quality=quality, optimize=True)
                    
                    new_size = os.path.getsize(filepath)
                    print(f"Compressed {file}: {original_size // 1024}KB -> {new_size // 1024}KB (Saved: {(original_size - new_size) // 1024}KB)")
                except Exception as e:
                    print(f"Error compressing {filepath}: {e}")

assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
compress_images(assets_dir)
