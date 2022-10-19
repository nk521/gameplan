#!/bin/bash
set -euxo pipefail

function init_bench() {
    bench init --skip-redis-config-generation frappe-bench

    cd frappe-bench

    # Use containers instead of localhost
    bench set-mariadb-host mariadb
    bench set-redis-cache-host redis:6379
    bench set-redis-queue-host redis:6379
    bench set-redis-socketio-host redis:6379

    # Remove redis, watch from Procfile
    sed -i '/redis/d' ./Procfile
    sed -i '/watch/d' ./Procfile

    bench get-app gameplan

    bench new-site gameplan.localhost \
    --force \
    --mariadb-root-password $MARIADB_ROOT_PASSWORD \
    --admin-password $BENCH_ADMIN_PASSWORD \
    --no-mariadb-socket

    bench --site gameplan.localhost install-app gameplan
    bench --site gameplan.localhost set-config developer_mode $BENCH_DEVELOPER_MODE
    bench --site gameplan.localhost clear-cache
    bench --site gameplan.localhost set-config mute_emails $BENCH_MUTE_EMAILS
    bench use gameplan.localhost
}

if [[ ! -e /tmp/wait-for-it.sh ]]; then
    curl https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh > /tmp/wait-for-it.sh
fi

chmod +x /tmp/wait-for-it.sh
/tmp/wait-for-it.sh mariadb:3306

if [[ -d "/home/frappe/frappe-bench/apps/frappe" ]]; then
    echo "Bench already exists, skipping init"
    cd frappe-bench
else
    echo "Creating new bench..."
    init_bench
fi

# Just run bench, no fallback to bash/sh upon bench termination
exec bench start