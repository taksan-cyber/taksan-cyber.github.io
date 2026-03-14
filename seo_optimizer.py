import os
import re

directories = ['.', 'posts', 'posts/drafts']
base_url = "https://taksan-cyber.github.io"

def get_keywords(filename):
    mapping = {
        'bermuda.html': 'バミューダトライアングル, 科学的説明, 魔の海域, Truth Seeker',
        'pyramid.html': 'ピラミッド, 宇宙人説, 古代エジプト, 土木技術, Truth Seeker',
        'secret-societies.html': '秘密結社, イルミナティ, フリーメイソン, Truth Seeker',
        'black-eyed-children.html': 'Black Eyed Children, 都市伝説, 黒い瞳の子供たち, Truth Seeker',
        'ai-conspiracy.html': 'AI, 陰謀論, 人工知能, Truth Seeker',
        'ancient-tech.html': 'オーパーツ, 古代技術, 超古代文明, Truth Seeker',
        'freemason.html': 'フリーメイソン, 都市伝説, 歴史, Truth Seeker',
        'moon-landing.html': '月面着陸, アポロ計画, 捏造説, Truth Seeker',
        'nostradamus.html': 'ノストラダムス, 予言, 大王, Truth Seeker',
        'psychology-conspiracy.html': '陰謀論, 心理学, 社会学, Truth Seeker',
        'unsolved-cases.html': '未解決事件, ミステリー, Truth Seeker',
        'cicada-3301.html': 'Cicada 3301, 暗号, ネットミステリー, Truth Seeker',
        'dead-internet-theory.html': 'デッドインターネットセオリー, AI, ネットの終焉, Truth Seeker',
        'mandela-effect.html': 'マンデラエフェクト, 異世界, 記憶違い, Truth Seeker',
        'missing-411.html': '神隠し, 行方不明, Missing 411, Truth Seeker',
        'polybius.html': 'ポリビアス, アーケードゲーム, 都市伝説, Truth Seeker',
        'the-hum.html': 'The Hum, 謎の低周波, 怪音, Truth Seeker',
        'about.html': 'Truth Seeker, このサイトについて, 都市伝説, 論理的検証',
        'index.html': 'Truth Seeker, 都市伝説, 論理的検証, ブログ'
    }
    return mapping.get(filename, 'Truth Seeker, 都市伝説, 論理的検証, ミステリー')

for d in directories:
    if not os.path.exists(d): continue
    for f in os.listdir(d):
        if not f.endswith('.html'): continue
        if f == 'template.html': continue # skip template
        
        filepath = os.path.join(d, f)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            
        original_content = content
        
        # Extract title and description
        title_match = re.search(r'<title>(.*?)</title>', content)
        desc_match = re.search(r'<meta name="description" content="(.*?)">', content)
        
        title = title_match.group(1) if title_match else "Truth Seeker"
        desc = desc_match.group(1) if desc_match else "Truth Seeker Articles"
        
        # Construct path for url
        rel_path = f if d == '.' else f"{d}/{f}".replace('\\', '/')
        page_url = f"{base_url}/{rel_path}"
        
        # 1. Canonical
        if '<link rel="canonical"' not in content:
            canonical_tag = f'\n    <link rel="canonical" href="{page_url}">'
            content = content.replace('</title>', f'</title>{canonical_tag}')
            
        # 2. Keywords
        if '<meta name="keywords"' not in content:
            keywords = get_keywords(f)
            kw_tag = f'\n    <meta name="keywords" content="{keywords}">'
            if '<meta name="description"' in content:
                content = content.replace('name="description"', f'name="keywords" content="{keywords}">\n    <meta name="description"')
            else:
                content = content.replace('</title>', f'</title>{kw_tag}')
                
        # 3. Twitter OGP Missing tags
        if '<meta name="twitter:card"' in content and '<meta name="twitter:title"' not in content:
            tw_tags = f'\n    <meta name="twitter:title" content="{title}">\n    <meta name="twitter:description" content="{desc}">'
            img_match = re.search(r'<meta property="og:image" content="(.*?)">', content)
            if img_match:
                tw_tags += f'\n    <meta name="twitter:image" content="{img_match.group(1)}">'
            content = content.replace('<meta name="twitter:card" content="summary_large_image">', f'<meta name="twitter:card" content="summary_large_image">{tw_tags}')
            
        # 4. JSON-LD
        if 'application/ld+json' not in content:
            # We insert it right before </head>
            json_ld = f"""
    <!-- Structured Data -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{title}",
      "description": "{desc}",
      "author": {{
        "@type": "Organization",
        "name": "Truth Seeker"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "Truth Seeker"
      }},
      "mainEntityOfPage": {{
        "@type": "WebPage",
        "@id": "{page_url}"
      }}
    }}
    </script>
"""
            content = content.replace('</head>', f'{json_ld}</head>')

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated SEO tags in: {filepath}")

print("SEO update completed.")
