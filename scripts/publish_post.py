import os
import shutil
import glob
from datetime import datetime
import re

# Paths
DRAFTS_DIR = 'posts/drafts'
POSTS_DIR = 'posts'
INDEX_FILE = 'index.html'
SITEMAP_FILE = 'sitemap.xml'
BASE_URL = 'https://taksan-cyber.github.io'

def get_meta_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Extract metadata from comments or HTML tags
    title_match = re.search(r'<!-- TITLE: (.*?) -->', content)
    if not title_match:
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    
    desc_match = re.search(r'<!-- DESCRIPTION: (.*?) -->', content)
    if not desc_match:
        desc_match = re.search(r'<meta name="description" content="(.*?)">', content, re.IGNORECASE)
    
    cat_match = re.search(r'<!-- CATEGORY: (.*?) -->', content)
    if not cat_match:
        # Fallback category extraction from tag
        cat_tag_match = re.search(r'<span class="category-tag">.*?• (.*?)</span>', content, re.IGNORECASE)
        category = cat_tag_match.group(1) if cat_tag_match else "Intelligence Report"
    else:
        category = cat_match.group(1)
    
    title = title_match.group(1).split('|')[0].strip() if title_match else "New Intelligence Report"
    desc = desc_match.group(1) if desc_match else "New analysis available."
    
    # Try to find a date or just use today
    date = datetime.now().strftime('%Y-%m-%d')
    return title, desc, date, category

def publish_oldest_draft():
    drafts = sorted(glob.glob(os.path.join(DRAFTS_DIR, '*.html')))
    if not drafts:
        print("No drafts found.")
        return None

    next_draft = drafts[0]
    filename = os.path.basename(next_draft)
    dest_path = os.path.join(POSTS_DIR, filename)

    print(f"Publishing {filename}...")
    shutil.move(next_draft, dest_path)
    return filename

def update_index(filename, title, desc, date, category):
    print(f"Updating {INDEX_FILE}...")
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the post-grid and insert at the top
    new_post_html = f"""
            <article class="card scroll-reveal">
                <div class="card-content">
                    <span class="card-meta">{category} • {date}</span>
                    <h2>{title}</h2>
                    <p>{desc}</p>
                    <a href="posts/{filename}" class="read-more">記事を読む</a>
                </div>
            </article>"""
    
    # Simple regex insert after the grid starts
    content = re.sub(r'(<div class="grid">)', r'\1' + new_post_html, content)

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

def update_sitemap(filename, date):
    print(f"Updating {SITEMAP_FILE}...")
    with open(SITEMAP_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_entry = f"""    <url>
        <loc>{BASE_URL}/posts/{filename}</loc>
        <lastmod>{date}</lastmod>
        <priority>0.80</priority>
    </url>\n"""

    # Insert before the closing </urlset>
    for i, line in enumerate(lines):
        if '</urlset>' in line:
            lines.insert(i, new_entry)
            break

    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)

if __name__ == "__main__":
    published = publish_oldest_draft()
    if published:
        title, desc, date, category = get_meta_info(os.path.join(POSTS_DIR, published))
        update_index(published, title, desc, date, category)
        update_sitemap(published, date)
        print("Done.")
