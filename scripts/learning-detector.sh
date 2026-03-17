#!/bin/bash

# Learning Detector for CogniCore
# Detects user corrections and feature requests

USER_MESSAGE="$1"

# Correction keywords (Chinese and English)
CORRECTION_KEYWORDS=("不对" "错了" "应该是" "实际上" "no" "wrong" "actually" "you're wrong" "that's incorrect")

# Feature request keywords
FEATURE_KEYWORDS=("能" "可以" "希望" "想要" "can" "could" "wish" "want" "is there a way")

# Check for corrections
for keyword in "${CORRECTION_KEYWORDS[@]}"; do
    if [[ "$USER_MESSAGE" == *"$keyword"* ]]; then
        echo "correction"
        exit 0
    fi
done

# Check for feature requests  
for keyword in "${FEATURE_KEYWORDS[@]}"; do
    if [[ "$USER_MESSAGE" == *"$keyword"* ]]; then
        echo "feature_request"
        exit 0
    fi
done

echo "none"
exit 0
