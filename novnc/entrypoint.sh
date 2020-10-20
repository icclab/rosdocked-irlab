#!/bin/bash
set -ex

RUN_FLUXBOX=${RUN_FLUXBOX:-yes}

case $RUN_FLUXBOX in
  false|no|n|0)
    rm -f /app/conf.d/fluxbox.conf
    ;;
esac

exec supervisord -c /app/supervisord.conf
