import os
from PIL import Image

def optimize_images_webp(directory, quality=80):
    supported_formats = ('.png', '.jpg', '.jpeg')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_formats):
                filepath = os.path.join(root, file)
                try:
                    img = Image.open(filepath)
                    original_size = os.path.getsize(filepath)
                    
                    # Convert to WebP
                    webp_path = os.path.splitext(filepath)[0] + '.webp'
                    
                    if img.mode in ("RGBA", "P") and not file.lower().endswith('.png'):
                        img = img.convert("RGB")
                    
                    # Save as WebP
                    img.save(webp_path, 'WEBP', quality=quality, method=6)
                    
                    new_size = os.path.getsize(webp_path)
                    print(f"Converted {file} to WebP: {original_size // 1024}KB -> {new_size // 1024}KB (Saved: {(original_size - new_size) // 1024}KB)")
                except Exception as e:
                    print(f"Error converting {filepath}: {e}")

assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
optimize_images_webp(assets_dir)
