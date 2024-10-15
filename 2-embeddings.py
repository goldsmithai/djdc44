import openai
import json
import os

# Load the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_embeddings(input_file, output_file):
    """
    Generates embeddings for each JSON object in the input file and outputs a new JSON file with embeddings.

    Args:
      input_file: Path to the input JSON file.
      output_file: Path to the output JSON file.
    """

    with open(input_file, 'r') as f:
        data = json.load(f)

    embeddings = []
    for document in data:
        response = openai.embeddings.create(
            input=document,
            model="text-embedding-3-small"
        )
        embeddings.append({
            "document": document,
            "embedding": response.data[0].embedding
        })

    with open(output_file, 'w') as f:
        json.dump(embeddings, f, indent=4)

if __name__ == "__main__":
    generate_embeddings("transcripts_chunked.json", "transcripts_embeddings.json")
