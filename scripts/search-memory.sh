#!/bin/bash

# Search memory using SQLite FTS5
# Uses current working directory as workspace

if [ -z "$COGNICORE_WORKSPACE" ]; then
    WORKSPACE="$PWD"
else
    WORKSPACE="$COGNICORE_WORKSPACE"
fi

MEMORY_DB_DIR="$HOME/.openclaw/memory"
MEMORY_DB="$MEMORY_DB_DIR/xiaozhang.sqlite"
QUERY="$1"

if [ -z "$QUERY" ]; then
    echo "Usage: $0 <search_query>"
    exit 1
fi

if [ ! -f "$MEMORY_DB" ]; then
    echo "Memory database not found. Run setup-memory-search.sh first."
    exit 1
fi

# Perform FTS search
echo "Searching for: $QUERY"
echo "Results:"
echo "=========="
sqlite3 "$MEMORY_DB" "SELECT date, priority, substr(content, 1, 200) as snippet FROM memory_fts WHERE content MATCH '$QUERY' ORDER BY priority DESC, date DESC LIMIT 5;"
