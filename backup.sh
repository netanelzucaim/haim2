#!/bin/bash

# Create the directory if it doesn't exist
current_date=$(date)
# Define the repository details
github_repo="git@github.com:netanelzucaim/backup.git"

# Initialize Git repository if not already initialized
if [ ! -d .git ]; then
    git init
fi

# Add the remote 'origin' if not already added
if ! git remote -v | grep -q "origin"; then
    git remote add origin $github_repo
fi

# Set the remote URL if 'origin' exists
if git remote -v | grep -q "origin"; then
    git remote set-url origin $github_repo
fi

# Example: Add and commit directory
git checkout main
git add -A
git commit -m "backup date $current_date"

# Push changes to GitHub using SSH
git push 

