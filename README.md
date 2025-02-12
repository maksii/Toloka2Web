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
- Python or Docker
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
set JWT_SECRET_KEY=your_jwt_secret_key  # Required for JWT authentication
# On Linux/Mac:
export FLASK_SECRET_KEY=your_random_secret_key
export PORT=5000
export API_KEY=your_api_key_here
export JWT_SECRET_KEY=your_jwt_secret_key  # Required for JWT authentication
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

### API Authentication

The API supports two authentication methods:

1. **JWT Token** (for API clients):
```bash
# Get tokens
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Use token
curl -H "Authorization: Bearer your_access_token" http://localhost:5000/api/anime
```

2. **API Key** (for automated tools):
```bash
curl -H "X-API-Key: your_api_key" http://localhost:5000/api/anime
```

Note: Some endpoints (like `/api/settings`) require admin privileges. Use an admin account for JWT auth or the API key.

### API Documentation (Swagger UI)

The API documentation is available through Swagger UI, which provides an interactive interface to explore and test the API endpoints.

#### Accessing Swagger UI
- When running locally: `http://localhost:5000/api/docs`
- Docker installation: `http://localhost:80/api/docs`

#### Features
- Interactive API documentation
- Request/response examples for each endpoint
- Built-in API testing interface
- Authentication support (JWT Token and API Key)
- Detailed error responses
- Schema definitions for all models

#### Authentication Setup
1. **Getting JWT Token**:
   - Use the `/api/auth/login` endpoint in Swagger UI
   - Or use cURL:
     ```bash
     curl -X POST http://localhost:5000/api/auth/login \
       -H "Content-Type: application/json" \
       -d '{"username": "your_username", "password": "your_password"}'
     ```
   - The response will contain `access_token` and `refresh_token`
   - Access tokens expire after 1 hour
   - Use the `/api/auth/refresh` endpoint with your refresh token to get a new access token

2. **API Key**:
   - The API key is set through the `API_KEY` environment variable when starting the application
   - For Docker: Set in your `docker-compose.yml`
   - For manual installation: Set in your environment
   - The key specified in `API_KEY` will be your authentication key

#### Using Swagger UI
1. Navigate to the Swagger UI URL
2. Click the "Authorize" button at the top
3. Choose your authentication method:
   - For JWT: Enter `Bearer your_token` in the "bearerAuth" field
   - For API Key: Enter your key in the "X-API-KEY" field
4. Click "Authorize" to save
5. Explore and test the available endpoints

Note: The documentation is automatically generated from the codebase and always reflects the current API state.

### Configuration

#### Environment Variables
- `PUID/PGID`: Set to match your user/group ID (run `id` command to find yours)
- `CRON_SCHEDULE`: Update frequency in cron format (Docker only)
- `API_KEY`: Key for accessing API endpoints without authentication (used by cron jobs)
- `FLASK_SECRET_KEY`: Random string used for session security (required)
- `PORT`: Web interface port (default: 5000)
- `TZ`: Timezone (default: Europe/Kiev)
- `CORS_ORIGINS`: Comma-separated list of allowed CORS origins (default: http://localhost:5173)

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

