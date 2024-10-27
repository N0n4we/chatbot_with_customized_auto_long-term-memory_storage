

with open('./data/setting/ChatbotName', 'r', encoding='utf-8') as file:
    chatbotName = file.read().strip()

def try_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
    return wrapper

@try_decorator
def format_chat_history(messages):
    """
    Convert a list of message dictionaries into a formatted string with role and content.
    Each message is on a new line.
    
    Args:
        messages (list): List of dictionaries with 'role' and 'content' keys
        
    Returns:
        str: Formatted string with each message on a new line
    """
    if not messages:
        return ""
        
    formatted_messages = []
    for msg in messages:
        role = msg.get('role', '')
        content = msg.get('content', '')
        if role == "assistant":
            role = chatbotName
        formatted_messages.append(f"{role}: {content}")
            
    return "\n".join(formatted_messages)
