from llama_cpp import Llama

llm = Llama.from_pretrained(
    repo_id="Qwen/Qwen2-0.5B-Instruct-GGUF",
    filename="*q4_K_M.gguf",
    verbose=True
)
