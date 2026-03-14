import os
import re

# 1. Revert HTML files to point back to .png
directories = ['.', 'posts', 'posts/drafts']

for d in directories:
    if not os.path.exists(d): continue
    for f in os.listdir(d):
        if not f.endswith('.html'): continue
        
        filepath = os.path.join(d, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            
        original_content = content
        
        # Replace .webp image references back to .png
        content = re.sub(r'(assets/.*?)\.webp', r'\1.png', content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Reverted image links in html: {filepath}")

# 2. Delete old .png and rename .webp to .png
assets_dirs = ['assets', 'assets/posts']
base_dir = os.path.dirname(os.path.abspath(__file__))

for d in assets_dirs:
    full_d = os.path.join(base_dir, d)
    if not os.path.exists(full_d): continue
    
    # First, delete all old .png files
    for f in os.listdir(full_d):
        if f.endswith('.png'):
            filepath = os.path.join(full_d, f)
            os.remove(filepath)
            print(f"Deleted old image: {filepath}")
            
    # Then, rename all new .webp files to .png
    for f in os.listdir(full_d):
        if f.endswith('.webp'):
            filepath = os.path.join(full_d, f)
            new_filepath = os.path.join(full_d, f.replace('.webp', '.png'))
            os.rename(filepath, new_filepath)
            print(f"Renamed {filepath} to {new_filepath}")

print("Image cleanup and rename completed.")
