#!/bin/bash

# Git commit-msg hook to automatically add JIRA ticket from branch name
# This hook runs after the commit message is written but before the commit is created

set -e  # Exit on any error

# Configuration - hardcoded for simplicity
JIRA_PATTERNS=(
    '[A-Z]+-[0-9]+'           # Standard: JIRA-123, ABC-456
    '[A-Z]+[0-9]+'            # No dash: ABC123, PROJECT456
    '[A-Z]{2,}-[0-9]+'        # At least 2 letters: AB-123
    '[a-z]+-[0-9]+'           # Lowercase: jira-123, abc-456
    '[a-z]+[0-9]+'            # Lowercase no dash: abc123, project456
    '[a-z]{2,}-[0-9]+'        # Lowercase at least 2 letters: ab-123
)
SKIP_PREFIXES=("Merge" "Revert" "WIP" "Draft")
JIRA_PREFIX_FORMAT="[{TICKET}] {MESSAGE}"

# Get the commit message file path (first argument)
COMMIT_MSG_FILE=$1

# Read the current commit message
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# Check if commit message starts with any skip prefixes
for prefix in "${SKIP_PREFIXES[@]}"; do
    if [[ "$COMMIT_MSG" =~ ^"$prefix" ]]; then
        exit 0
    fi
done

# Extract JIRA ticket from current branch name
BRANCH_NAME=$(git branch --show-current)
JIRA_TICKET=""

# Try each pattern to find a JIRA ticket
for pattern in "${JIRA_PATTERNS[@]}"; do
    JIRA_TICKET=$(echo "$BRANCH_NAME" | grep -oE "$pattern" | head -1)
    if [ -n "$JIRA_TICKET" ]; then
        break
    fi
done

# Convert patterns without dash to include dash (ABC123 -> ABC-123, abc123 -> ABC-123)
if [ -n "$JIRA_TICKET" ]; then
    if [[ "$JIRA_TICKET" =~ ^[A-Z]+[0-9]+$ ]]; then
        # Uppercase no dash: ABC123 -> ABC-123
    JIRA_TICKET=$(echo "$JIRA_TICKET" | sed 's/\([A-Z]*\)\([0-9]*\)/\1-\2/')
    elif [[ "$JIRA_TICKET" =~ ^[a-z]+[0-9]+$ ]]; then
        # Lowercase no dash: abc123 -> ABC-123
        JIRA_TICKET=$(echo "$JIRA_TICKET" | sed 's/\([a-z]*\)\([0-9]*\)/\1-\2/' | tr '[:lower:]' '[:upper:]')
    elif [[ "$JIRA_TICKET" =~ ^[a-z]+-[0-9]+$ ]]; then
        # Lowercase with dash: abc-123 -> ABC-123
        JIRA_TICKET=$(echo "$JIRA_TICKET" | tr '[:lower:]' '[:upper:]')
    fi
fi

# If we found a JIRA_TICKET, check if it's already in the commit message
if [ -n "$JIRA_TICKET" ]; then
    # Check if JIRA ticket is already present in the commit message
    if ! grep -Fq "[$JIRA_TICKET]" "$COMMIT_MSG_FILE"; then
        # Use a temporary file to safely prepend the ticket
        TMP_FILE=$(mktemp)
        # The trap ensures the temp file is removed on exit, error, or interrupt
        trap 'rm -f "$TMP_FILE"' EXIT HUP INT QUIT TERM

        # Prepend the JIRA ticket to the original message content
        printf "[%s] %s" "$JIRA_TICKET" "$COMMIT_MSG" > "$TMP_FILE"

        # Overwrite the original commit message file
        mv "$TMP_FILE" "$COMMIT_MSG_FILE"

        echo "✅ Added JIRA ticket [$JIRA_TICKET] to commit message from branch: $BRANCH_NAME" >&2
    fi
fi
