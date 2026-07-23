#!/usr/bin/env python3
"""
gabutin aja - Massive 14,000+ Movies & Series Catalog Generator
Scrapes TMDB API (IDLIX source) 2020-2026 for ALL movies, TV series, anime, K-drama, & Indonesian cinema
Generates a clean, ultra-optimized catalog.json with 14,000+ unique titles.
"""
import json
import urllib.request
import urllib.error
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = "15d2ea6d0dc1d476efbca3eba2b9bbfb"
BASE_URL = "https://api.themoviedb.org/3"
catalog = {}

def api_fetch(path, params=""):
    url = f"{BASE_URL}{path}?api_key={API_KEY}&language=id-ID&{params}"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(1.5)
                continue
            return None
        except Exception:
            time.sleep(0.3)
            continue
    return None

def add_to_catalog(item, mtype="movie"):
    if not item or 'id' not in item:
        return False
    mid = item['id']
    if mid in catalog:
        return False

    is_movie = mtype == "movie"
    title = item.get('title') or item.get('name') or item.get('original_title') or item.get('original_name')
    if not title:
        return False

    poster = item.get('poster_path')
    if not poster:
        return False  # skip entries without posters

    backdrop = item.get('backdrop_path')
    release = item.get('release_date') if is_movie else item.get('first_air_date')
    rel_year = (release or "2024")[:4]

    catalog[mid] = {
        "id": mid,
        "title": title,
        "type": "movie" if is_movie else "series",
        "release_date": rel_year,
        "vote_average": round(item.get('vote_average', 8.0), 1),
        "overview": (item.get('overview') or "Sinopsis belum tersedia.")[:150],
        "poster_path": f"https://image.tmdb.org/t/p/w500{poster}",
        "backdrop_path": f"https://image.tmdb.org/t/p/original{backdrop}" if backdrop else f"https://image.tmdb.org/t/p/w500{poster}",
        "genre_ids": item.get('genre_ids', [])
    }
    return True

def fetch_discover(mtype, year, page, extra=""):
    path = "/discover/movie" if mtype == "movie" else "/discover/tv"
    date_param = f"primary_release_year={year}" if mtype == "movie" else f"first_air_date_year={year}"
    data = api_fetch(path, f"{date_param}&page={page}&sort_by=popularity.desc&vote_count.gte=3&{extra}")
    if not data or 'results' not in data:
        return 0
    cnt = 0
    for item in data['results']:
        if add_to_catalog(item, mtype):
            cnt += 1
    return cnt

def main():
    years = [2026, 2025, 2024, 2023, 2022, 2021, 2020]
    print("=" * 60)
    print("🎬 GABUTIN AJA - MASSIVE 14,000+ CATALOG GENERATOR")
    print("=" * 60)
    sys.stdout.flush()

    # Build tasks
    tasks = []
    for y in years:
        for p in range(1, 26):  # 25 pages movies per year = 3500+
            tasks.append(("movie", y, p, ""))
        for p in range(1, 20):  # 19 pages TV per year = 2600+
            tasks.append(("tv", y, p, ""))

    # Additional genres & languages (Anime, K-Drama, Indo, Bollywood, etc.)
    for y in years:
        for p in range(1, 12):
            tasks.append(("movie", y, p, "with_genres=16")) # Anime movies
            tasks.append(("tv", y, p, "with_genres=16")) # Anime series
            tasks.append(("movie", y, p, "with_original_language=id")) # Indo movies
            tasks.append(("tv", y, p, "with_original_language=id")) # Indo series
            tasks.append(("tv", y, p, "with_original_language=ko")) # K-Drama
            tasks.append(("movie", y, p, "with_original_language=hi")) # Bollywood
            tasks.append(("movie", y, p, "with_original_language=ja")) # Japanese

    total = len(tasks)
    done = 0

    print(f"🚀 Launching {total} parallel requests...")
    sys.stdout.flush()

    with ThreadPoolExecutor(max_workers=5) as ex:
        futures = {ex.submit(fetch_discover, *t): t for t in tasks}
        for f in as_completed(futures):
            done += 1
            if done % 50 == 0 or done == total:
                print(f"   📥 Progress: {done}/{total} requests... ({len(catalog)} unique titles)")
                sys.stdout.flush()

    full_list = list(catalog.values())

    print("\n" + "=" * 60)
    print(f"🎉 SELESAI! TOTAL {len(full_list)} JUDUL UNIK")
    print("=" * 60)
    sys.stdout.flush()

    with open('/home/junancok/Downloads/movie-stream-app/catalog.json', 'w', encoding='utf-8') as f:
        json.dump(full_list, f, ensure_ascii=False, separators=(',', ':'))

    print(f"✅ Saved to catalog.json ({len(full_list)} items)")

if __name__ == '__main__':
    main()
