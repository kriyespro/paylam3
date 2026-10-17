#!/bin/sh
set -eu

# Runs inside the postgres:16-alpine image (has pg_dump built in) as a
# dedicated compose service — loops forever, dumping once a day and
# pruning dumps older than RETENTION_DAYS. Not cron: cron in a minimal
# Alpine container needs its own daemon/logging setup for no real benefit
# over a plain sleep loop at this scale.

RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-14}"
INTERVAL_SECONDS="${BACKUP_INTERVAL_SECONDS:-86400}"

echo "Backup service started. Retention: ${RETENTION_DAYS} days, interval: ${INTERVAL_SECONDS}s."

while true; do
    timestamp=$(date +%Y%m%d_%H%M%S)
    dest="/backups/thebasics_${timestamp}.sql.gz"
    echo "$(date): starting backup -> ${dest}"

    if PGPASSWORD="$POSTGRES_PASSWORD" pg_dump \
        --host="$POSTGRES_HOST" \
        --username="$POSTGRES_USER" \
        --dbname="$POSTGRES_DB" \
        --no-owner --no-privileges \
        | gzip > "$dest"; then
        echo "$(date): backup OK ($(du -h "$dest" | cut -f1))"
    else
        echo "$(date): backup FAILED" >&2
        rm -f "$dest"
    fi

    find /backups -name 'thebasics_*.sql.gz' -mtime "+${RETENTION_DAYS}" -delete
    echo "$(date): pruned backups older than ${RETENTION_DAYS} days"

    sleep "$INTERVAL_SECONDS"
done
