# Toloka2Web [![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/) [![CI](https://github.com/maksii/Toloka2Web/actions/workflows/docker_hub.yml/badge.svg?branch=main)](https://github.com/maksii/Toloka2Web/actions/workflows/docker_hub.yml)

A web interface for managing anime content, with features for searching, downloading, and organizing media from various sources. Primarily focused on Ukrainian anime content management.

## Features

- Search and download content from Toloka
- Automatic file naming and organization
- Integration with MAL and TheMovieDB for metadata
- Scheduled updates via cron jobs
- Local database for studios and anime tracking
- Docker-based deployment for easy setup

## Quick Start

### Prerequisites
- Python 3.12+ or Docker
- Storage space for media files
- (Optional) Plex Media Server

### First Start Behavior

On first start, the application will automatically:

1. Create or download required files:
   - `data/anime_data.db`: Downloads the anime database
   - `data/app.ini`: Downloads template from Toloka2MediaServer
   - `data/titles.ini`: Creates empty file for release tracking
   - `data/toloka2web.db`: Creates SQLite database for application data

2. Initialize the database with:
   - Default application settings
   - User authentication tables
   - Release tracking tables

3. Default settings include:
   - Open registration enabled
   - Empty MAL and TMDB API keys (configure in web interface)

The application will create these files automatically, but you can also pre-configure them by placing them in the data directory before starting.

### Docker Installation

1. Create required directories:
```bash
mkdir -p /path/to/your/config
mkdir -p /path/to/your/downloads
```

2. Create a docker-compose.yml file:
```yaml
version: '3.8'
services:
  toloka2web:
    image: maksii/toloka2web:latest
    container_name: toloka2web
    volumes:
      - /path/to/your/config:/app/data
      - /path/to/your/downloads:/path/to/your/downloads
    environment:
      - PORT=80
      - PUID=1024  # Your user ID
      - PGID=100   # Your group ID
      - CRON_SCHEDULE=0 */2 * * *  # Update schedule
      - TZ=Europe/Kiev
      - API_KEY=your_api_key_here  # Key for automated API access
      - FLASK_SECRET_KEY=your_random_secret_key  # Used for session security
    restart: unless-stopped
    user: "${PUID}:${PGID}"
```

3. Start the container:
```bash
docker-compose up -d
```

4. Access the web interface at `http://localhost:80`

### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/maksii/Toloka2Web.git
cd Toloka2Web
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# On Windows:
set FLASK_SECRET_KEY=your_random_secret_key
set PORT=5000
set API_KEY=your_api_key_here
# On Linux/Mac:
export FLASK_SECRET_KEY=your_random_secret_key
export PORT=5000
export API_KEY=your_api_key_here
```

5. Create data directories:
```bash
mkdir -p data/downloads
```

6. Run the application:
```bash
python -m app
```

7. Access the web interface at `http://localhost:5000`

### Configuration

#### Environment Variables
- `PUID/PGID`: Set to match your user/group ID (run `id` command to find yours)
- `CRON_SCHEDULE`: Update frequency in cron format (Docker only)
- `API_KEY`: Key for accessing API endpoints without authentication (used by cron jobs)
- `FLASK_SECRET_KEY`: Random string used for session security (required)
- `PORT`: Web interface port (default: 5000)
- `TZ`: Timezone (default: Europe/Kiev)

#### External Service API Keys
Third-party service API keys are managed through the web interface:
1. Log in as admin
2. Go to Settings
3. Configure the following keys:
   - MAL API Key: Required for MyAnimeList integration
   - TMDB API Key: Required for TheMovieDB integration

## Contributing

1. **Bug Reports & Feature Requests**
   - Use GitHub Issues for bugs and feature requests
   - Include steps to reproduce for bugs
   - Provide clear use cases for features

2. **Code Contributions**
   - Fork the repository
   - Create a feature branch
   - Submit a Pull Request
   - Keep changes focused and maintainable
   - Use English for code comments

3. **Related Projects**
   - [Toloka2Python](https://github.com/CakesTwix/toloka2python) - Core functionality
   - [Toloka2MediaServer](https://github.com/CakesTwix/Toloka2MediaServer) - Media server integration
   - [Stream2MediaServer](https://github.com/maksii/Stream2MediaServer) - Streaming support

## License

[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)

