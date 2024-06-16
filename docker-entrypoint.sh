#!/bin/bash

# Ensure environment variables are available
if [ -z "$CRON_SCHEDULE" ] || [ -z "$PORT" ]; then
  echo "Required environment variables are missing."
  exit 1
fi

# Create a cron job file dynamically
echo "$CRON_SCHEDULE cd /app && curl -X POST http://127.0.0.1:$PORT/api/releases/ -H 'x-api-key: your_api_key_here' >> /var/log/cron.log 2>&1" > /etc/cron.d/toloka-job
chmod 0644 /etc/cron.d/toloka-job
crontab -u appuser /etc/cron.d/toloka-job

# Start cron
crond

# Start the web server
exec python -m app