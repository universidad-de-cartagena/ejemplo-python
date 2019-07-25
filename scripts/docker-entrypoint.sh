#!/usr/bin/env sh
# -e exit       when a command fails
# -u exit       when trying to use undefined variable
# -o pipefail   return the exit code of piped commands that fail
# -x            debug

# https://www.gnu.org/software/bash/manual/bashref.html#index-expansion_002c-parameter
# ${ENV_VAR?"Error message"}    Requires the ENV_VAR and gives human readable stderr
set -euo pipefail

PREFIX="[*]"

# echo
echo $PREFIX "Django check"
python3 manage.py check

echo
echo $PREFIX "Current migrations in database"
mkdir -p database/
touch database/db.sqlite3
python3 manage.py showmigrations

echo
echo $PREFIX "Running migrations on database"
python3 manage.py migrate --no-input

# echo
# echo $PREFIX "ENV Variables"
# echo $PREFIX "- APP_UID" $APP_UID
# echo $PREFIX "- APP_GID" $APP_GID
# echo $PREFIX "- HARAKIRI_TIMEOUT" $HARAKIRI_TIMEOUT
# echo $PREFIX "- STATS" ${STATS:-"Not enabled"}
# echo $PREFIX "- PROCESSES" $PROCESSES
# echo $PREFIX "- DEBUG" $DEBUG

exec "$@"