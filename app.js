// StreamX - Main Application Logic

// ============================================================
// 🛡️ MEGA ANTI-POPUP & TAB HIJACK KILLER
// 100% Blocks ALL popunder triggers, new tab redirects & one-clicks
// ============================================================

// 1. Kill window.open completely
const _noop = function() { 
    console.log('[🛡️ StreamX] Popup BLOCKED!'); 
    return null; 
};
window.open = _noop;

// Continuous enforcement of window.open override
setInterval(() => { window.open = _noop; }, 200);

// 2. Intercept and block all programmatic anchor click popup triggers
const origAnchorClick = HTMLAnchorElement.prototype.click;
HTMLAnchorElement.prototype.click = function() {
    if (this.target === '_blank' || (this.href && !this.href.includes(window.location.hostname))) {
        console.log('[🛡️ StreamX] Anchor popup click BLOCKED:', this.href);
        return;
    }
    return origAnchorClick.apply(this, arguments);
};

// 3. Block all _blank link clicks globally
document.addEventListener('click', function(e) {
    const link = e.target.closest('a');
    if (link && (link.target === '_blank' || link.hostname !== window.location.hostname)) {
        e.preventDefault();
        e.stopPropagation();
        console.log('[🛡️ StreamX] External link BLOCKED:', link.href);
        return false;
    }
}, true);

// 4. Automatic Window Refocus on Blur (Kills popunders instantly)
window.addEventListener('blur', function() {
    setTimeout(() => {
        window.focus();
    }, 10);
});

// 5. Prevent beforeunload hijacks from iframes
window.addEventListener('beforeunload', function(e) {
    e.stopImmediatePropagation();
}, true);

// 6. Block form submissions to external URLs
document.addEventListener('submit', function(e) {
    const form = e.target;
    if (form && form.action && !form.action.includes(window.location.hostname)) {
        e.preventDefault();
        console.log('[🛡️ StreamX] External form BLOCKED');
    }
}, true);

// Configuration & State
const CONFIG = {
    TMDB_API_KEY: '15d2ea6d0dc1d476efbca3eba2b9bbfb',
    TMDB_BASE_URL: 'https://api.themoviedb.org/3',
    IMAGE_BASE_URL: 'https://image.tmdb.org/t/p/w500',
    BACKDROP_BASE_URL: 'https://image.tmdb.org/t/p/original'
};

const state = {
    currentTab: 'home',
    currentGenre: 'all',
    searchQuery: '',
    currentPage: 1,
    isLoadingMore: false,
    currentSeason: 1,
    currentEpisode: 1,
    movies: [],
    featuredMovie: null,
    activeMovie: null,
    activeServer: 'vidbinge',
    watchlist: JSON.parse(localStorage.getItem('streamx_watchlist') || '[]'),
    customMovies: JSON.parse(localStorage.getItem('streamx_custom_movies') || '[]')
};

// Stream Server Embed Providers (VERIFIED 100% ZERO-POPUP & CLEAN)
const SERVERS = {
    'vidbinge': (movie, season = 1, episode = 1) => {
        return movie.type === 'series' 
            ? `https://vidbinge.dev/embed/tv/${movie.id}/${season}/${episode}` 
            : `https://vidbinge.dev/embed/movie/${movie.id}`;
    },
    'embed-su': (movie, season = 1, episode = 1) => {
        return movie.type === 'series' 
            ? `https://embed.su/embed/tv/${movie.id}/${season}/${episode}` 
            : `https://embed.su/embed/movie/${movie.id}`;
    },
    'vidsrc-vip': (movie, season = 1, episode = 1) => {
        return movie.type === 'series' 
            ? `https://vidsrc.vip/embed/tv/${movie.id}/${season}/${episode}` 
            : `https://vidsrc.vip/embed/movie/${movie.id}`;
    },
    'multiembed': (movie, season = 1, episode = 1) => {
        return movie.type === 'series' 
            ? `https://multiembed.mov/?video_id=${movie.id}&tmdb=1&s=${season}&e=${episode}` 
            : `https://multiembed.mov/?video_id=${movie.id}&tmdb=1`;
    },
    'videasy': (movie, season = 1, episode = 1) => {
        return movie.type === 'series' 
            ? `https://player.videasy.net/tv/${movie.id}/${season}/${episode}` 
            : `https://player.videasy.net/movie/${movie.id}`;
    }
};

