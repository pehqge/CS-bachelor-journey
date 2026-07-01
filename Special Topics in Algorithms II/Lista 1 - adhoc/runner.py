import os
import subprocess

def run_program_and_compare_outputs(letter):
    # Define the input and output folder paths
    total = 0
    errors = 0
    input_folder = f"{letter}_input/"
    output_folder = f"{letter}_output/"
    program = f"{letter}.py"
    wrong = []
    
    # Ensure the input and output folders exist
    if not os.path.exists(input_folder) or not os.path.exists(output_folder):
        print("Input or output folder does not exist.")
        return

    # Find all input files in the input folder that match the pattern letter_*.txt
    input_files = [f for f in os.listdir(input_folder) if f.startswith(f"{letter.upper()}_")]

    # Loop through each input file
    for input_file in input_files:
        input_path = os.path.join(input_folder, input_file)
        output_file = input_file.replace(f"{letter}_", "")  # Expected output filename
        output_path = os.path.join(output_folder, output_file)

        if not os.path.exists(output_path):
            print(f"Expected output file not found: {output_path}")
            continue

        # Run the Python program with the input file
        try:
            # Capture the output from running letter.py
            result = subprocess.run(
                ['python3', program],
                input=open(input_path).read(),
                text=True,
                capture_output=True,
                check=True
            )
            program_output = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running {program}: {e}")
            continue

        # Read the expected output
        with open(output_path, 'r') as f:
            expected_output = f.read().strip()
        total += 1
        # Compare the program's output with the expected output
        if program_output != expected_output:
            errors += 1
            wrong.append(input_file)
            print(f"Output mismatch for input file {input_file}:")
            print(f"Expected:\n{expected_output}")
            print(f"Got:\n{program_output}")
        else:
            print(f"Output correct for input file {input_file}.")
            
    print(f"Total: {total}, Errors: {errors}, Percentage: {((total - errors) / total) * 100}%")
    print("Wrong files:", wrong)

if __name__ == "__main__":
    letter = input("Enter the letter: ").strip()
    run_program_and_compare_outputs(letter)