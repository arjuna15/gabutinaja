#!/usr/bin/env python3
"""
Extract direct video player stream URLs (iembed with clean player) for Indonesian movies in catalog.json.
This ensures the player opens ONLY the film video, NOT the Rebahin website.
"""
import urllib.request
import re
import json
import time
from concurrent.futures import ThreadPoolExecutor

CATALOG_PATH = "/home/junancok/Downloads/movie-stream-app/catalog.json"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer': 'https://rebahinxxi3.mom/'
}

PATTERN = re.compile(r'data-iframe=[\'\"]([A-Za-z0-9+/=]+)[\'\"]')

def fetch_streams_for_movie(movie, retries=2):
    raw_url = movie.get('rebahin_url') or ''
    if not raw_url:
        return movie['id'], None, []

    is_series = movie.get('type') == 'series'
    play_url = raw_url.rstrip('/') + ('/watch/' if is_series else '/play/')

    for attempt in range(retries):
        try:
            req = urllib.request.Request(play_url, headers=HEADERS)
            html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
            matches = PATTERN.findall(html)
            if matches:
                import base64
                unique_b64 = list(dict.fromkeys(matches))
                clean_streams = []
                for b in unique_b64:
                    try:
                        dec = base64.b64decode(b).decode('utf-8', errors='ignore')
                        if dec.startswith('http'):
                            clean_streams.append(dec)
                        else:
                            clean_streams.append(f"https://rebahinxxi3.mom/iembed/?source={b}")
                    except Exception:
                        clean_streams.append(f"https://rebahinxxi3.mom/iembed/?source={b}")
                return movie['id'], clean_streams[0], clean_streams
            return movie['id'], None, []
        except Exception:
            if attempt < retries - 1:
                time.sleep(1)
            else:
                return movie['id'], None, []

def populate_streams(target_count=600):
    print("🎬 Memulai ekstraksi link pemutar video langsung (clean video stream) dari rebahin...")
    with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    # Find Rebahin Indonesian movies without stream_url
    indo_movies = [m for m in catalog if (m.get('source') == 'rebahin' or m.get('is_indonesian')) and not m.get('stream_url')]
    print(f"Total film Indonesia yang belum memiliki stream_url: {len(indo_movies)}")

    to_process = indo_movies[:target_count]
    print(f"Memproses {len(to_process)} judul film & serial Indonesia...")

    t0 = time.time()
    results = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        for mid, primary_stream, all_sources in executor.map(fetch_streams_for_movie, to_process):
            if primary_stream:
                results[mid] = (primary_stream, all_sources)

    print(f"Berhasil mengekstrak {len(results)}/{len(to_process)} direct stream URLs dalam {time.time()-t0:.2f}s!")

    # Update catalog
    updated = 0
    for movie in catalog:
        mid = movie.get('id')
        if mid in results:
            primary, all_s = results[mid]
            movie['stream_url'] = primary
            if movie.get('type') == 'series':
                movie['episodes_sources'] = all_s
            else:
                movie['stream_sources'] = all_s
            if 'rebahin_play_url' in movie:
                del movie['rebahin_play_url']
            updated += 1

    with open(CATALOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, separators=(',', ':'))

    print(f"🎉 Sukses! {updated} film Indonesia di catalog.json kini memutar LANGSUNG videonya (clean video player).")

if __name__ == '__main__':
    populate_streams(target_count=600)
