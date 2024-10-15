import openai
import json
import os

# Load the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Read the prompt from the text file
with open("prompt.txt", "r") as f:
    user_prompt = f.read()

# Read the retrieved documents from the JSON file
with open("retrieved_documents.json", "r") as f:
    retrieved_documents = json.load(f)

# Format the documents into a single string
formatted_documents = ""
for doc in retrieved_documents:
    formatted_documents += f"{doc['document']} ({doc['distance']})\n\n"

# Create the user message
user_message = f"{formatted_documents}\n\n{user_prompt}"

with open("final_prompt.txt", "w") as f:
    f.write(user_message)

# Create the chat completion request
completion = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "Answer the user's prompt based on the provided documents.",
        },
        {"role": "user", "content": user_message},
    ],
)

# Print the model's response to a file
with open("final_output.txt", "w") as f:
    f.write(completion.choices[0].message.content)
