#!/usr/bin/env bash
set -e

if [[ -e /backups/iddatabase.sql ]]; then
    psql -U iduser -d iddatabase -f /backups/iddatabase.sql
fi

if [[ -e /backups/minter.csv && -e /backups/binder.csv ]]; then
    psql -U iduser -d iddatabase -f /backups/migrate.sql
fi
