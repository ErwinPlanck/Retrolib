#!/bin/bash

ROOT="$(cd "$(dirname "$0")" && pwd)"

cd "$ROOT/Tools/scripts"

exec python3 retrolib.py