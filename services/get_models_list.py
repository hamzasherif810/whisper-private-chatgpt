from config.settings import Settings

settings = Settings()

def get_models():
    ollama_models = settings.OLLAMA_MODELS
    models_list = [model.strip() for model in ollama_models.split(",") if model.strip()]
    return models_list