FROM python:3.13-alpine

# Install system dependencies
RUN apk add --no-cache \
    bash \
    curl \
    git \
    dcron \
    ffmpeg \
    tzdata \
 && addgroup -S appgroup \
 && adduser -S appuser -G appgroup

# Set the timezone
ENV TZ=Europe/Kyiv
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

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

# Setup environment
ENV PORT=5000 \
    CRON_SCHEDULE="0 8 * * *"

# Prepare the entrypoint
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Switch to the non-root user
USER appuser

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["crond", "-f", "-d", "8"]