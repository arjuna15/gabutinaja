#!/usr/bin/env python3
"""
gabutin aja - Exhaustive 14,500+ Movies & Series Catalog Generator
Scrapes TMDB API 2020-2026 up to 35 pages per year to achieve 14,000+ unique titles.
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
        return False

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
    data = api_fetch(path, f"{date_param}&page={page}&sort_by=popularity.desc&vote_count.gte=2&{extra}")
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
    print("🎬 GABUTIN AJA - EXHAUSTIVE 14,500+ CATALOG SCRAPER")
    print("=" * 60)
    sys.stdout.flush()

    tasks = []
    # 35 pages per year for movies (4,900+ items)
    for y in years:
        for p in range(1, 36):
            tasks.append(("movie", y, p, ""))
    # 28 pages per year for series (3,900+ items)
    for y in years:
        for p in range(1, 29):
            tasks.append(("tv", y, p, ""))

    # Extra Genres & Languages (Anime, K-Drama, Indo, Bollywood, Japanese, Asian)
    for y in years:
        for p in range(1, 15):
            tasks.append(("movie", y, p, "with_genres=16"))
            tasks.append(("tv", y, p, "with_genres=16"))
            tasks.append(("movie", y, p, "with_original_language=id"))
            tasks.append(("tv", y, p, "with_original_language=id"))
            tasks.append(("tv", y, p, "with_original_language=ko"))
            tasks.append(("movie", y, p, "with_original_language=hi"))
            tasks.append(("movie", y, p, "with_original_language=ja"))
            tasks.append(("tv", y, p, "with_original_language=ja"))

    total = len(tasks)
    done = 0

    print(f"🚀 Launching {total} requests for 14,500+ target...")
    sys.stdout.flush()

    with ThreadPoolExecutor(max_workers=6) as ex:
        futures = {ex.submit(fetch_discover, *t): t for t in tasks}
        for f in as_completed(futures):
            done += 1
            if done % 60 == 0 or done == total:
                print(f"   📥 Progress: {done}/{total} requests... ({len(catalog)} unique titles)")
                sys.stdout.flush()

    full_list = list(catalog.values())

    print("\n" + "=" * 60)
    print(f"🎉 SCRAPING SELESAI! TOTAL {len(full_list)} JUDUL UNIK")
    print("=" * 60)
    sys.stdout.flush()

    with open('/home/junancok/Downloads/movie-stream-app/catalog.json', 'w', encoding='utf-8') as f:
        json.dump(full_list, f, ensure_ascii=False, separators=(',', ':'))

    print(f"✅ catalog.json updated! ({len(full_list)} items)")

if __name__ == '__main__':
    main()