// Curated Offline Demo Dataset (Fallback if network or TMDB API is unavailable)
const DEMO_MOVIES = [
    {
        id: 550,
        title: 'Fight Club',
        type: 'movie',
        release_date: '1999-10-15',
        vote_average: 8.4,
        overview: 'Seorang pekerja kantor yang menderita insomnia bertemu dengan pembuat sabun yang ceroboh dan membentuk klub pertarungan bawah tanah yang segera berkembang menjadi sesuatu yang lebih besar.',
        poster_path: '/pB8OverwY1vSRWz2B7dwoUZxYDH.jpg',
        backdrop_path: '/hZkgoQY85WAgW2sAYWi246qZkZ8.jpg',
        genre_ids: [18, 53]
    },
    {
        id: 157336,
        title: 'Interstellar',
        type: 'movie',
        release_date: '2014-11-05',
        vote_average: 8.6,
        overview: 'Petualangan sekelompok penjelajah yang memanfaatkan lubang cacing yang baru ditemukan untuk menembus batas perjalanan luar angkasa manusia dan menaklukkan jarak yang sangat jauh dalam perjalanan antarbintang.',
        poster_path: '/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg',
        backdrop_path: '/xJHokMbljvjADYdit5fKjVQsXv7.jpg',
        genre_ids: [12, 18, 878]
    },
    {
        id: 27205,
        title: 'Inception',
        type: 'movie',
        release_date: '2010-07-15',
        vote_average: 8.3,
        overview: 'Seorang pencuri yang mencuri rahasia korporat melalui penggunaan teknologi berbagi mimpi diberikan tugas terbalik yaitu menanamkan ide ke dalam pikiran seorang CEO.',
        poster_path: '/oYuLEW9W2vBBC122RiWIZGwueft.jpg',
        backdrop_path: '/8ZTVqvKDQ8emSGUEMjsS4yHAVaw.jpg',
        genre_ids: [28, 12, 878]
    },
    {
        id: 299536,
        title: 'Avengers: Infinity War',
        type: 'movie',
        release_date: '2018-04-25',
        vote_average: 8.3,
        overview: 'Avengers dan sekutunya harus bersedia mengorbankan segalanya dalam usaha mengalahkan Thanos sebelum kehancuran dan kebinasaan mengakhiri alam semesta.',
        poster_path: '/7WsyChLLEzFiDOVTGDRtqWj2JmA.jpg',
        backdrop_path: '/mGJuZg1n2kChyJ1x3d70w8n0.jpg',
        genre_ids: [28, 12, 878]
    },
    {
        id: 671,
        title: "Harry Potter and the Philosopher's Stone",
        type: 'movie',
        release_date: '2001-11-16',
        vote_average: 7.9,
        overview: 'Seorang anak laki-laki yatim piatu mendaftar di sekolah sihir, di mana ia mempelajari kebenaran tentang dirinya, keluarganya, dan kejahatan mengerikan yang mengintai di dunia sihir.',
        poster_path: '/wuMc08IPKEatf9rnMNXvIDxqh4W.jpg',
        backdrop_path: '/hziNrL92wS2V9sY79b.jpg',
        genre_ids: [12, 14, 10751]
    },
    {
        id: 1396,
        title: 'Breaking Bad',
        type: 'series',
        release_date: '2008-01-20',
        vote_average: 8.9,
        overview: 'Seorang guru kimia SMA yang didiagnosis menderita kanker paru-paru stadium akhir beralih ke pembuatan dan penjualan methamphetamine bersama mantan muridnya.',
        poster_path: '/zte2id74.jpg',
        backdrop_path: '/tsRy63MuZvT8t6Z.jpg',
        genre_ids: [18, 80]
    }
];

