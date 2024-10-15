import json
import os

import openai
from scipy import spatial

# Load the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Read the prompt from the text file
with open("prompt.txt", "r") as f:
    prompt = f.read()

# Generate an embedding for the prompt
response = openai.embeddings.create(
    input=prompt,
    model="text-embedding-3-small"
)
prompt_embedding = response.data[0].embedding

# Load the transcripts and embeddings from the JSON file
with open("transcripts_embeddings.json", "r") as f:
    transcripts_data = json.load(f)

# Calculate cosine similarity for each transcript
results = []
for transcript in transcripts_data:
    transcript_embedding = transcript["embedding"]
    distance = spatial.distance.cosine(prompt_embedding, transcript_embedding)
    results.append({"document": transcript["document"], "distance": distance})

# Sort the results by cosine similarity
results.sort(key=lambda x: x["distance"])

# Select the top 20 most similar transcripts
top_results = results[:20]

# Save the results to a new JSON file
with open("retrieved_documents.json", "w") as f:
    json.dump(top_results, f, indent=4)
