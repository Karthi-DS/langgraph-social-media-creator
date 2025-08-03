import os
import re
import requests
from llama_cpp import Llama

MODEL_URL = (
    "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
)
MODEL_PATH = "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"

def download_model_if_needed(url, path):
    if not os.path.exists(path):
        print("⏬ Model not found. Downloading...")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        print("✅ Model download complete.")

# Download if needed before loading
download_model_if_needed(MODEL_URL, MODEL_PATH)

# Load model
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,
    n_threads=8,
    n_batch=512,
    n_gpu_layers=0  # Adjust this if you have GPU support
)

def generate_response(prompt: str, max_tokens=256) -> str:
    try:
        system_msg = (
            "You are a helpful social media content assistant. "
            "Provide concise, creative, and engaging responses."
        )
        formatted_prompt = f"[INST] <<SYS>>{system_msg}<</SYS>> {prompt} [/INST]"

        output = llm(
            prompt=formatted_prompt,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=0.9,
            stop=["</s>", "#", "Day", "INST", "SYS"],
            echo=False
        )
        result = output["choices"][0]["text"].strip()
        return re.sub(r'\[/?[A-Z]+\]', '', result).strip()
    except Exception as e:
        print(f"LLM Error: {str(e)}")
        return ""