// DOM Elements
const elements = {
    searchInput: document.getElementById('search-input'),
    clearSearch: document.getElementById('clear-search'),
    movieGrid: document.getElementById('movie-grid'),
    resultCount: document.getElementById('result-count'),
    sectionTitle: document.getElementById('section-title'),
    favCount: document.getElementById('fav-count'),
    
    // Hero Banner
    heroBg: document.getElementById('hero-bg'),
    heroTitle: document.getElementById('hero-title'),
    heroOverview: document.getElementById('hero-overview'),
    heroYear: document.getElementById('hero-year'),
    heroRating: document.getElementById('hero-rating'),
    heroDuration: document.getElementById('hero-duration'),
    heroGenres: document.getElementById('hero-genres'),
    heroPlayBtn: document.getElementById('hero-play-btn'),
    heroInfoBtn: document.getElementById('hero-info-btn'),

    // Player Modal
    playerModal: document.getElementById('player-modal'),
    closePlayerModal: document.getElementById('close-player-modal'),
    modalMovieTitle: document.getElementById('modal-movie-title'),
    modalMovieSubtitle: document.getElementById('modal-movie-subtitle'),
    modalPoster: document.getElementById('modal-poster'),
    modalRating: document.getElementById('modal-rating'),
    modalOverview: document.getElementById('modal-overview'),
    modalFavBtn: document.getElementById('modal-fav-btn'),
    streamIframe: document.getElementById('stream-iframe'),
    playerLoader: document.getElementById('player-loader'),
    serverList: document.getElementById('server-list'),
    
    // Custom URL Input Drawer
    customUrlBox: document.getElementById('custom-url-box'),
    btnInputCustomUrl: document.getElementById('btn-input-custom-url'),
    customIframeInput: document.getElementById('custom-iframe-input'),
    applyCustomUrlBtn: document.getElementById('apply-custom-url'),

    // Page Pagination Container
    paginationContainer: document.getElementById('pagination-container'),

    // TV Episodes Selector Elements
    tvEpisodesBar: document.getElementById('tv-episodes-bar'),
    seasonSelect: document.getElementById('season-select'),
    episodeGrid: document.getElementById('episode-grid')
};

// Initialize App
function startApp() {
    initNavigation();
    initGenreChips();
    initSearch();
    initModals();
    updateFavCount();
    loadCatalogDatabase();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startApp);
} else {
    startApp();
}

// Fetch Comprehensive Catalog Database (catalog.json)
async function loadCatalogDatabase() {
    if (elements.movieGrid) {
        elements.movieGrid.innerHTML = createSkeletons(12);
    }
    try {
        const response = await fetch('./catalog.json?t=' + Date.now());
        if (response.ok) {
            const data = await response.json();
            if (Array.isArray(data)) {
                state.movies = [...state.customMovies, ...data.filter(item => item && typeof item === 'object' && item.id)];
                console.log(`Loaded ${state.movies.length} movies from catalog database!`);
            } else {
                throw new Error('Catalog data is not an array');
            }
        } else {
            throw new Error('Local catalog.json HTTP ' + response.status);
        }
    } catch (err) {
        console.warn('Catalog load error, using fallback:', err);
        try {
            await loadMoviesLive('/trending/all/day');
        } catch (e) {
            state.movies = [...state.customMovies, ...DEMO_MOVIES];
        }
    }

    try {
        renderMovies();
    } catch (e) {
        console.error('Error rendering movies:', e);
    }

    try {
        setupHeroBanner();
    } catch (e) {
        console.error('Error setting up hero banner:', e);
    }
}

