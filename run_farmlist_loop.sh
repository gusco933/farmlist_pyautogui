#!/bin/sh

set -eu

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
python_script="$script_dir/click_farmlist_button.py"
venv_activate="$script_dir/.venv/bin/activate"

base_interval="${1:-70}"
variation="${2:-5}"

case "$base_interval" in
  ''|*[!0-9]*)
    echo "Usage: $0 [base_interval_seconds] [variation_seconds]" >&2
    echo "Example: $0 70 5" >&2
    exit 1
    ;;
esac

case "$variation" in
  ''|*[!0-9]*)
    echo "Usage: $0 [base_interval_seconds] [variation_seconds]" >&2
    echo "Example: $0 70 5" >&2
    exit 1
    ;;
esac

if [ ! -f "$python_script" ]; then
  echo "Error: missing Python script at $python_script" >&2
  exit 1
fi

if [ ! -f "$venv_activate" ]; then
  echo "Error: missing virtual environment at $venv_activate" >&2
  exit 1
fi

. "$venv_activate"

while :; do
  # Run Python unbuffered so prints/tracebacks are flushed immediately, and keep stderr visible
  if ! python3 -u "$python_script" 2>&1; then
    exit_code=$?
    echo "Python script exited with code ${exit_code}" >&2
  fi

  offset=$(awk -v variation="$variation" 'BEGIN { srand(); print int(rand() * (variation * 2 + 1)) - variation }')
  sleep_seconds=$((base_interval + offset))

  if [ "$sleep_seconds" -lt 1 ]; then
    sleep_seconds=1
  fi

  echo "Sleeping for ${sleep_seconds}s before the next run..."
  sleep "$sleep_seconds"
done