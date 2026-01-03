#!/usr/bin/env python3
"""
简单静态生成脚本（用于在没有 Jekyll 的环境下预览）
- 读取 _config.yml 的 site.title 和 site.description
- 读取 _posts/*.md（解析 YAML front matter）并将 Markdown 转为 HTML
- 复制 assets/ 到 _site/assets/
- 生成 _site/index.html 和 _site/posts/<slug>.html
"""
import os
import re
import shutil
import pathlib
import html
from datetime import datetime

try:
    import yaml
    import markdown
except Exception as e:
    print("需要依赖模块 pyyaml 和 markdown，请先运行: python -m pip install pyyaml markdown")
    raise

ROOT = pathlib.Path(__file__).parent
SITE_DIR = ROOT / '_site'
ASSETS_SRC = ROOT / 'assets'
POSTS_DIR = ROOT / '_posts'

slugify_re = re.compile(r'[^a-z0-9]+')

def slugify(s):
    s = s.lower()
    s = re.sub(r"[\s_]+", '-', s)
    s = re.sub(r'[^a-z0-9\-]+', '', s)
    s = re.sub(r'-{2,}', '-', s)
    return s.strip('-') or 'post'


def parse_front_matter(text):
    # split on leading YAML front matter
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2]
            meta = yaml.safe_load(fm) or {}
            return meta, body.lstrip('\n')
    return {}, text


def excerpt_html(html_text, length=200):
    # strip tags and truncate
    text = re.sub(r'<[^>]+>', '', html_text)
    text = text.replace('\n', ' ').strip()
    if len(text) > length:
        return text[:length].rstrip() + '...'
    return text