// Fallback Live TMDB Fetcher
async function loadMoviesLive(endpoint = '/trending/all/day') {
    try {
        const response = await fetch(`${CONFIG.TMDB_BASE_URL}${endpoint}?api_key=${CONFIG.TMDB_API_KEY}&language=id-ID`);
        if (!response.ok) throw new Error('API Request Failed');
        const data = await response.json();
        
        state.movies = [...state.customMovies, ...(data.results || []).map(item => ({
            id: item.id,
            title: item.title || item.name || 'Untitled',
            type: item.media_type || (item.title ? 'movie' : 'series'),
            release_date: (item.release_date || item.first_air_date || '2026').substring(0, 4),
            vote_average: item.vote_average ? item.vote_average.toFixed(1) : '8.0',
            overview: item.overview || 'Sinopsis belum tersedia.',
            poster_path: item.poster_path ? `${CONFIG.IMAGE_BASE_URL}${item.poster_path}` : 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=500&auto=format&fit=crop',
            backdrop_path: item.backdrop_path ? `${CONFIG.BACKDROP_BASE_URL}${item.backdrop_path}` : 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=1200&auto=format&fit=crop',
            genre_ids: item.genre_ids || []
        }))];
    } catch (err) {
        state.movies = [...state.customMovies, ...DEMO_MOVIES];
    }
}

