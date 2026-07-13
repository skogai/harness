#!/usr/bin/env bash
# env
RESULT=$(skogcli config get "$1.env.$2" --raw)
echo "$RESULT"
