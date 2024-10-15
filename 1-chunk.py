import os
import json
from datetime import datetime, timedelta

def parse_transcripts(folder_path):
    """
    Parses meeting transcripts from text files in a folder.

    Args:
      folder_path: The path to the folder containing the transcript files.

    Returns:
      A list of strings, where each string represents a speaker's turn with the corresponding timestamp.
    """
    output_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r') as f:
                lines = f.readlines()

            # Extract meeting start time
            first_line = lines[0].strip()
            start_time_str = first_line.split('(')[1].split(')')[0].strip()
            start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M %Z')

            # Initialize variables
            current_time = start_time
            speaker = None
            speech = ""

            # Process transcript lines
            for line in lines[3:]:  # Start from the 4th line (index 3)
                line = line.strip()
                if line.startswith("00:"):
                    # Update timestamp
                    minutes = int(line.split(':')[1])
                    current_time = start_time + timedelta(minutes=minutes)
                elif ":" in line:
                    # Extract speaker and speech
                    if speaker:
                        output_data.append(f"{speaker} ({current_time.strftime('%Y-%m-%d %H:%M %Z')}): {speech.strip()}")
                    speaker, speech = line.split(':', 1)
                else:
                    # Append to current speaker's speech
                    speech += " " + line

            # Add the last speaker's turn
            if speaker:
                output_data.append(f"{speaker} ({current_time.strftime('%Y-%m-%d %H:%M %Z')}): {speech.strip()}")

    return output_data

if __name__ == "__main__":
    transcripts_folder = "transcripts"
    output_filename = "transcripts_chunked.json"

    structured_data = parse_transcripts(transcripts_folder)

    with open(output_filename, 'w') as outfile:
        json.dump(structured_data, outfile, indent=2)

    print(f"Transcripts processed and saved to {output_filename}")
