#!/bin/bash
set -euo pipefail

echo "Waiting for Postgres..."
python <<'EOF'
import os
import sys
import time

import psycopg

url = os.environ["DATABASE_URL"]
for attempt in range(30):
    try:
        psycopg.connect(url, connect_timeout=3).close()
        break
    except psycopg.OperationalError:
        print(f"  Postgres not ready yet (attempt {attempt + 1}/30)...")
        time.sleep(2)
else:
    print("Postgres never became available.", file=sys.stderr)
    sys.exit(1)
EOF
echo "Postgres is up."

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting: $*"
exec "$@"
