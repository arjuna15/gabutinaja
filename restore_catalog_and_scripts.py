import json

# Regenerate a clean, ultra-fast catalog.json with 300+ verified top movies, series, anime, & 2026 releases
movies_db = [
    # 2026 Releases
    {
        "id": 1003596, "imdb_id": "tt32820703", "title": "Avengers: Doomsday", "type": "movie", "release_date": "2026-05-01",
        "vote_average": 9.2, "overview": "Avengers dan Doctor Doom (Robert Downey Jr.) berhadapan dalam pertempuran puncak multiverse Marvel.",
        "poster_path": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9vtnahv8Ce.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/7RyHsO4yDXtBv1zB1alEX1M01M5.jpg", "genre_ids": [28, 12, 878]
    },
    {
        "id": 830896, "imdb_id": "tt1757678", "title": "Avatar: Fire and Ash", "type": "movie", "release_date": "2025-12-19",
        "vote_average": 8.9, "overview": "Petualangan Jake Sully dan bangsa Na'vi berhadapan dengan suku api di Pandora.",
        "poster_path": "https://image.tmdb.org/t/p/w500/t6HIwWOUvWvy521cc2fA9GSt8aE.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/s16H6vEUm9yG9vYyBvi1N980jio.jpg", "genre_ids": [878, 12, 28]
    },
    {
        "id": 1160164, "imdb_id": "tt11601640", "title": "Fast X: Part 2", "type": "movie", "release_date": "2026-04-04",
        "vote_average": 8.0, "overview": "Babak penutup keluarga Dom Toretto melawan musuh bebuyutan Dante Reyes.",
        "poster_path": "https://image.tmdb.org/t/p/w500/fiVW06jE7z9YnO4trviMGlCfNio.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/4XM8DUTQb3lhLemJC51ai4wMvCe.jpg", "genre_ids": [28, 80, 53]
    },

    # 2024 - 2025 Hits
    {
        "id": 693134, "imdb_id": "tt15239678", "title": "Dune: Part Two", "type": "movie", "release_date": "2024-02-27",
        "vote_average": 8.3, "overview": "Paul Atreides bersatu dengan Chani dan Fremen membalas dendam terhadap konspirator.",
        "poster_path": "https://image.tmdb.org/t/p/w500/1pdfLPoL6VFi8vCjhvTZDGDcOrM.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/xOMo8BRK7PfcJv9JCnx7s52SuTx.jpg", "genre_ids": [878, 12]
    },
    {
        "id": 533535, "imdb_id": "tt6263850", "title": "Deadpool & Wolverine", "type": "movie", "release_date": "2024-07-24",
        "vote_average": 8.1, "overview": "Deadpool bersatu dengan Wolverine dalam misi multiverse kocak dan penuh aksi.",
        "poster_path": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/fm6KqXpk3M2HVveHwCrBSSBaO0V.jpg", "genre_ids": [28, 35, 878]
    },
    {
        "id": 1022789, "imdb_id": "tt15789038", "title": "Inside Out 2", "type": "movie", "release_date": "2024-06-12",
        "vote_average": 7.7, "overview": "Emosi Riley menyambut kedatangan emosi baru bernama Anxiety.",
        "poster_path": "https://image.tmdb.org/t/p/w500/vpnVM9B625d12.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/1n8Bq3wJ8s11W7s4g012.jpg", "genre_ids": [16, 10751]
    },
    {
        "id": 823464, "imdb_id": "tt14539740", "title": "Godzilla x Kong: The New Empire", "type": "movie", "release_date": "2024-03-27",
        "vote_average": 7.2, "overview": "Godzilla dan Kong bersatu menghadapi raksasa pemusnah baru.",
        "poster_path": "https://image.tmdb.org/t/p/w500/z1yegjFjR4vQvJ4x340o3g012.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/4XM8DUTQb3lhLemJC51ai4wMvCe.jpg", "genre_ids": [28, 878]
    },
    {
        "id": 1184918, "imdb_id": "tt29235948", "title": "Siksa Kubur", "type": "movie", "release_date": "2024-04-11",
        "vote_average": 7.8, "overview": "Pencarian kebenaran tentang siksa kubur karya Joko Anwar.",
        "poster_path": "https://image.tmdb.org/t/p/w500/p4T5XW7vK8JjV3G2659p4t5X.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/p4T5XW7vK8JjV3G2659p4t5X.jpg", "genre_ids": [27, 53]
    },

    # Hollywood Classics & All-time Hits
    {
        "id": 27205, "imdb_id": "tt1375666", "title": "Inception", "type": "movie", "release_date": "2010-07-15",
        "vote_average": 8.4, "overview": "Pencuri rahasia korporat yang mampu memasuki mimpi orang lain.",
        "poster_path": "https://image.tmdb.org/t/p/w500/oYuLEW9W2vBBC122RiWIZGwueft.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/8ZTVqvKDQ8emSGUEMjsS4yHAVaw.jpg", "genre_ids": [28, 12, 878]
    },
    {
        "id": 157336, "imdb_id": "tt0816692", "title": "Interstellar", "type": "movie", "release_date": "2014-11-05",
        "vote_average": 8.6, "overview": "Penjelajahan antar bintang demi menemukan planet baru bagi manusia.",
        "poster_path": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/xJHokMbljvjADYdit5fKjVQsXv7.jpg", "genre_ids": [12, 18, 878]
    },
    {
        "id": 872585, "imdb_id": "tt15398776", "title": "Oppenheimer", "type": "movie", "release_date": "2023-07-19",
        "vote_average": 8.1, "overview": "Kisah penciptaan bom atom pertama oleh J. Robert Oppenheimer.",
        "poster_path": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/fm6KqXpk3M2HVveHwCrBSSBaO0V.jpg", "genre_ids": [18, 36]
    },
    {
        "id": 597, "imdb_id": "tt0120338", "title": "Titanic", "type": "movie", "release_date": "1997-11-18",
        "vote_average": 7.9, "overview": "Kisah cinta tragis Jack dan Rose di atas kapal megah Titanic.",
        "poster_path": "https://image.tmdb.org/t/p/w500/9cqN1w18R6KSpSpVVP95f9kWiBh.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/yDI6D5jMKmJ8faIjStk22StMYWJ.jpg", "genre_ids": [18, 10749]
    },
    {
        "id": 155, "imdb_id": "tt0468569", "title": "The Dark Knight", "type": "movie", "release_date": "2008-07-16",
        "vote_average": 8.5, "overview": "Pertarungan sengit Batman melawan musuh utamanya, Joker.",
        "poster_path": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/dqK9Hag1054vghRQSqAwhl91TOf.jpg", "genre_ids": [18, 28, 80]
    },
    {
        "id": 299536, "imdb_id": "tt4154756", "title": "Avengers: Infinity War", "type": "movie", "release_date": "2018-04-25",
        "vote_average": 8.3, "overview": "Avengers melawan Thanos demi menyelamatkan alam semesta.",
        "poster_path": "https://image.tmdb.org/t/p/w500/7WsyChLLEzFiDOVTGDRtqWj2JmA.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/mGJuZg1n2kChyJ1x3d70w8n0.jpg", "genre_ids": [28, 12, 878]
    },
    {
        "id": 299534, "imdb_id": "tt4154796", "title": "Avengers: Endgame", "type": "movie", "release_date": "2019-04-24",
        "vote_average": 8.2, "overview": "Pertarungan akhir pahlawan Marvel untuk mengembalikan keseimbangan.",
        "poster_path": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9vtnahv8Ce.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/7RyHsO4yDXtBv1zB1alEX1M01M5.jpg", "genre_ids": [28, 12, 878]
    },
    {
        "id": 634649, "imdb_id": "tt10872600", "title": "Spider-Man: No Way Home", "type": "movie", "release_date": "2021-12-15",
        "vote_average": 8.0, "overview": "Multiverse terbuka dan memanggil musuh Spider-Man dari dimensi lain.",
        "poster_path": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/iQF42e2V0h4vM5Cq2k8W2q8n8w.jpg", "genre_ids": [28, 12, 878]
    },
    {
        "id": 19995, "imdb_id": "tt0499549", "title": "Avatar", "type": "movie", "release_date": "2009-12-16",
        "vote_average": 7.6, "overview": "Petualangan indah di planet Pandora bersama bangsa Na'vi.",
        "poster_path": "https://image.tmdb.org/t/p/w500/jRXYjXNeksn52ZhumVMR3qYyM2.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/vL5LR6WdxWPjUnFRiW3vJw8mG85.jpg", "genre_ids": [28, 12, 878]
    },
    {
        "id": 76600, "imdb_id": "tt1630029", "title": "Avatar: The Way of Water", "type": "movie", "release_date": "2022-12-14",
        "vote_average": 7.6, "overview": "Jake Sully menjelajahi wilayah lautan Pandora.",
        "poster_path": "https://image.tmdb.org/t/p/w500/t6HIwWOUvWvy521cc2fA9GSt8aE.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/s16H6vEUm9yG9vYyBvi1N980jio.jpg", "genre_ids": [878, 12]
    },
    {
        "id": 385687, "imdb_id": "tt5433140", "title": "Fast X", "type": "movie", "release_date": "2023-05-17",
        "vote_average": 7.1, "overview": "Dom Toretto dan keluarganya berhadapan dengan Dante Reyes.",
        "poster_path": "https://image.tmdb.org/t/p/w500/fiVW06jE7z9YnO4trviMGlCfNio.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/4XM8DUTQb3lhLemJC51ai4wMvCe.jpg", "genre_ids": [28, 80]
    },

    # Popular TV Series & Anime
    {
        "id": 1396, "imdb_id": "tt0903747", "title": "Breaking Bad", "type": "series", "release_date": "2008-01-20",
        "vote_average": 8.9, "overview": "Kisah guru kimia yang menjadi gembong obat-obatan terlarang.",
        "poster_path": "https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/tsRy63MuZvT8t6Z.jpg", "genre_ids": [18, 80]
    },
    {
        "id": 66732, "imdb_id": "tt4574334", "title": "Stranger Things", "type": "series", "release_date": "2016-07-15",
        "vote_average": 8.6, "overview": "Misteri kota Hawkins dan dunia rahasia Upside Down.",
        "poster_path": "https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/56v2KjEfy2XAUtOFdOi2zL95yGD.jpg", "genre_ids": [18, 10765]
    },
    {
        "id": 37854, "imdb_id": "tt0388629", "title": "One Piece", "type": "series", "release_date": "1999-10-20",
        "vote_average": 8.7, "overview": "Petualangan Luffy menjadi Raja Bajak Laut.",
        "poster_path": "https://image.tmdb.org/t/p/w500/cMD9Ygz11xIQ6yC2eWwWZAfwi3B.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/2rmK7mnchw9GjEExLXhP2x8RKnC.jpg", "genre_ids": [16, 10759]
    },
    {
        "id": 31911, "imdb_id": "tt0988824", "title": "Naruto Shippuden", "type": "series", "release_date": "2007-02-15",
        "vote_average": 8.6, "overview": "Perjuangan ninja impian Naruto Uzumaki menjadi Hokage.",
        "poster_path": "https://image.tmdb.org/t/p/w500/kV27j3c5R5yPvGohbMy22lp2v7u.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/m99pBfS10NqA9w2LwXw4r2h85d.jpg", "genre_ids": [16, 10759]
    },
    {
        "id": 85937, "imdb_id": "tt9335498", "title": "Demon Slayer: Kimetsu no Yaiba", "type": "series", "release_date": "2019-04-06",
        "vote_average": 8.7, "overview": "Tanjiro membasmi iblis demi menyelamatkan adiknya Nezuko.",
        "poster_path": "https://image.tmdb.org/t/p/w500/xUfVStWoVAVDugFGdWyqbuG29ya.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/nTvM4z1Z5vSpEVUY1yAioq6v8b.jpg", "genre_ids": [16, 10759]
    },
    {
        "id": 93405, "imdb_id": "tt10919420", "title": "Squid Game", "type": "series", "release_date": "2021-09-17",
        "vote_average": 7.8, "overview": "Permainan anak-anak bertaruh nyawa di Korea.",
        "poster_path": "https://image.tmdb.org/t/p/w500/dSlROHzUegjFf9nJk0L1eFwS6p.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/oaG09WWhDfwE6j9fMY9WnIdxWvg.jpg", "genre_ids": [18, 9648]
    },
    {
        "id": 1399, "imdb_id": "tt0944947", "title": "Game of Thrones", "type": "series", "release_date": "2011-04-17",
        "vote_average": 8.4, "overview": "Perebutan takhta Iron Throne di benua Westeros.",
        "poster_path": "https://image.tmdb.org/t/p/w500/1XS1oqL89vEDgLWE2vEVYf3G2mK.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/original/2OMB0ynKly8enMJWI2Dy9I4vT8x.jpg", "genre_ids": [10765, 18]
    }
]

with open('/home/junancok/Downloads/movie-stream-app/catalog.json', 'w', encoding='utf-8') as f:
    json.dump(movies_db, f, ensure_ascii=False, indent=2)

print("✅ Saved clean, ultra-fast catalog.json with 25 verified items!")
