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

On first launch, the application bootstraps these files (all in the repo `data/` directory):

| File | Purpose | Source |
|------|---------|--------|
| `data/anime_data.db` | Ukrainian anime database | Downloaded from Stream2MediaServer repo |
| `data/app.ini` | Toloka2MediaServer configuration template | Downloaded from Toloka2MediaServer repo |
| `data/titles.ini` | Release tracking | Created empty if missing |
| `data/toloka2web.db` | Application database (users, settings) | Created by SQLAlchemy |

Default: Open registration enabled, API keys empty (configure via web UI).

### First Run (Step-by-Step, full guide)

#### 0) Prerequisites
1. **Python 3.10+ or Docker**.
2. **Torrent client** (choose one): qBittorrent or Transmission.
3. **Toloka account** (credentials will go into `data/app.ini`).
4. **Toloka2MediaServer config format**: Toloka2Web uses the Toloka2MediaServer config schema and template for `data/app.ini`.
5. Optional: MAL and TMDB API keys for metadata.

#### 1) Get the app running
Choose one of these:

**Docker (recommended)**:
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
      - API_KEY=replace_with_api_key
      - FLASK_SECRET_KEY=replace_with_flask_secret
      - JWT_SECRET_KEY=replace_with_jwt_secret
    restart: unless-stopped
    user: "${PUID}:${PGID}"
```
```bash
docker-compose up -d
# Open http://localhost:80
```
Security notes for Docker environment variables:
- **FLASK_SECRET_KEY**: Protects Flask sessions and CSRF tokens. Required for login and form security. Use a long random string.
- **JWT_SECRET_KEY**: Signs JWT access/refresh tokens. Required for API auth; if it changes, existing tokens become invalid.
- **API_KEY**: Simple header key for automated tools (sent as `X-API-Key`). Treat it like a password.

If you leave the example values (`replace_with_*`), the app will still start, but it is insecure and not recommended. At minimum, change them to any unique string. Best practice is a random 32+ character secret, for example:
```bash
openssl rand -hex 32  # example output: 9f2e8c... (64 hex chars)
```
Use the generated value for each secret.

**Manual (virtualenv)**:
```bash
git clone https://github.com/maksii/Toloka2Web.git
cd Toloka2Web
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Secret values (required for secure auth)
# - FLASK_SECRET_KEY: protects sessions/CSRF
# - JWT_SECRET_KEY: signs JWT tokens
# - API_KEY: header key for automation (X-API-Key)
#
# You can use any unique string, but random values are safer.
export FLASK_SECRET_KEY=$(openssl rand -hex 32)
export JWT_SECRET_KEY=$(openssl rand -hex 32)
export API_KEY=$(openssl rand -hex 32)
export PORT=5000

python -m app
# Open http://localhost:5000
```

#### 2) Confirm bootstrap files and sources
After the first start, check the `data/` directory:
- `data/anime_data.db` (downloaded from Stream2MediaServer: `https://github.com/maksii/Stream2MediaServer/raw/main/data/anime_data.db`).
- `data/app.ini` (downloaded from Toloka2MediaServer: `https://raw.githubusercontent.com/CakesTwix/Toloka2MediaServer/main/data/app-example.ini`).
- `data/titles.ini` (created empty if missing).
- `data/toloka2web.db` (created by SQLAlchemy).

#### 3) Register the first user (admin)
1. Open `http://localhost:<port>`.
2. Go to **Register**.
3. Submit the form. The first account becomes **admin**. Later accounts become **user**.
4. If registration is closed, see **Settings → Configuration → toloka2web → open_registration**.

#### 4) Verify that the app works if `data/app.ini` is empty
If `data/app.ini` exists but is empty, the app still starts:
- Web settings (`open_registration`, `mal_api`, `tmdb_api`) are added to the DB.
- You can log in and open **Settings**.
- Toloka and torrent features will not work until `data/app.ini` is populated.

#### 5) Configure settings from the UI (full path actions)
Use **Settings** (admin only). All `data/app.ini` entries are editable from the UI. The Configuration table maps directly to `data/app.ini`:

