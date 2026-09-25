#!/usr/bin/env python3
"""
gabutin aja - Auto Catalog Updater Script
Fetches latest 2026 movie/series releases & trending content from TMDB
and automatically appends new titles to catalog.json.
"""
import json
import urllib.request
import urllib.error
import os

API_KEY = "15d2ea6d0dc1d476efbca3eba2b9bbfb"
BASE_URL = "https://api.themoviedb.org/3"
CATALOG_PATH = "/home/junancok/Downloads/movie-stream-app/catalog.json"

ENDPOINTS = [
    "/trending/all/day",
    "/movie/now_playing",
    "/movie/popular",
    "/tv/on_the_air",
    "/tv/popular",
    "/discover/movie?primary_release_year=2026&sort_by=popularity.desc",
    "/discover/tv?first_air_date_year=2026&sort_by=popularity.desc"
]

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def update_catalog():
    print("🔄 Memulai sinkronisasi otomatis film & series terbaru...")
    
    # Load existing catalog
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
    else:
        catalog = []

    existing_ids = {item['id'] for item in catalog}
    new_added = 0

    for ep in ENDPOINTS:
        url = f"{BASE_URL}{ep}{'&' if '?' in ep else '?'}api_key={API_KEY}&language=id-ID"
        data = fetch_json(url)
        if not data or 'results' not in data:
            continue

        for item in data['results']:
            mid = item.get('id')
            if not mid or mid in existing_ids:
                continue

            poster = item.get('poster_path')
            if not poster:
                continue

            is_movie = 'title' in item or 'release_date' in item
            title = item.get('title') or item.get('name') or 'Untitled'
            rel_date = (item.get('release_date') or item.get('first_air_date') or '2026')[:4]
            backdrop = item.get('backdrop_path')

            entry = {
                "id": mid,
                "title": title,
                "type": "movie" if is_movie else "series",
                "release_date": rel_date,
                "vote_average": round(item.get('vote_average', 8.0), 1),
                "overview": (item.get('overview') or "Sinopsis belum tersedia.")[:150],
                "poster_path": f"https://image.tmdb.org/t/p/w500{poster}",
                "backdrop_path": f"https://image.tmdb.org/t/p/original{backdrop}" if backdrop else f"https://image.tmdb.org/t/p/w500{poster}",
                "genre_ids": item.get('genre_ids', [])
            }

            catalog.insert(0, entry) # Prepend new items to top
            existing_ids.add(mid)
            new_added += 1

    # Also sync latest Indonesian releases from rebahinxxi3.mom
    try:
        from scrape_rebahin import fetch_page_with_retry
        print("🇮🇩 Menyinkronkan rilisan film & serial Indonesia terbaru dari rebahinxxi3.mom...")
        indo_urls = [
            "https://rebahinxxi3.mom/country/indonesia/",
            "https://rebahinxxi3.mom/country/indonesia/page/2/",
            "https://rebahinxxi3.mom/country/indonesia/page/3/",
            "https://rebahinxxi3.mom/genre/series-indonesia/"
        ]
        indo_added = 0
        for i_url in indo_urls:
            items = fetch_page_with_retry(i_url)
            for it in items:
                if it['id'] not in existing_ids:
                    catalog.insert(0, it)
                    existing_ids.add(it['id'])
                    new_added += 1
                    indo_added += 1
        if indo_added > 0:
            print(f"🇮🇩 Berhasil menambah {indo_added} judul film/series Indonesia terbaru dari Rebahin XXI!")
    except Exception as ie:
        print(f"Rebahin sync note: {ie}")

    if new_added > 0:
        with open(CATALOG_PATH, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, ensure_ascii=False, separators=(',', ':'))
        print(f"✅ Berhasil menambah {new_added} film/series baru ke catalog.json! Total: {len(catalog)} judul.")
        
        # Auto-commit locally
        try:
            os.system(f"cd /home/junancok/Downloads/movie-stream-app && git add catalog.json && git commit -m 'cron: auto-update catalog with {new_added} new releases (incl. Rebahin XXI Indo)'")
            # Attempt push only if non-interactive credentials exist
            os.system("GIT_TERMINAL_PROMPT=0 git push origin main 2>/dev/null || true")
            print("🚀 Catalog updated and committed locally!")
        except Exception as ge:
            print(f"Git note: {ge}")
    else:
        print("✨ Database sudah up-to-date! Tidak ada judul baru.")

if __name__ == '__main__':
    update_catalog()
