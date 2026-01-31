# Toloka2Web [![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/) [![Docker Hub](https://github.com/maksii/Toloka2Web/actions/workflows/docker_hub.yml/badge.svg?branch=main)](https://github.com/maksii/Toloka2Web/actions/workflows/docker_hub.yml) [![CI](https://github.com/maksii/Toloka2Web/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/maksii/Toloka2Web/actions/workflows/ci.yml)

A web interface for managing Ukrainian anime content with multi-source search, torrent management, and media server integration.

## Features

### Core
- **Multi-source Search** - Search across Toloka torrents, streaming sites, and local anime database simultaneously
- **Release Management** - Track, download, and organize Toloka anime releases with automatic file naming
- **Metadata Integration** - Enrich content with MAL and TheMovieDB data
- **Scheduled Updates** - Cron-based automatic release checking (Docker)

### User Interface
- **Theme Switcher** - Light, Dark, and Auto (system) modes
- **Language Switcher** - English and Ukrainian UI
- **Update Notifications** - Automatic new version alerts from GitHub

### Administration
- **User Management** - Create, edit roles, reset passwords, delete users
- **Role-based Access** - `user` (basic) and `admin` (settings + user management) roles
- **API Documentation** - Interactive Swagger UI at `/api/docs`

## Quick Start

### Prerequisites
- Python 3.10+ or Docker
- Storage space for media files

### First Start

On first launch, the application automatically creates:

| File | Purpose |
|------|---------|
| `data/anime_data.db` | Ukrainian anime database (downloaded) |
| `data/app.ini` | Toloka2MediaServer config template |
| `data/titles.ini` | Release tracking |
| `data/toloka2web.db` | Application database (users, settings) |

Default: Open registration enabled, API keys empty (configure via web UI).

### Docker Installation

```yaml
# docker-compose.yml
services:
  toloka2web:
    image: maksii/toloka2web:latest
    container_name: toloka2web
    volumes:
      - ./config:/app/data
      - ./downloads:/downloads
    environment:
      - PORT=80
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Kiev
      - CRON_SCHEDULE=0 */2 * * *
      - API_KEY=your_api_key_here
      - FLASK_SECRET_KEY=your_random_secret_key
      - JWT_SECRET_KEY=your_jwt_secret_key
    restart: unless-stopped
    user: "${PUID}:${PGID}"
```

```bash
docker-compose up -d
# Access at http://localhost:80
```

### Manual Installation

```bash
git clone https://github.com/maksii/Toloka2Web.git
cd Toloka2Web
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables (Linux/Mac)
export FLASK_SECRET_KEY=your_random_secret_key
export JWT_SECRET_KEY=your_jwt_secret_key
export API_KEY=your_api_key_here
export PORT=5000

python -m app
# Access at http://localhost:5000
```

### API Authentication

Two authentication methods supported:

| Method | Header | Use Case |
|--------|--------|----------|
| JWT Token | `Authorization: Bearer <token>` | API clients, web sessions |
| API Key | `X-API-Key: <key>` | Automated tools, cron jobs |

```bash
# Get JWT token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Use JWT token
curl -H "Authorization: Bearer <access_token>" http://localhost:5000/api/anime

# Use API key
curl -H "X-API-Key: your_api_key" http://localhost:5000/api/anime
```

JWT tokens expire after 1 hour. Use `/api/auth/refresh` with your refresh token to renew.

### Swagger UI

Interactive API documentation available at `/api/docs`:
- Local: `http://localhost:5000/api/docs`
- Docker: `http://localhost:80/api/docs`

Click "Authorize" to authenticate with JWT (`Bearer <token>`) or API Key.

## Configuration

### Environment Variables

**Required:**

| Variable | Description |
|----------|-------------|
| `FLASK_SECRET_KEY` | Flask session secret (`openssl rand -hex 32`) |
| `JWT_SECRET_KEY` | JWT token secret (`openssl rand -hex 32`) |
| `API_KEY` | API access key for automated tools |

**Optional:**

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `5000` | Web interface port |
| `HOST` | `0.0.0.0` | Bind address |
| `TZ` | `Europe/Kiev` | Timezone |
| `CORS_ORIGINS` | `*` | Allowed CORS origins |
| `PUID/PGID` | - | User/Group ID (Docker) |
| `CRON_SCHEDULE` | `0 */2 * * *` | Auto-update schedule (Docker) |

### Web UI Settings

Configure in Settings page (admin only):
- **MAL API Key** - MyAnimeList integration
- **TMDB API Key** - TheMovieDB integration
- **Open Registration** - Allow new user signups

### INI Files

The app syncs settings bidirectionally with INI files for [Toloka2MediaServer](https://github.com/CakesTwix/Toloka2MediaServer) compatibility:
- `data/app.ini` - Toloka credentials, download paths, media server config
- `data/titles.ini` - Release tracking

## Related Projects

| Project | Description |
|---------|-------------|
| [Toloka2Python](https://github.com/CakesTwix/toloka2python) | Toloka API wrapper |
| [Toloka2MediaServer](https://github.com/CakesTwix/Toloka2MediaServer) | Media server integration |
| [Stream2MediaServer](https://github.com/maksii/Stream2MediaServer) | Streaming site support |

## Contributing

- **Issues**: Bug reports and feature requests via GitHub Issues
- **PRs**: Fork → feature branch → Pull Request
- Use English for code comments

## License

[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)
