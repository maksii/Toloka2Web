#!/bin/bash

# Create a cron job file dynamically
echo "$CRON_SCHEDULE appuser cd /app && python3 -m toloka2MediaServer >> /var/log/cron.log 2>&1" > /etc/cron.d/toloka-job
chmod 0644 /etc/cron.d/toloka-job
crontab -u appuser /etc/cron.d/toloka-job

# Start cron
crond

# Start the web server
exec python -m app