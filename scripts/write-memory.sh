#!/bin/bash

# Write memory entry and update FTS index
# Uses current working directory as workspace

if [ -z "$COGNICORE_WORKSPACE" ]; then
    WORKSPACE="$PWD"
else
    WORKSPACE="$COGNICORE_WORKSPACE"
fi

# Use OpenClaw standard memory location if available
if [ -d "$HOME/.openclaw/workspace" ]; then
    FIRST_WORKSPACE=$(ls -1 "$HOME/.openclaw/workspace" | head -1)
    if [ -n "$FIRST_WORKSPACE" ]; then
        WORKSPACE="$HOME/.openclaw/workspace/$FIRST_WORKSPACE"
    fi
fi

MEMORY_DB_DIR="$HOME/.openclaw/memory"
MEMORY_DB="$MEMORY_DB_DIR/xiaozhang.sqlite"
DATE=$(date +%Y-%m-%d)
PRIORITY=${2:-"low"}
CONTENT="$1"

# Create memory directory
mkdir -p "$WORKSPACE/memory"

# Write to daily memory file
echo "[$(date '+%H:%M')] [PRIORITY: $PRIORITY] $CONTENT" >> "$WORKSPACE/memory/$DATE.md"

# Update FTS index
if [ -f "$MEMORY_DB" ]; then
    sqlite3 "$MEMORY_DB" "INSERT INTO memory_fts (date, content, priority) VALUES ('$DATE', '$CONTENT', '$PRIORITY');"
fi

echo "Memory written: $DATE.md"
