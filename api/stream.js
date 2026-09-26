// Vercel Serverless Function: Stream Proxy for Indonesian Movies (Rebahin / JuicyCodes / Embed Servers)
// Serves clean, direct HTML5 video player without external website wrapper, headers, or slot ads.
const https = require('https');
const http = require('http');

function resolveTarget(urlOrB64) {
    if (!urlOrB64) return null;
    let str = decodeURIComponent(urlOrB64).trim();
    if (str.includes('source=')) {
        const b64 = str.split('source=')[1].split('&')[0];
        try {
            const dec = Buffer.from(b64, 'base64').toString('utf8');
            if (dec.startsWith('http')) return dec;
        } catch (e) {}
    }
    if (!str.startsWith('http')) {
        try {
            const dec = Buffer.from(str, 'base64').toString('utf8');
            if (dec.startsWith('http')) return dec;
        } catch (e) {}
    }
    return str;
}

function fetchWithReferer(targetUrl, userAgent, maxRedirects = 3) {
    return new Promise((resolve, reject) => {
        if (maxRedirects < 0) return reject(new Error('Too many redirects'));
        let u;
        try {
            u = new URL(targetUrl);
        } catch (e) {
            return reject(new Error('Invalid URL: ' + targetUrl));
        }

        const client = u.protocol === 'http:' ? http : https;
        const req = client.get(targetUrl, {
            headers: {
                'User-Agent': userAgent || 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://rebahinxxi3.mom/',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            },
            rejectUnauthorized: false
        }, (res) => {
            if ([301, 302, 303, 307, 308].includes(res.statusCode) && res.headers.location) {
                const nextUrl = new URL(res.headers.location, targetUrl).toString();
                return resolve(fetchWithReferer(nextUrl, userAgent, maxRedirects - 1));
            }
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => resolve({ statusCode: res.statusCode, data, url: targetUrl, origin: u.origin }));
        });
        req.on('error', reject);
    });
}

module.exports = async function handler(req, res) {
    // Enable CORS & Frame embedding
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS');
    res.setHeader('X-Frame-Options', 'ALLOWALL');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    const { url, source } = req.query;
    const targetInput = url || source;

    if (!targetInput) {
        return res.status(400).send('<h3>Parameter url atau source diperlukan.</h3>');
    }

    const directUrl = resolveTarget(targetInput);
    if (!directUrl) {
        return res.status(400).send('<h3>Format link stream tidak valid.</h3>');
    }

    // Direct redirect for YouTube embeds
    if (/youtube\.com|youtu\.be/.test(directUrl)) {
        return res.redirect(302, directUrl);
    }

    try {
        let userAgent = req.headers['user-agent'] || '';
        if (!userAgent.includes('Mozilla')) {
            userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';
        }
        let result = await fetchWithReferer(directUrl, userAgent);

        // If returned page is Rebahin iembed wrapper, extract inner iframe and fetch direct player
        const iframeMatch = result.data.match(/<iframe[^>]+src=[\x27\x22]([^\x27\x22]+)[\x27\x22]/i);
        if (iframeMatch && iframeMatch[1] && (result.data.length < 1000 || result.data.includes('iembed'))) {
            result = await fetchWithReferer(iframeMatch[1], userAgent);
        }

        let html = result.data;
        // Inject <base> tag so relative styles, player scripts, and ping endpoints resolve properly
        if (!html.includes('<base ') && html.includes('<head>')) {
            html = html.replace('<head>', `<head>\n<base href="${result.origin}/">`);
        }

        // Add responsive full-bleed styling for seamless player inside modal iframe
        const customStyle = `<style>
            html, body { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: #000; }
            .player-wrap, #jc-player { width: 100% !important; height: 100% !important; }
        </style>`;
        if (html.includes('</head>')) {
            html = html.replace('</head>', `${customStyle}\n</head>`);
        } else {
            html = customStyle + html;
        }

        res.setHeader('Content-Type', 'text/html; charset=utf-8');
        res.setHeader('Cache-Control', 'public, max-age=1800, s-maxage=3600');
        return res.status(result.statusCode || 200).send(html);
    } catch (err) {
        console.error('Stream proxy error:', err);
        return res.status(502).send(`
            <div style="background:#000;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;font-family:sans-serif;">
                <p style="font-size:18px;margin-bottom:12px;">Gagal memuat pemutar video film.</p>
                <a href="${directUrl}" target="_blank" style="padding:10px 20px;background:#e50914;color:#fff;text-decoration:none;border-radius:8px;font-weight:bold;">
                    Buka Pemutar Video Langsung
                </a>
            </div>
        `);
    }
};
