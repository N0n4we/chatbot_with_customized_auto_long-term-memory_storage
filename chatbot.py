from client import revisor, thinker, performer
from utils import format_chat_history
from dao import DataAccess
from string import Template
import os
import json
import time

class Chatbot:
    def __init__(self):
        # Initialize data access to load all memory and prompts
        self.dao = DataAccess("data")
        self.chat_history_path = os.path.join("data/memo", "ChatHistory")

    def save_chat_history(self, messages):
        """Save chat history to file"""
        try:
            with open(self.chat_history_path, 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
            print("\nChat history saved successfully!")
        except Exception as e:
            print(f"\nError saving chat history: {e}")

    def load_chat_history(self):
        """Load chat history from file if it exists"""
        try:
            if os.path.exists(self.chat_history_path):
                with open(self.chat_history_path, 'r', encoding='utf-8') as f:
                    messages = json.load(f)
                print("Previous chat history loaded!")
                return messages
        except Exception as e:
            print(f"Error loading chat history: {e}")
        return None

    def clean_chat_history(self):
        """Remove chat history file"""
        try:
            if os.path.exists(self.chat_history_path):
                os.remove(self.chat_history_path)
        except Exception as e:
            print(f"\nError cleaning chat history: {e}")

    def get_character_prompt(self):
        """Get character prompt with chatbot name substituted"""
        if self.dao.setting.chatbotCharacter and self.dao.setting.chatbotName:
            return Template(self.dao.setting.chatbotCharacter).substitute(
                chatbotName=self.dao.setting.chatbotName
            )
        return "You are a friendly chatbot."

    def build_variable_pool(self, messages=None, user_input=None, updated_memories=None):
        """Build a pool of all available variables for template substitution"""
        # Start with settings
        pool = {
            "chatbotName": self.dao.setting.chatbotName or "",
            "chatbotCharacter": self.dao.setting.chatbotCharacter or "",
        }
        
        # Add memories
        pool.update({
            "events": self.dao.memo.events or "",
            "selfImage": self.dao.memo.selfImage or "",
            "thoughts": self.dao.memo.thoughts or "",
            "moodAndReasons": self.dao.memo.moodAndReasons or "",
            "userInfo": self.dao.memo.userInfo or "",
            "userCharacter": self.dao.memo.userCharacter or "",
            "relationship": self.dao.memo.relationship or "",
        })
        
        # Add conversation context if provided
        if messages is not None:
            pool["chatHistory"] = format_chat_history(messages[:-1] if user_input else messages)
        if user_input is not None:
            pool["userInput"] = user_input
            
        # Add updated memories if provided (for final thoughts generation)
        if updated_memories:
            pool.update(updated_memories)
        
        return pool

    def generate_response(self, messages, user_input):
        """Generate response using MemoEnsemble with full memory context"""
        # Build variable pool with conversation context
        variables = self.build_variable_pool(messages, user_input)
        
        # Create a temporary message list with clear system and user messages
        temp_messages = [
            {
                "role": "system",
                "content": Template(self.dao.prompt.memoEnsemble).substitute(variables)
            },
            {"role": "user", "content": user_input}
        ]
        
        response = performer.request(temp_messages)
        return response

    def update_memories(self, messages):
        """Update memory files when user leaves"""
        try:
            # Build initial variable pool
            variables = self.build_variable_pool(messages)
            total_steps = 7  # Updated total steps to include SelfImage
            current_step = 0
            updated_memories = {}  # Store updated memories for final thoughts

            def update_progress():
                nonlocal current_step
                current_step += 1
                progress = (current_step / total_steps) * 50  # 50 characters wide progress bar
                print(f"\rUpdating memories: [{'#' * int(progress)}{' ' * (50 - int(progress))}] {current_step}/{total_steps}", end="")
            
            memory_updates = [
                ("Events", revisor, "eventsRevision"),
                ("MoodAndReasons", thinker, "moodRevision"),
                ("Relationship", revisor, "relationshipRevision"),
                ("UserInfo", revisor, "userInfoRevision"),
                ("UserCharacter", revisor, "userCharacterRevision"),
                ("SelfImage", revisor, "selfImageRevision")
            ]

            for memory_name, client, prompt_name in memory_updates:
                try:
                    print(f"\nUpdating {memory_name}...")
                    response = client.revise(
                        template=getattr(self.dao.prompt, prompt_name),
                        **variables
                    )
                    if response:
                        with open(os.path.join("data/memo", memory_name), 'w', encoding='utf-8') as f:
                            f.write(response['content'])
                        updated_memories[memory_name.lower()] = response['content']
                    update_progress()
                except Exception as e:
                    print(f"\nError updating {memory_name}: {e}")
                    # Continue with other updates even if one fails
                time.sleep(1)  # Reduced sleep time
            
            # Finally, update Thoughts using all updated memories
            try:
                print("\nGenerating final thoughts...")
                final_variables = self.build_variable_pool(messages, updated_memories=updated_memories)
                thoughts_response = thinker.revise(
                    template=self.dao.prompt.overthinking,
                    **final_variables
                )
                if thoughts_response:
                    with open(os.path.join("data/memo", "Thoughts"), 'w', encoding='utf-8') as f:
                        f.write(thoughts_response['content'])
                update_progress()
                
                print("\n\nMemo's Final Thoughts:")
                print("="*50)
                print(thoughts_response['content'] if thoughts_response else "No thoughts generated")
                print("="*50)
            except Exception as e:
                print(f"\nError updating Thoughts: {e}")
            
            print("\nMemories have been updated!")
            
        except Exception as e:
            print(f"\nError in memory update process: {e}")

    def chat_loop(self):
        # Try to load previous chat history
        messages = self.load_chat_history()
        
        # If no previous history, initialize with system context
        if not messages:
            character_prompt = self.get_character_prompt()
            messages = [{"role": "system", "content": character_prompt}]
        
        print("Chat started! (Type '/leave' to end and save memories, '/save' to save chat history)")
        print("-" * 50)
        
        # Print last few messages from history if any
        if len(messages) > 1:  # More than just system message
            print("\nLast few messages from previous chat:")
            for msg in messages[-3:]:  # Show last 3 messages
                if msg["role"] != "system":
                    prefix = "You: " if msg["role"] == "user" else f"{self.dao.setting.chatbotName}: "
                    print(f"{prefix}{msg['content']}")
            print("-" * 50)
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Check for commands
                if user_input.lower() == '/leave':
                    print("\nUpdating memories before leaving...")
                    self.update_memories(messages)
                    self.clean_chat_history()  # Clean up chat history after updating memories
                    break
                elif user_input.lower() == '/save':
                    self.save_chat_history(messages)
                    break
                    
                # Add user message to history
                messages.append({"role": "user", "content": user_input})
                
                # Get response using MemoEnsemble
                response = self.generate_response(messages, user_input)
                if response and isinstance(response, dict):
                    messages.append(response)
                    print(f"{self.dao.setting.chatbotName}: {response['content']}")
                
            except Exception as e:
                print(f"Error in chat loop: {e}")
                print("Continuing chat...")
                continue
