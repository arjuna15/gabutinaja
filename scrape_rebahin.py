#!/usr/bin/env python3
"""
Scrape Indonesian movies & series from rebahinxxi3.mom and merge into catalog.json
"""
import urllib.request
import urllib.error
import json
import re
import os
import time
from concurrent.futures import ThreadPoolExecutor

CATALOG_PATH = "/home/junancok/Downloads/movie-stream-app/catalog.json"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
}

PATTERN = re.compile(
    r'<div data-movie-id=[\'\"](?P<id>[0-9]+)[\'\"]\s+class=[\'\"]ml-item[\'\"].*?'
    r'<a href=[\'\"](?P<url>https?://rebahinxxi3\.mom/(?:series/|)[^\'\"]+)[\'\"].*?'
    r'title=[\'\"](?P<title>[^\'\"]+)[\'\"].*?'
    r'(?:<span class=[\'\"]mli-rating[\'\"][^>]*>.*?([0-9\.]+)\s*</span>|).*?'
    r'(?:src=[\'\"](?P<img1>https?://[^\'\"]+)[\'\"]|data-original=[\'\"](?P<img2>https?://[^\'\"]+)[\'\"])',
    re.DOTALL
)

def clean_title_and_year(raw_title, url):
    title = raw_title.replace('&amp;', '&').replace('&#8211;', '-').replace('&#038;', '&').replace('&quot;', '"').replace('&#39;', "'")
    
    # Try finding year in title
    year_match = re.search(r'[\(（]\s*(\d{4})\s*[\)）]', title)
    if year_match:
        year = year_match.group(1)
    else:
        slug_year = re.search(r'-(\d{4})(?:-sub-indo|/|$)', url)
        year = slug_year.group(1) if slug_year else '2026'

    # Clean title
    clean_t = re.sub(r'[\(（]\s*\d{4}\s*[\)）]', '', title)
    clean_t = re.sub(r'(?i)\s*sub\s+indo\s*', '', clean_t)
    clean_t = clean_t.strip(' -:')
    return clean_t, year

def get_genres(title, is_series):
    lower = title.lower()
    genres = [18] # Drama default
    if any(k in lower for k in ['hantu', 'setan', 'pocong', 'kuntilanak', 'sengkolo', 'tumbal', 'santet', 'susuk', 'iblis', 'kutukan', 'jenazah', 'mayat', 'misteri', 'horor', 'darah', 'mati', 'arwah', 'teror']):
        genres.append(27) # Horror
    if any(k in lower for k in ['cinta', 'hati', 'jodoh', 'nikah', 'istri', 'suami', 'pacar', 'sayang', 'romansa', 'rindu', 'asmara', 'selingkuh']):
        genres.append(10749) # Romance
    if any(k in lower for k in ['komedi', 'lucu', 'warkop', 'gokil', 'ngakak', 'bodor', 'kocak']):
        genres.append(35) # Comedy
    if any(k in lower for k in ['aksi', 'tarung', 'bela', 'jagoan', 'perang', 'gangster']):
        genres.append(28) # Action
    return list(set(genres))

def fetch_page_with_retry(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', errors='ignore')
            matches = PATTERN.finditer(html)
            items = []
            for m in matches:
                d = m.groupdict()
                img = d.get('img2') or d.get('img1') or ''
                is_series = '/series/' in d['url']
                clean_title, year = clean_title_and_year(d['title'], d['url'])
                
                raw_rating = m.group(4)
                rating = 8.2
                if raw_rating:
                    try:
                        r_val = float(raw_rating)
                        rating = round(r_val / 10.0, 1) if r_val > 10.0 else round(r_val, 1)
                    except:
                        pass

                genre_ids = get_genres(clean_title, is_series)
                item_type = 'series' if is_series else 'movie'
                overview = (
                    f"Nonton serial Indonesia {clean_title} ({year}) lengkap episode terbaru streaming Full HD sub Indo gratis tanpa iklan popup di gabutin aja."
                    if is_series else
                    f"Nonton dan streaming film bioskop Indonesia {clean_title} ({year}) sub Indo kualitas 1080p Full HD gratis di gabutin aja."
                )

                items.append({
                    'id': 90000000 + int(d['id']),
                    'rebahin_id': int(d['id']),
                    'title': clean_title,
                    'type': item_type,
                    'release_date': year,
                    'vote_average': rating,
                    'overview': overview,
                    'poster_path': img,
                    'backdrop_path': img,
                    'genre_ids': genre_ids,
                    'rebahin_url': d['url'],
                    'rebahin_play_url': (d['url'] + 'watch') if is_series else (d['url'] + 'play'),
                    'country': 'ID',
                    'is_indonesian': True,
                    'source': 'rebahin'
                })
            return items
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1 + attempt)
            else:
                print(f"Failed to fetch {url} after {retries} attempts: {e}")
                return []

def scrape_all_rebahin_indonesia():
    urls = []
    # 62 pages of country/indonesia
    for p in range(1, 63):
        urls.append(f"https://rebahinxxi3.mom/country/indonesia/page/{p}/" if p > 1 else "https://rebahinxxi3.mom/country/indonesia/")
    # 15 pages of genre/series-indonesia
    for p in range(1, 16):
        urls.append(f"https://rebahinxxi3.mom/genre/series-indonesia/page/{p}/" if p > 1 else "https://rebahinxxi3.mom/genre/series-indonesia/")

    print(f"📡 Mengambil data film & series Indonesia dari {len(urls)} halaman rebahinxxi3.mom...")
    t0 = time.time()
    
    # 5 workers to stay below rate limit
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(fetch_page_with_retry, urls))

    all_scraped = []
    for res in results:
        all_scraped.extend(res)

    # Deduplicate by ID
    unique_map = {}
    for item in all_scraped:
        unique_map[item['id']] = item

    rebahin_movies = list(unique_map.values())
    rebahin_movies.sort(key=lambda x: (x['release_date'], x['id']), reverse=True)
    print(f"✅ Selesai mengambil {len(rebahin_movies)} judul film & serial Indonesia dalam {time.time()-t0:.2f}s!")
    return rebahin_movies

def update_catalog_with_rebahin():
    rebahin_movies = scrape_all_rebahin_indonesia()
    if not rebahin_movies:
        print("❌ Tidak ada data dari rebahin.")
        return

    # Load existing catalog
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
    else:
        catalog = []

    print(f"📦 Total katalog saat ini sebelum merge: {len(catalog)} judul.")

    # Remove any old rebahin items to avoid stale data
    existing_non_rebahin = [m for m in catalog if m.get('source') != 'rebahin' and not str(m.get('id', '')).startswith('90')]
    
    # Merge: Put recent 2026/2025/2024 Indonesian movies at the very top
    # Followed by existing catalog, followed by older Indonesian movies
    recent_rebahin = [m for m in rebahin_movies if m.get('release_date', '') in ['2026', '2025', '2024']]
    older_rebahin = [m for m in rebahin_movies if m.get('release_date', '') not in ['2026', '2025', '2024']]

    merged_catalog = recent_rebahin + existing_non_rebahin + older_rebahin

    with open(CATALOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(merged_catalog, f, ensure_ascii=False, separators=(',', ':'))

    print(f"🎉 Sukses! Katalog baru berisi {len(merged_catalog)} judul ({len(rebahin_movies)} film & serial Indonesia dari rebahinxxi3.mom).")

if __name__ == '__main__':
    update_catalog_with_rebahin()
