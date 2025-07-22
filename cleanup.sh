#!/bin/bash

# UNED Scraper Cleanup Script
# This script removes all generated files and directories from the scraper

echo "🧹 UNED Scraper Cleanup"
echo "======================="
echo

# Function to safely remove files/directories
safe_remove() {
    if [ -e "$1" ]; then
        echo "Removing: $1"
        rm -rf "$1"
        echo "✓ Removed: $1"
    else
        echo "⚠️  Not found: $1"
    fi
}

# Remove PDF directory and all contents
echo "Cleaning up PDF downloads..."
safe_remove "pdfs"

# Remove degree structure files
echo
echo "Cleaning up degree structure files..."
safe_remove "degree_structure.json"
safe_remove "degree_structure.txt"

# Remove any temporary files that might be created
echo
echo "Cleaning up temporary files..."
safe_remove "temp_page.html"
safe_remove "*.tmp"

echo
echo "🎉 Cleanup completed!"
echo
echo "The following files/directories have been removed:"
echo "  • pdfs/ (directory and all contents)"
echo "  • degree_structure.json"
echo "  • degree_structure.txt"
echo "  • Any temporary files"
echo
echo "You can now run the scraper again for a fresh start."