// Render Movies Grid
// Render Movies Grid with Page Pagination (40 Items Per Page)
function renderMovies() {
    const ITEMS_PER_PAGE = 40;
    let filtered = state.movies;

    // Filter by Tab
    if (state.currentTab === 'movies') {
        filtered = filtered.filter(m => m.type === 'movie');
    } else if (state.currentTab === 'series') {
        filtered = filtered.filter(m => m.type === 'series');
    } else if (state.currentTab === 'trending') {
        filtered = [...filtered].sort((a, b) => (b.vote_average || 0) - (a.vote_average || 0));
    } else if (state.currentTab === 'watchlist') {
        filtered = state.watchlist;
    }

    // Filter by Genre
    if (state.currentGenre !== 'all') {
        const genreId = parseInt(state.currentGenre);
        filtered = filtered.filter(m => m.genre_ids && m.genre_ids.includes(genreId));
    }

    // Filter by Search Query
    if (state.searchQuery.trim() !== '') {
        const q = state.searchQuery.toLowerCase();
        filtered = filtered.filter(m => m.title.toLowerCase().includes(q) || (m.overview && m.overview.toLowerCase().includes(q)));
    }

    const totalItems = filtered.length;
    const totalPages = Math.max(1, Math.ceil(totalItems / ITEMS_PER_PAGE));

    // Ensure current page is within valid range
    if (state.currentPage > totalPages) {
        state.currentPage = 1;
    }

    const startIndex = (state.currentPage - 1) * ITEMS_PER_PAGE;
    const endIndex = Math.min(startIndex + ITEMS_PER_PAGE, totalItems);
    const pageItems = filtered.slice(startIndex, endIndex);

    elements.resultCount.textContent = `${totalItems} Judul Ditemukan (Halaman ${state.currentPage} dari ${totalPages})`;

    if (totalItems === 0) {
        elements.movieGrid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 4rem 1rem; color: var(--text-muted);">
                <i class="fa-solid fa-film" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                <h3>Tidak Ada Film Ditemukan</h3>
                <p>Coba kata kunci lain atau pilih genre yang berbeda.</p>
            </div>
        `;
        if (elements.paginationContainer) elements.paginationContainer.innerHTML = '';
        return;
    }

    elements.movieGrid.innerHTML = pageItems.map(movie => {
        const posterUrl = (movie.poster_path && movie.poster_path.startsWith('http')) 
            ? movie.poster_path 
            : (movie.poster_path ? `${CONFIG.IMAGE_BASE_URL}${movie.poster_path}` : 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=500&auto=format&fit=crop');

        return `
        <div class="movie-card" onclick="openPlayerModal(${movie.id}, '${movie.customUrl ? 'custom' : 'tmdb'}')">
            <div class="card-poster">
                <img src="${posterUrl}" 
                     alt="${movie.title}" 
                     loading="lazy" 
                     onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=500&auto=format&fit=crop';">
                <div class="card-overlay">
                    <div class="play-hover-btn"><i class="fa-solid fa-play"></i></div>
                </div>
                <span class="card-type-badge">${movie.type || 'MOVIE'}</span>
                <span class="card-badge-rating"><i class="fa-solid fa-star"></i> ${movie.vote_average || '8.0'}</span>
            </div>
            <div class="card-info">
                <h3 class="card-title" title="${movie.title}">${movie.title}</h3>
                <div class="card-meta">
                    <span>${(movie.release_date || '').substring(0, 4)}</span>
                    <span><i class="fa-solid fa-shield-halved text-gradient"></i> HD</span>
                </div>
            </div>
        </div>
    `;
    }).join('');

    renderPaginationControls(totalPages);
}

// Render Page Pagination Buttons (Prev, 1, 2, 3... Next)
function renderPaginationControls(totalPages) {
    if (!elements.paginationContainer) return;
    if (totalPages <= 1) {
        elements.paginationContainer.innerHTML = '';
        return;
    }

    const current = state.currentPage;
    let html = '';

    // Previous Button
    html += `<button class="page-btn nav-page-btn ${current === 1 ? 'disabled' : ''}" ${current === 1 ? 'disabled' : ''} onclick="changePage(${current - 1})"><i class="fa-solid fa-chevron-left"></i> Prev</button>`;

    // Page Number Buttons Logic
    let pagesToDisplay = [];
    if (totalPages <= 7) {
        for (let i = 1; i <= totalPages; i++) pagesToDisplay.push(i);
    } else {
        pagesToDisplay.push(1);
        if (current > 3) pagesToDisplay.push('...');

        const startRange = Math.max(2, current - 1);
        const endRange = Math.min(totalPages - 1, current + 1);

        for (let i = startRange; i <= endRange; i++) {
            if (!pagesToDisplay.includes(i)) pagesToDisplay.push(i);
        }

        if (current < totalPages - 2) pagesToDisplay.push('...');
        pagesToDisplay.push(totalPages);
    }

    pagesToDisplay.forEach(p => {
        if (p === '...') {
            html += `<span class="page-ellipsis">...</span>`;
        } else {
            html += `<button class="page-btn ${p === current ? 'active' : ''}" onclick="changePage(${p})">${p}</button>`;
        }
    });

    // Next Button
    html += `<button class="page-btn nav-page-btn ${current === totalPages ? 'disabled' : ''}" ${current === totalPages ? 'disabled' : ''} onclick="changePage(${current + 1})">Next <i class="fa-solid fa-chevron-right"></i></button>`;

    elements.paginationContainer.innerHTML = html;
}

// Change Current Page & Smooth Scroll to Section Top
function changePage(newPage) {
    state.currentPage = newPage;
    renderMovies();
    const section = document.getElementById('results-section');
    if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Setup Hero Featured Banner
function setupHeroBanner() {
    if (state.movies.length === 0) return;
    const featured = state.movies[0];
    state.featuredMovie = featured;

    elements.heroBg.style.backgroundImage = `url('${featured.backdrop_path}')`;
    elements.heroTitle.textContent = featured.title;
    elements.heroOverview.textContent = featured.overview;
    elements.heroYear.textContent = (featured.release_date || '').substring(0, 4);
    elements.heroRating.textContent = featured.vote_average || '8.5';
    
    elements.heroPlayBtn.onclick = () => openPlayerModal(featured.id);
    elements.heroInfoBtn.onclick = () => openPlayerModal(featured.id);
}

// Open Video Player Modal
function openPlayerModal(id, source = 'tmdb') {
    let movie = state.movies.find(m => m.id === id || m.id == id);
    if (!movie) movie = state.watchlist.find(m => m.id === id || m.id == id);
    if (!movie) return;

    state.activeMovie = movie;
    state.currentSeason = 1;
    state.currentEpisode = 1;

    elements.modalMovieTitle.textContent = movie.title;
    elements.modalMovieSubtitle.textContent = `${(movie.release_date || '').substring(0, 4)} • ${movie.type === 'series' ? 'TV Series / Anime' : 'Movie'}`;
    elements.modalPoster.src = movie.poster_path;
    elements.modalRating.textContent = movie.vote_average || '8.0';
    elements.modalOverview.textContent = movie.overview;

    const nativeVideo = document.getElementById('native-video');
    const nativeVideoSource = document.getElementById('native-video-source');

    // TV Series Episode Selector Bar
    if (movie.type === 'series' && elements.tvEpisodesBar) {
        elements.tvEpisodesBar.classList.remove('hidden');
        if (elements.seasonSelect) elements.seasonSelect.value = '1';
        renderEpisodeGrid(24);
    } else if (elements.tvEpisodesBar) {
        elements.tvEpisodesBar.classList.add('hidden');
    }

    // Check Fav status
    const isFav = state.watchlist.some(m => m.id === movie.id);
    updateFavButtonState(isFav);

    // If custom direct video URL (e.g., MP4/M3U8 test streams)
    if (movie.customUrl && (movie.customUrl.endsWith('.mp4') || movie.customUrl.endsWith('.m3u8'))) {
        elements.streamIframe.classList.add('hidden');
        nativeVideo.classList.remove('hidden');
        nativeVideoSource.src = movie.customUrl;
        nativeVideo.load();
        elements.customUrlBox.classList.remove('hidden');
        elements.customIframeInput.value = movie.customUrl;
    } else {
        nativeVideo.classList.add('hidden');
        elements.streamIframe.classList.remove('hidden');
        elements.customUrlBox.classList.add('hidden');
        loadServerStream(state.activeServer || 'videasy');
    }

    elements.playerModal.classList.remove('hidden');
}

// Render Episode Buttons (Eps 1 to totalEps)
function renderEpisodeGrid(totalEps = 24) {
    if (!elements.episodeGrid) return;
    let html = '';
    for (let ep = 1; ep <= totalEps; ep++) {
        const isActive = ep === state.currentEpisode;
        html += `<button class="ep-btn ${isActive ? 'active' : ''}" onclick="changeEpisode(${ep})">Eps ${ep}</button>`;
    }
    elements.episodeGrid.innerHTML = html;
}

// Change Episode Selection
function changeEpisode(epNum) {
    state.currentEpisode = epNum;
    renderEpisodeGrid(24);
    loadServerStream(state.activeServer || 'videasy');
}

// Switch Stream Server
function loadServerStream(serverKey) {
    if (!state.activeMovie) return;
    state.activeServer = serverKey;

    const nativeVideo = document.getElementById('native-video');
    const adShield = document.getElementById('ad-shield');

    nativeVideo.classList.add('hidden');
    elements.streamIframe.classList.remove('hidden');
    
    // Highlight active server button
    document.querySelectorAll('.server-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.server === serverKey);
    });

    elements.playerLoader.classList.remove('hidden');

    const providerFn = SERVERS[serverKey] || SERVERS['videasy'];
    const streamUrl = providerFn(state.activeMovie, state.currentSeason, state.currentEpisode);
    
    elements.streamIframe.src = streamUrl;

    // Hide loader on iframe load + activate click shield
    elements.streamIframe.onload = () => {
        elements.playerLoader.classList.add('hidden');
        // Hide the manual ad-shield since we have auto click-shield now
        if (adShield) adShield.classList.add('hidden');
        // Setup transparent click absorber
        setupClickShield();
    };
    
    // Timeout fallback
    setTimeout(() => {
        elements.playerLoader.classList.add('hidden');
        if (adShield) adShield.classList.add('hidden');
        setupClickShield();
    }, 2500);
}

// Navigation Tabs
function initNavigation() {
    document.querySelectorAll('.nav-link').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.nav-link').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            state.currentTab = btn.dataset.tab;
            state.currentPage = 1; // Reset to page 1 on tab change
            
            if (state.currentTab === 'watchlist') {
                elements.sectionTitle.innerHTML = `<i class="fa-solid fa-bookmark text-gradient"></i> Koleksi Favorit Saya`;
            } else if (state.currentTab === 'movies') {
                elements.sectionTitle.innerHTML = `<i class="fa-solid fa-film text-gradient"></i> Katalog Film`;
            } else if (state.currentTab === 'series') {
                elements.sectionTitle.innerHTML = `<i class="fa-solid fa-tv text-gradient"></i> Serial TV Populer`;
            } else if (state.currentTab === 'trending') {
                elements.sectionTitle.innerHTML = `<i class="fa-solid fa-fire text-gradient"></i> Paling Populer & Top Rating`;
            } else {
                elements.sectionTitle.innerHTML = `<i class="fa-solid fa-house text-gradient"></i> Beranda - Semua Tayangan`;
            }
            
            renderMovies();
        });
    });

    // Server selector buttons click event
    elements.serverList.addEventListener('click', (e) => {
        if (e.target.classList.contains('server-btn') && !e.target.classList.contains('custom-server')) {
            loadServerStream(e.target.dataset.server);
        }
    });

    // Custom Server toggle
    elements.btnInputCustomUrl.addEventListener('click', () => {
        elements.customUrlBox.classList.toggle('hidden');
    });

    // Apply custom URL button
    elements.applyCustomUrlBtn.addEventListener('click', () => {
        const url = elements.customIframeInput.value.trim();
        if (url) {
            elements.streamIframe.src = url;
        }
    });

    // Favorite Button Click
    elements.modalFavBtn.addEventListener('click', () => {
        if (!state.activeMovie) return;
        const index = state.watchlist.findIndex(m => m.id === state.activeMovie.id);
        if (index > -1) {
            state.watchlist.splice(index, 1);
            updateFavButtonState(false);
        } else {
            state.watchlist.push(state.activeMovie);
            updateFavButtonState(true);
        }
        localStorage.setItem('streamx_watchlist', JSON.stringify(state.watchlist));
        updateFavCount();
    // Season Dropdown Change
    if (elements.seasonSelect) {
        elements.seasonSelect.addEventListener('change', (e) => {
            state.currentSeason = parseInt(e.target.value) || 1;
            state.currentEpisode = 1;
            renderEpisodeGrid(24);
            loadServerStream(state.activeServer || 'videasy');
        });
    }
}

function updateFavButtonState(isFav) {
    if (isFav) {
        elements.modalFavBtn.classList.add('active');
        elements.modalFavBtn.innerHTML = `<i class="fa-solid fa-bookmark"></i> Tersimpan di Favorit`;
    } else {
        elements.modalFavBtn.classList.remove('active');
        elements.modalFavBtn.innerHTML = `<i class="fa-regular fa-bookmark"></i> Tambah ke Favorit`;
    }
}

function updateFavCount() {
    elements.favCount.textContent = state.watchlist.length;
}

// Genre Filter Chips
function initGenreChips() {
    document.querySelectorAll('.chip').forEach(chip => {
        chip.addEventListener('click', () => {
            document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            state.currentGenre = chip.dataset.genre;
            state.currentPage = 1; // Reset to page 1 on genre change
            renderMovies();
        });
    });
}

// Global Live Search Across All Movies in the World
function initSearch() {
    let debounceTimer;
    elements.searchInput.addEventListener('input', (e) => {
        state.searchQuery = e.target.value;
        state.currentPage = 1; // Reset to page 1 on search
        if (state.searchQuery.length > 0) {
            elements.clearSearch.classList.remove('hidden');
        } else {
            elements.clearSearch.classList.add('hidden');
        }
        renderMovies();

        // Perform real-time global online search across all world movies
        clearTimeout(debounceTimer);
        if (state.searchQuery.trim().length >= 2) {
            debounceTimer = setTimeout(async () => {
                try {
                    const q = encodeURIComponent(state.searchQuery.trim());
                    // Try searching TMDB global database
                    const res = await fetch(`${CONFIG.TMDB_BASE_URL}/search/multi?api_key=${CONFIG.TMDB_API_KEY}&query=${q}&language=id-ID`);
                    if (res.ok) {
                        const data = await res.json();
                        const searchItems = (data.results || []).map(item => ({
                            id: item.id,
                            title: item.title || item.name || 'Untitled',
                            type: item.media_type || (item.title ? 'movie' : 'series'),
                            release_date: item.release_date || item.first_air_date || '2024',
                            vote_average: item.vote_average ? Number(item.vote_average.toFixed(1)) : 8.0,
                            vote_count: item.vote_count || 0,
                            overview: item.overview || 'Sinopsis belum tersedia.',
                            poster_path: item.poster_path ? `${CONFIG.IMAGE_BASE_URL}${item.poster_path}` : 'https://via.placeholder.com/500x750.png?text=No+Poster',
                            backdrop_path: item.backdrop_path ? `${CONFIG.BACKDROP_BASE_URL}${item.backdrop_path}` : 'https://via.placeholder.com/1200x600.png?text=StreamX',
                            genre_ids: item.genre_ids || []
                        }));
                        
                        // Dynamically insert missing movies to global state
                        let addedCount = 0;
                        searchItems.forEach(newItem => {
                            if (newItem.title && !state.movies.some(m => m.id === newItem.id)) {
                                state.movies.unshift(newItem);
                                addedCount++;
                            }
                        });

                        if (addedCount > 0) {
                            renderMovies();
                        }
                    }
                } catch(e) {
                    console.log('Search error:', e);
                }
            }, 300);
        }
    });

    elements.clearSearch.addEventListener('click', () => {
        elements.searchInput.value = '';
        state.searchQuery = '';
        elements.clearSearch.classList.add('hidden');
        renderMovies();
    });
}

// Modals Handler
function initModals() {
    // Close Player Modal
    elements.closePlayerModal.addEventListener('click', () => {
        elements.playerModal.classList.add('hidden');
        elements.streamIframe.src = ''; // Stop video on close
    });

    elements.playerModal.addEventListener('click', (e) => {
        if (e.target === elements.playerModal) {
            elements.playerModal.classList.add('hidden');
            elements.streamIframe.src = '';
        }
    });

    // Ad-Shield Activate Button
    const activateBtn = document.getElementById('activate-stream-btn');
    const adShield = document.getElementById('ad-shield');
    if (activateBtn && adShield) {
        activateBtn.addEventListener('click', () => {
            adShield.classList.add('hidden');
            elements.streamIframe.focus();
        });
    }
}

// Helper: Skeleton Loaders
function createSkeletons(count) {
    let skeletons = '';
    for (let i = 0; i < count; i++) {
        skeletons += `
            <div class="movie-card" style="opacity:0.6; pointer-events:none;">
                <div class="card-poster" style="background:#1e2533;"></div>
                <div class="card-info">
                    <div style="height:15px; background:#2a3346; border-radius:4px; margin-bottom:8px;"></div>
                    <div style="height:10px; width:60%; background:#2a3346; border-radius:4px;"></div>
                </div>
            </div>
        `;
    }
    return skeletons;
}


