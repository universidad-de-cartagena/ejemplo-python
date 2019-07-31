#!/usr/bin/env bash
# -e exit       when a command fails
# -u exit       when trying to use undefined variable
# -o pipefail   return the exit code of piped commands that fail
# -x            debug

set -euo pipefail

PREFIX="[*]"

echo $PREFIX "Django check"
touch ejemploPython/.env
python3 manage.py check

echo
echo $PREFIX "Current migrations in database"
mkdir -p database/
touch database/db.sqlite3
python3 manage.py showmigrations

echo
echo $PREFIX "Running migrations on database"
python3 manage.py migrate --no-input

exec "$@"
