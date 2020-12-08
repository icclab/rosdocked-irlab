#!/bin/bash
set -ex

RUN_ICEWM=${RUN_ICEWM:-yes}

case $RUN_ICEWM in
  false|no|n|0)
    rm -f /app/conf.d/icewm.conf
    ;;
esac

exec supervisord -c /app/supervisord.conf
