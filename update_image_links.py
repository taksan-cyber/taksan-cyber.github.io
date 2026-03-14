import os
import re

directories = ['.', 'posts', 'posts/drafts']

for d in directories:
    if not os.path.exists(d): continue
    for f in os.listdir(d):
        if not f.endswith('.html'): continue
        
        filepath = os.path.join(d, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            
        original_content = content
        
        # Replace .png image references in assets with .webp
        # Specifically targeting anything containing 'assets/' and ending in .png
        content = re.sub(r'(assets/.*?)\.png', r'\1.webp', content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated image links in: {filepath}")

print("Image link update completed.")
