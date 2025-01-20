import google.generativeai as genai
import os
from dotenv import load_dotenv

def merge_text_files_by_date(folder_path):
    """
    Merges all text files in the given folder into a single output file, starting with the oldest,
    excluding the 'file_list.txt' file.

    Args:
        folder_path (str): The path to the folder containing the text files.
    """
    output_file = "merged.txt"
    try:
        # Get a list of text files sorted by modification time (oldest first)
        files = [
            os.path.join(folder_path, f) for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.txt') and f != 'file_list.txt'
        ]
        files.sort(key=lambda x: os.path.getmtime(x))  # Sort by modification time
        
        # Merging files
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for file_path in files:
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n')  # Add a new line between file content
        print(f"Files have been merged into {output_file} in order from oldest to newest (excluding 'file_list.txt').")
    except Exception as e:
        print(f"An error occurred: {e}")


def summarize_text_gemini(folder_path, output_dir, language="en-US"):
    """
    Summarizes a text file using the Gemini API and saves the summary to a text file.
    
    Args:
        folder_path (str): The path to the folder containing the text files.
        output_dir (str): The directory where the summary will be saved.
        language (str): The language for the summary (e.g., "en-US", "pl").
    
    Returns:
        str: The file path where the summary was saved, or None on error.
    """
    merge_text_files_by_date(folder_path)
    input_file = "merged.txt"
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("API_GEMINI")
    if not api_key:
        print("Error: The GOOGLE_API_KEY environment variable is not set.")
        return None
    
    # Read the merged text file
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File {input_file} not found")
        return None
    except Exception as e:
        print(f"Error during file reading: {e}")
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    try:
        if language == "pl":
            prompt_prefix = "Napisz streszczenie w języku polskim: "
        else: # Default to English if not Polish
            prompt_prefix = "Give me a summary in English: "
        
        prompt = f"{prompt_prefix} {text}"

        response = model.generate_content(prompt)
        if response.text:
            # Save the summary to a file in output directory
            if not os.path.exists(output_dir):
               os.makedirs(output_dir)
            
            output_file_path = os.path.join(output_dir, "summary.txt")
            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                outfile.write(response.text)
            print(f"Summary saved to {output_file_path}")
            return output_file_path
        else:
            print("Error: Gemini did not return a summary.")
            return None

    except Exception as e:
        print(f"Error during summary generation: {e}")
        return None