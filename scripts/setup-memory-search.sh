#!/bin/bash

# Setup SQLite FTS5 for CogniCore memory search
# Uses current working directory as workspace

if [ -z "$COGNICORE_WORKSPACE" ]; then
    # Default to current directory if not set
    WORKSPACE="$PWD"
else
    WORKSPACE="$COGNICORE_WORKSPACE"
fi

# Use OpenClaw standard memory location if available
if [ -d "$HOME/.openclaw/workspace" ]; then
    # Find the first workspace directory
    FIRST_WORKSPACE=$(ls -1 "$HOME/.openclaw/workspace" | head -1)
    if [ -n "$FIRST_WORKSPACE" ]; then
        WORKSPACE="$HOME/.openclaw/workspace/$FIRST_WORKSPACE"
    fi
fi

MEMORY_DB_DIR="$HOME/.openclaw/memory"
MEMORY_DB="$MEMORY_DB_DIR/xiaozhang.sqlite"

# Create directories
mkdir -p "$WORKSPACE/memory"
mkdir -p "$MEMORY_DB_DIR"

# Initialize SQLite database with FTS5
if [ ! -f "$MEMORY_DB" ]; then
    sqlite3 "$MEMORY_DB" "CREATE VIRTUAL TABLE memory_fts USING fts5(date, content, priority, tokenize='porter');"
    echo "Memory search database initialized: $MEMORY_DB"
else
    # Check if FTS table exists
    if ! sqlite3 "$MEMORY_DB" ".tables" | grep -q "memory_fts"; then
        sqlite3 "$MEMORY_DB" "CREATE VIRTUAL TABLE memory_fts USING fts5(date, content, priority, tokenize='porter');"
        echo "Memory FTS table created"
    fi
fi

# Index existing memory files
echo "Indexing existing memory files in: $WORKSPACE/memory"
for memory_file in "$WORKSPACE/memory"/*.md; do
    if [ -f "$memory_file" ]; then
        date_part=$(basename "$memory_file" .md)
        # Read file content and insert into FTS
        content=$(cat "$memory_file" | tr '\n' ' ')
        # Extract priority from content (if any)
        if [[ "$content" == *"[PRIORITY: high]"* ]]; then
            priority="high"
        elif [[ "$content" == *"[PRIORITY: medium]"* ]]; then
            priority="medium"
        else
            priority="low"
        fi
        sqlite3 "$MEMORY_DB" "INSERT INTO memory_fts (date, content, priority) VALUES ('$date_part', '$content', '$priority');"
        echo "Indexed: $memory_file"
    fi
done

echo "Memory search setup completed!"
