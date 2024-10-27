from chatbot import Chatbot


if __name__ == "__main__":
    try:
        chatbot = Chatbot()
        chatbot.chat_loop()
    except KeyboardInterrupt:
        print("\nChat interrupted. Memories not saved.")
    print("\nThank you for chatting!")