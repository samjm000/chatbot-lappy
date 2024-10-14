import llama_cpp
import os
import sys

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the script directory
os.chdir(script_dir)

# Construct the relative path
model_path = os.path.join("..", "..", "LLM", "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf")

# Convert to absolute path
absolute_model_path = os.path.abspath(model_path)
print(f"Absolute model path: {absolute_model_path}")

# Verify if the path exists
if not os.path.exists(absolute_model_path):
    raise ValueError(f"Model path does not exist: {absolute_model_path}")

# Load the GGUF model
model = llama_cpp.Llama(model_path=absolute_model_path)

# Function to generate a response
def generate_response(question):
    response = model.generate(question)
    return response

if __name__ == "__main__":
    print("Running test")
    print(os.getcwd())
