import json
import csv
import os
import sys

def filter_instagram_column6(csv_path, json_path, output_path=None):
    """
    Filter out rows from a CSV file where the Instagram handle in the 6th column 
    is found in a JSON list.
    
    Args:
        csv_path (str): Path to the CSV file
        json_path (str): Path to the JSON file containing Instagram handles to filter out
        output_path (str, optional): Path for the output filtered CSV
    
    Returns:
        str: Path to the filtered output CSV
    """
    try:
        # Load Instagram handles to filter from JSON file
        print(f"Loading Instagram filter list from: {json_path}")
        with open(json_path, 'r') as file:
            instagram_filter_list = json.load(file)
        
        # Convert all handles to lowercase for case-insensitive comparison
        instagram_filter_lower = [handle.lower() for handle in instagram_filter_list]
        print(f"Found {len(instagram_filter_list)} Instagram handles to filter")
        
        # Set output path if not provided
        if not output_path:
            base_name = os.path.splitext(csv_path)[0]
            output_path = f"{base_name}_filtered.csv"
        
        # Process the file line by line
        print(f"Processing file: {csv_path}")
        
        # First, detect the delimiter
        with open(csv_path, 'r', encoding='utf-8', errors='replace') as sample_file:
            first_line = sample_file.readline()
            dialect = csv.Sniffer().sniff(first_line)
            delimiter = dialect.delimiter
            print(f"Detected delimiter: '{delimiter}'")
            
        # Process file line by line
        total_lines = 0
        filtered_lines = 0
        problem_lines = 0
        
        with open(csv_path, 'r', encoding='utf-8', errors='replace') as input_file:
            with open(output_path, 'w', encoding='utf-8', newline='') as output_file:
                csv_reader = csv.reader(input_file, delimiter=delimiter)
                csv_writer = csv.writer(output_file, delimiter=delimiter)
                
                # Process each line
                for line_num, row in enumerate(csv_reader, 1):
                    total_lines += 1
                    
                    try:
                        # Check if we have at least 6 columns
                        if len(row) >= 6:
                            # Get the Instagram handle from the 6th column (index 5)
                            instagram = row[5].strip().lower()
                            
                            # If Instagram handle is in the filter list, skip this row
                            if instagram in instagram_filter_lower:
                                filtered_lines += 1
                                continue
                        
                        # Keep all other rows
                        csv_writer.writerow(row)
                        
                    except Exception as e:
                        problem_lines += 1
                        print(f"Warning: Skipping problematic line {line_num}: {e}")
        
        # Report results
        print(f"\nProcess completed successfully!")
        print(f"Total lines processed: {total_lines}")
        print(f"Lines filtered out: {filtered_lines}")
        print(f"Problem lines skipped: {problem_lines}")
        print(f"Remaining lines: {total_lines - filtered_lines - problem_lines}")
        print(f"Filtered data saved to: {output_path}")
        
        return output_path
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_path}")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Get file paths from command line arguments or user input
    if len(sys.argv) >= 3:
        csv_path = sys.argv[1]
        json_path = sys.argv[2]
        output_path = sys.argv[3] if len(sys.argv) >= 4 else None
    else:
        print("Instagram Filter Tool - Column 6 Processor")
        print("------------------------------------------")
        csv_path = input("Enter path to CSV file: ")
        json_path = input("Enter path to JSON file with Instagram handles to filter: ")
        output_path = input("Enter path for output CSV (leave blank for default): ")
        if not output_path.strip():
            output_path = None
    
    filter_instagram_column6(csv_path, json_path, output_path)