- **Path:** `Settings → Configuration`
  - Table columns are **Section / Key / Value**.
  - Each row maps to INI:
    - `Section` = `[Section]`
    - `Key` = `key = value`
  - To save a change:
    1. Edit the row fields.
    2. Click the **Save** button at the end of the row.
    3. Click **Sync to app.ini** to write DB changes to `data/app.ini`.
  - Use the top-right buttons:
    - **Add** = create a new row (fill Section/Key/Value, then **Save**).
    - **Sync to app.ini** = write DB settings → `data/app.ini`.
    - **Sync from app.ini** = read `data/app.ini` → DB.

- **Path:** `Settings → System`
  - **Sync titles.ini from DB** = write DB releases → `data/titles.ini`.
  - **Sync titles.ini to DB** = read `data/titles.ini` → DB.
- **Path:** `Settings → System → Show Versions` (displays package versions).
- **Path:** `Settings → Configuration → Add` (add a new setting row).
- **Path:** `Settings → Configuration → Save` (save row changes).
- **Path:** `Settings → Configuration → Sync to app.ini` (write to file).
- **Path:** `Settings → Configuration → Sync from app.ini` (load from file).

#### 6) Configure Toloka + torrent client (ini + UI mapping)
Add or edit these settings in **Settings → Configuration** and sync to `data/app.ini`:

**Web settings (toloka2web section):**
```ini
[toloka2web]
open_registration = True
mal_api = your_mal_api_key
tmdb_api = your_tmdb_api_key
```

**Toloka section (required):**
```ini
[Toloka]
username = toloka_username
password = toloka_password
client = qbittorrent  # or transmission
default_download_dir = /downloads/anime
default_meta = [WEBRip-1080p][UK+JA][Ukr Sub]
```

**qBittorrent (if `client=qbittorrent`):**
```ini
[qbittorrent]
host = localhost
port = 8080
username = qb_user
password = qb_password
protocol = http
category = sonarr
tag = toloka
```

**Transmission (if `client=transmission`):**
```ini
[transmission]
host = localhost
port = 9091
username = trans_user
password = trans_password
protocol = http
rpc = /transmission/rpc
category = sonarr
tag = tolokaAnime
```

**Optional logging:**
```ini
[Python]
logging = INFO
```

#### 7) Validate from the UI
1. Use the top navigation **Search** field, enter a query, and submit.
   - Search results open in an offcanvas panel titled **Search Results**.
   - **Toloka** tab shows torrent rows with actions:
     - **Direct Download** (downloads the `.torrent`).
     - **Add to client** (adds torrent to configured client).
     - **Copy Values** (opens **Add Release** and pre-fills fields).
2. From the **Toloka** tab, click **Copy Values** on a row:
   - The **Add Release** modal opens with the Toloka URL, title, and release group prefilled.
   - If file details are available, the **Index Extractor** panel opens and you can click a detected number to set **Episode Index**.
3. Complete the **Add Release** form:
   - **Toloka URL** must start with `https://toloka.to/`.
   - **Title** can be cleaned with **Cut Title** (scissors icon).
   - **Season** and **Episode Index** are required.
   - **Index Correction** is optional; use it if the source numbering needs adjustment.
   - **Release Group & Meta** is optional (meta defaults from `Toloka.default_meta` if set).
   - **Ongoing** toggles episode range naming (S01E01-E## vs S01).
4. Click **Submit**. The **Operation Results** offcanvas opens:
   - **Response Code** shows status: `SUCCESS`, `FAILURE`, or another status.
   - **Operation Logs** show step-by-step processing output.
   - **Titles References** and **Torrent References** show affected items.
5. First add can take time depending on torrent size and client responsiveness. Wait for the results panel.
6. If anything fails, re-check:
   - `Settings → Configuration` rows.
   - Sync direction (from/to `app.ini`).
   - Torrent client connectivity.

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

#### `data/app.ini` required settings

Minimum keys needed for Toloka + torrent operations are shown in the **First Run** section above.

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
