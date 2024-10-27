class revisorConfig:
    base_url = "your_base_url" # such as "https://openrouter.ai/api/v1/chat/completions"
    api_key = "your_api_key" # related to base_url
    model_name = "your_selected_model_for_revisor" # such as "cohere/command-r-plus-08-2024"
    
    # feel free to modify completion options
    class completionOptions:
        temperature = 1
        max_tokens = 2048
        top_p = 1
        min_p = 0
        top_k = None
        frequency_penalty = 0
        presence_penalty = 0

class thinkerConfig:
    base_url = "your_base_url"
    api_key = "your_api_key"
    model_name = "your_selected_model_for_thinker"
    
    class completionOptions:
        temperature = 1
        max_tokens = 2048
        top_p = 1
        min_p = 0
        top_k = None
        frequency_penalty = 0
        presence_penalty = 0

class performerConfig:
    base_url = "your_base_url"
    api_key = "your_api_key"
    model_name = "your_selected_model_for_performer"
    
    class completionOptions:
        temperature = 1
        max_tokens = 2048
        top_p = 1
        min_p = 0
        top_k = None
        frequency_penalty = 0
        presence_penalty = 0
        
