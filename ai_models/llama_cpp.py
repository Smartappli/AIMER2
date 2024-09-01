from llama_cpp import Llama

llm = Llama.from_pretrained(
    repo_id="Qwen/Qwen2-0.5B-Instruct-GGUF",
    filename="*q4_K_M.gguf",
    verbose=True,
)
output = llm(
    "Q: Name the planets in the solar system? A: ",  # Prompt
    max_tokens=32,  # Generate up to 32 tokens, set to None to generate up to the end of the context window
    stop=[
        "Q:",
        "\n",
    ],  # Stop generating just before the model would generate a new question
    echo=True,  # Echo the prompt back in the output
)  # Generate a completion, can also call create_completion
print(output)  # noqa: T201
