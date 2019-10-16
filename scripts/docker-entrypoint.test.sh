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

echo
echo $PREFIX "Run tests"
coverage run --source '.' --omit 'env/*' manage.py test --no-input || true
coverage report --show-missing -m
coverage html -d reports/htmlcov/
coverage xml -o reports/coverage.xml
rm .coverage

echo
echo $PREFIX "Restoring user permissions"
chown -R $TEST_UID:$TEST_GID .
