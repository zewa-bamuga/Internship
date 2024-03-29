#!/bin/bash

set -o errexit
set -o pipefail

# Let the DB start
python -m a8t_tools.db.wait_for_db

alembic upgrade head

# Create superuser
if [ -n "${ADMIN_USERNAME}" ]; then
  python manage.py create-superuser "${ADMIN_USERNAME}" "${ADMIN_PASSWORD}" || true
fi

exec "$@"
