FROM python:3.12.4-alpine3.20

# Install system dependencies
RUN apk add --no-cache \
    sudo \
    bash \
    curl \
    git \
    dcron \
    ffmpeg 

# Create a group and user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Define volumes
VOLUME /app/data
VOLUME /app/downloads

# Set file ownership
RUN chown -R appuser:appgroup /app
USER appuser

ENV PORT=5000

# Copy and prepare the entrypoint
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Set default cron schedule and command to start cron
ENV CRON_SCHEDULE="0 8 * * *"
CMD ["crond", "-f", "-d", "8"]