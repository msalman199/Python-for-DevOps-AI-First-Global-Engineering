#!/bin/bash

# File Integrity Checker Script
# This script generates and verifies file checksums

# TODO: Add function to generate checksums
generate_checksums() {
    local directory="$1"
    local output_file="checksums.sha256"
    
    # TODO: Generate SHA256 for all files in directory
    # Hint: Use find command to locate files, then sha256sum
    
    echo "Checksums saved to $output_file"
}

# TODO: Add function to verify checksums
verify_checksums() {
    local checksum_file="$1"
    
    # TODO: Verify files against saved checksums
    # Hint: Use sha256sum -c command
    
}

# Main script logic
case "$1" in
    generate)
        # TODO: Call generate_checksums function
        ;;
    verify)
        # TODO: Call verify_checksums function
        ;;
    *)
        echo "Usage: $0 {generate|verify}"
        exit 1
        ;;
esac

#!/bin/bash

# File Integrity Checker Script

generate_checksums() {
    local directory="${1:-.}"
    local output_file="checksums.sha256"
    
    echo "Generating checksums for files in $directory..."
    find "$directory" -type f -name "*.txt" -exec sha256sum {} \; > "$output_file"
    echo "Checksums saved to $output_file"
}

verify_checksums() {
    local checksum_file="${1:-checksums.sha256}"
    
    if [ ! -f "$checksum_file" ]; then
        echo "Error: Checksum file not found!"
        exit 1
    fi
    
    echo "Verifying file integrity..."
    sha256sum -c "$checksum_file"
}

case "$1" in
    generate)
        generate_checksums "$2"
        ;;
    verify)
        verify_checksums "$2"
        ;;
    *)
        echo "Usage: $0 {generate|verify} [path]"
        exit 1
        ;;
esac
