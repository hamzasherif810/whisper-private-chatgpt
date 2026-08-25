from llama_index.llms.ollama import Ollama
from config.settings import Settings

settings = Settings()
OLLAMA_URL = settings.OLLAMA_URL

# client = Ollama(model=settings.OLLAMA_URL, base_url=settings.OLLAMA_URL)
current_model_name = None
current_llm_instance = None


def get_llm(model_name: str):
    global current_llm_instance, current_model_name
    if model_name == current_model_name:
        return current_llm_instance
    current_llm_instance = Ollama(base_url=OLLAMA_URL, model=model_name)
    current_model_name = model_name
    return current_llm_instance
