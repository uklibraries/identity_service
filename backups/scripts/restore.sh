#!/usr/bin/env bash
set -e

psql -U iduser -d iddatabase -f /backups/iddatabase.sql
