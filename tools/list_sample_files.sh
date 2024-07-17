#!/bin/bash

# list_sample_files.sh
# Description: This script defines a function that generates a list of a specified percentage of the files from each folder within a specified directory.
# The list is saved in a text file, with each entry containing the folder and file path. These files can then be used to set up the 
# LISA annotation tool (https://www.robots.ox.ac.uk/~vgg/software/via/app/lisa/lisa.html).

# Author: Cait Newport
# Date: 2024-07-17
#
# Usage:
# 1. Save this script to a file, e.g., list_sample_files.sh.
# 2. Make the script executable: chmod +x list_sample_files.sh.
# 3. Run the script with the directory path and percentage as arguments: ./list_sample_files.sh "/path/to/directory" percentage.
#    Alternatively, you can call the function directly within another script.
#
# Example:
#   ./list_sample_files.sh "/path/to/directory" 10
#
# Function:
# - list_sample_files(directory, percentage):
#   Takes a directory and percentage as arguments, lists all folders in that directory, and creates a list of the specified percentage of the files in each folder.
#   The list is saved to a text file named "sample_files_list.txt", with each folder and file path on its own line.
#   The function saves the file list in the current working directory.
#
# Dependencies:
# - The script uses basic Unix commands such as ls, sort, and standard file operations.
#
# Notes:
# - Ensure that the specified directory exists and contains subfolders with files.
# - The output file (sample_files_list.txt) will be created or overwritten in the current working directory.

list_sample_files() {
    local dir="$1"
    local percentage="$2"
    local output_file="sample_files_list.txt"

    echo "Starting the script..."
    echo "Directory to process: $dir"
    echo "Percentage to sample: $percentage%"

    # Check if the directory exists
    if [[ ! -d "$dir" ]]; then
        echo "Error: Directory '$dir' does not exist."
        return 1
    fi

    # Check if the percentage is a valid number
    if ! [[ "$percentage" =~ ^[0-9]+$ ]] || [ "$percentage" -le 0 ] || [ "$percentage" -gt 100 ]; then
        echo "Error: Percentage must be a positive integer between 1 and 100."
        return 1
    fi

    echo "Directory exists. Proceeding..."

    # Empty or create the output file
    > "$output_file"
    if [[ $? -ne 0 ]]; then
        echo "Error: Failed to initialize output file $output_file"
        return 1
    fi
    echo "Output file initialized: $output_file"

    # Loop through each folder in the directory
    for folder in "$dir"/*; do
        if [[ -d "$folder" ]]; then
            echo "Processing folder: $folder"

            # Get all files in the folder
            files=("$folder"/*)
            echo "Number of files in folder: ${#files[@]}"

            # Check if folder is empty
            if [[ ${#files[@]} -eq 1 && ! -e "${files[0]}" ]]; then
                echo "No files found in folder: $folder"
                continue
            fi

            # Calculate the number of sample files
            num_files=${#files[@]}
            if (( num_files == 0 )); then
                echo "No files found in folder: $folder"
                continue
            fi
            num_sample=$(( (num_files * percentage + 99) / 100 )) # Calculate percentage and round up
            echo "Number of sample files to select: $num_sample"

            # Shuffle and get a sample of the specified percentage
            sample_files=$(ls "$folder" | sort -R | head -n $num_sample)
            if [[ $? -ne 0 ]]; then
                echo "Error: sort command failed in folder $folder"
                return 1
            fi

            # Write to output file
            for file in $sample_files; do
                echo "Adding file to list: $folder/$file"
                echo "$folder/$file" >> "$output_file"
                if [[ $? -ne 0 ]]; then
                    echo "Error: Failed to write to output file $output_file"
                    return 1
                fi
            done
        else
            echo "Skipping non-directory item: $folder"
        fi
    done

    echo "Sample file list created at $output_file"
}

# Check if two arguments are provided
if [[ $# -ne 2 ]]; then
    echo "Usage: $0 /path/to/directory percentage"
    exit 1
fi


# Call the function with the provided directory and percentage
list_sample_files "$1" "$2"


