from huggingface_hub import hf_hub_download
from llama_cpp import Llama

"""
Downloads GGUF model files from Hugging Face Hub and loads them using the llama_cpp library.

This script handles multiple models, some of which are split into multiple files (e.g., 7B and 14B models).
Each model's files are downloaded using the `huggingface_hub` library, and then the Llama model is loaded
using `llama_cpp`. Finally, it runs a prompt to demonstrate the model's generation capabilities.

Models:
    - Qwen2.5-0.5B, 1.5B, 3B: Single GGUF file.
    - Qwen2.5-7B, 14B: Multiple GGUF files (splitted into parts).

Note: For split models, only the first file in the series is passed to the Llama model loader.
"""

# List of models to download
models = [
    {
        "repo_id": "Qwen/Qwen2.5-0.5B-Instruct-GGUF",
        "filenames": ["qwen2.5-0.5b-instruct-q4_k_m.gguf"],
        "verbose": False,
    },
    {
        "repo_id": "Qwen/Qwen2.5-1.5B-Instruct-GGUF",
        "filenames": ["qwen2.5-1.5b-instruct-q4_k_m.gguf"],
        "verbose": False,
    },
    {
        "repo_id": "Qwen/Qwen2.5-3B-Instruct-GGUF",
        "filenames": ["qwen2.5-3b-instruct-q4_k_m.gguf"],
        "verbose": False,
    },
    {
        "repo_id": "Qwen/Qwen2.5-7B-Instruct-GGUF",
        "filenames": [
            "qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf",
            "qwen2.5-7b-instruct-q4_k_m-00002-of-00002.gguf",
        ],
        "verbose": False,
    },
    {
        "repo_id": "Qwen/Qwen2.5-14B-Instruct-GGUF",
        "filenames": [
            "qwen2.5-14b-instruct-q4_k_m-00001-of-00003.gguf",
            "qwen2.5-14b-instruct-q4_k_m-00002-of-00003.gguf",
            "qwen2.5-14b-instruct-q4_k_m-00003-of-00003.gguf",
        ],
        "verbose": False,
    },
]

for model in models:
    repo_id = model["repo_id"]
    filenames = model["filenames"]

    # Download each file associated with the model from Hugging Face Hub
    for filename in filenames:
        hf_hub_download(repo_id=repo_id, filename=filename)

    # Load the model using the first file in the series (in case of split models)
    llm = Llama.from_pretrained(
        repo_id=repo_id,
        filename=filenames[
            0
        ],  # Only the first file is passed, llama_cpp handles the rest
        verbose=model["verbose"],
    )

    # Generate a response from the model with a specific prompt
    output = llm(
        "Q: Name the planets in the solar system? A: ",  # Prompt
        max_tokens=None,  # Generate up to the end of the context window
        stop=["Q:", "\n"],  # Stop generation before it generates a new question
        echo=True,  # Echo the prompt back in the output
    )

    # Print the generated output
    print(output["choices"])  # noqa: T201
