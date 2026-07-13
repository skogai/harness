#!/bin/bash
# date executable

case "$1" in
"now")
  date "+%Y-%m-%d %H:%M:%S"
  ;;
"unix")
  date +%s
  ;;
"")
  date "+%Y-%m-%d"
  ;;
*)
  date "+%Y-%m-%d"
  ;;
esac