def build():
    # load config
    cfg_path = ROOT / '_config.yml'
    config = {}
    if cfg_path.exists():
        with cfg_path.open('r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}

    site_title = config.get('title', 'Site')
    site_desc = config.get('description', '')

    # collect posts
    posts = []
    if POSTS_DIR.exists():
        for p in sorted(POSTS_DIR.iterdir()):
            if p.suffix.lower() in ['.md', '.markdown']:
                text = p.read_text(encoding='utf-8')
                meta, body = parse_front_matter(text)
                md = markdown.markdown(body, extensions=['fenced_code', 'tables'])
                title = meta.get('title') or p.stem
                date = meta.get('date')
                if date:
                    try:
                        # try parse
                        dt = datetime.fromisoformat(str(date))
                        date_str = dt.strftime('%Y-%m-%d %H:%M')
                    except Exception:
                        date_str = str(date)
                else:
                    date_str = ''
                tags = meta.get('tags', []) or []
                slug = slugify(title + '-' + p.stem)
                posts.append({
                    'title': title,
                    'date': date_str,
                    'tags': tags,
                    'html': md,
                    'slug': slug,
                    'source': str(p)
                })

    # create site dir
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    # copy assets
    if ASSETS_SRC.exists():
        try:
            shutil.copytree(ASSETS_SRC, SITE_DIR / 'assets')
        except Exception:
            # maybe partially exists
            pass

    # write index.html
    index_html = []
    index_html.append('<!doctype html>')
    index_html.append('<html lang="zh-CN">')
    index_html.append('<head>')
    index_html.append('  <meta charset="utf-8">')
    index_html.append(f'  <title>{html.escape(site_title)}</title>')
    index_html.append('  <meta name="viewport" content="width=device-width, initial-scale=1">')
    index_html.append(f'  <meta name="description" content="{html.escape(site_desc)}">')
    # link css if exists
    css_path = 'assets/css/style.css'
    if (ROOT / css_path).exists() or (SITE_DIR / css_path).exists():
        index_html.append(f'  <link rel="stylesheet" href="{css_path}">')
    index_html.append('</head>')
    index_html.append('<body>')

    # header
    index_html.append('  <header class="site-header">')
    index_html.append('    <div class="wrapper">')
    index_html.append(f'      <a class="site-title" href="/">{html.escape(site_title)}</a>')
    index_html.append('    </div>')
    index_html.append('  </header>')

    # hero
    index_html.append('  <main class="page-content home">')
    index_html.append('    <div class="wrapper">')
    index_html.append('      <div class="hero">')
    index_html.append(f'        <h1 class="page-heading">{html.escape(site_title)}</h1>')
    index_html.append(f'        <p class="lead">{html.escape(site_desc)}</p>')
    index_html.append('      </div>')

    # posts list
    index_html.append('      <h2>最新笔记</h2>')
    index_html.append('      <ul class="post-list">')
    for post in posts:
        excerpt = excerpt_html(post['html'], 220)
        post_url = f'posts/{post["slug"]}.html'
        index_html.append('        <li>')
        index_html.append('          <article class="post-card">')
        if post['date']:
            index_html.append(f'            <div class="post-meta">{html.escape(post["date"])}</div>')
        index_html.append(f'            <h3 class="post-title"><a class="post-link" href="{post_url}">{html.escape(post["title"])}</a></h3>')
        index_html.append(f'            <div class="post-excerpt">{excerpt}</div>')
        if post['tags']:
            index_html.append('            <div class="post-tags">')
            index_html.append('              <ul class="tag-list">')
            for tag in post['tags']:
                index_html.append(f'                <li class="tag">{html.escape(str(tag))}</li>')
            index_html.append('              </ul>')
            index_html.append('            </div>')
        index_html.append('          </article>')
        index_html.append('        </li>')
    index_html.append('      </ul>')

    index_html.append('    </div>')
    index_html.append('  </main>')

    # footer
    index_html.append('  <footer class="site-footer">')
    index_html.append('    <div class="wrapper">')
    index_html.append(f'      <p>{html.escape(site_desc)}</p>')
    index_html.append('    </div>')
    index_html.append('  </footer>')

    index_html.append('</body>')
    index_html.append('</html>')

    (SITE_DIR / 'index.html').write_text('\n'.join(index_html), encoding='utf-8')

    # write posts
    posts_dir_out = SITE_DIR / 'posts'
    posts_dir_out.mkdir(parents=True, exist_ok=True)
    for post in posts:
        out = []
        out.append('<!doctype html>')
        out.append('<html lang="zh-CN">')
        out.append('<head>')
        out.append('  <meta charset="utf-8">')
        out.append(f'  <title>{html.escape(post["title"])}</title>')
        out.append('  <meta name="viewport" content="width=device-width, initial-scale=1">')
        if (ROOT / css_path).exists() or (SITE_DIR / css_path).exists():
            out.append(f'  <link rel="stylesheet" href="/assets/css/style.css">')
        out.append('</head>')
        out.append('<body>')
        out.append('  <header class="site-header">')
        out.append('    <div class="wrapper">')
        out.append(f'      <a class="site-title" href="/">{html.escape(site_title)}</a>')
        out.append('    </div>')
        out.append('  </header>')
        out.append('  <main class="page-content">')
        out.append('    <div class="wrapper">')
        if post['date']:
            out.append(f'      <div class="post-meta">{html.escape(post["date"])}</div>')
        out.append(f'      <h1>{html.escape(post["title"])}</h1>')
        out.append('      <div class="post-content">')
        out.append(post['html'])
        out.append('      </div>')
        if post['tags']:
            out.append('      <div class="post-tags">')
            out.append('        <ul class="tag-list">')
            for tag in post['tags']:
                out.append(f'          <li class="tag">{html.escape(str(tag))}</li>')
            out.append('        </ul>')
            out.append('      </div>')
        out.append('    </div>')
        out.append('  </main>')
        out.append('  <footer class="site-footer">')
        out.append('    <div class="wrapper">')
        out.append(f'      <p>{html.escape(site_desc)}</p>')
        out.append('    </div>')
        out.append('  </footer>')
        out.append('</body>')
        out.append('</html>')

        (posts_dir_out / f"{post['slug']}.html").write_text('\n'.join(out), encoding='utf-8')

    print('静态站点已生成到:', SITE_DIR)


if __name__ == '__main__':
    build()

