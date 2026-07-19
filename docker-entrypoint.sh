#!/bin/bash

# Check required environment variables
if [ -z "$CRON_SCHEDULE" ] || [ -z "$PORT" ]; then
  echo "Required environment variables are missing."
  exit 1
fi

# Set the API key from environment variable or use default.
# Must match the Flask default in app/app.py so the cron curl authenticates
# even when API_KEY is not explicitly set.
API_KEY=${API_KEY:-default_api_key}

# Create a cron job file dynamically
(crontab -l 2>/dev/null; echo "$CRON_SCHEDULE curl -X POST http://127.0.0.1:$PORT/api/releases/update -H 'x-api-key: $API_KEY'") | crontab -u appuser -

# Start cron in the foreground to handle logs better
crond -f -L /dev/stdout &

# Start the web server
exec python -m app