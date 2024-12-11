import requests
import base64
from PIL import Image
import io
import os

#endpoint = "INSERT"
endpoint = "INSERT"
#api_key = "INSERT"
api_key = "INSERT"
deployment_name = "gpt-4o"

def read_local_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except Exception as e:
        print (f"Error reading local input file: {e}")
        return ""

def update_user_bio(conversation_summary, latest_message, core_memories, existing_user_bio):
    try:
        # Generate response from GPT-4o
        system_prompt = load_system_prompt('./long-term-memory-system/system_prompt_user_persona.txt')
        system_prompt = {
            "role": "system",
            "content": system_prompt
        }

        message = "Conversation Summary:\n" + conversation_summary + "\nCore Memories\n" + core_memories + "\nExisting User Profile:\n" + existing_user_bio + "\nLatest User Message:\n" + latest_message + '\n'
        message = {
            "role": "system",
            "content": message
        }

        response = requests.post(
            endpoint,
            headers={
                'api-key': f'{api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-4o',
                'messages': [system_prompt, message],
                'temperature': 0
            }
        )
        
        response_data = response.json()
        assistant_message = response_data['choices'][0]['message']
        print(f"\n\nUpdated user bio: {assistant_message['content']}\n\n")
        return assistant_message['content']
    except Exception as e:
        print(f"Error updating user persona: {e}")


def update_conversation_summary(conversation_summary, filtered_messages):
    try:
        # Generate response from GPT-4o
        formatted_messages = ""
        for message in filtered_messages:
            role = message['role']
            content = message.get('content', '')
            formatted_messages += "\n" + role + ": " + content + "\n"

        system_prompt = load_system_prompt("./long-term-memory-system/system_prompt_summary.txt")
        system_prompt = {
            "role": "system",
            "content": system_prompt
        }

        print(f"\n\nConversation summary: {conversation_summary}\nFormatted Messages: {formatted_messages}\n\n")
        user_message = "Existing Conversation Summary: \n" + conversation_summary + "\n Most Recent Messages: \n" + formatted_messages + "\n"
        user_message = {
            "role": "user",
            "content": user_message
        }

        response = requests.post(
            endpoint,
            headers={
                'api-key': f'{api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-4o',
                'messages': [system_prompt, user_message],
                'temperature': 0
            }
        )
        
        response_data = response.json()
        assistant_message = response_data['choices'][0]['message']
        print(f"Updated conversation summary: {assistant_message['content']}")
        return assistant_message['content']
        
    except Exception as e:
        print(f"Error updating conversation summary: {e}")
        return conversation_summary

def generate_context_list(conversation_summary, user_input, core_memories):
    try:
        system_prompt = load_system_prompt('./long-term-memory-system/system_prompt_relevant_list.txt')
        system_prompt = {
            "role": "system",
            "content": system_prompt
        }
        print(conversation_summary)
        print(user_input)
        print(core_memories)
        message = "\n\nConversation Summary:\n" + conversation_summary + "\n\nLatest User Input:\n" + user_input + "\n\nCore Memories:\n" + core_memories
        message = {
            "role": "user",
            "content": message
        }

        response = requests.post(
            endpoint,
            headers={
                'api-key': f'{api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-4o',
                'messages': [system_prompt, message],
                'temperature': 0
            }
        )
        
        response_data = response.json()
        assistant_message = response_data['choices'][0]['message']
        print(f"\n\nUpdated context list: {assistant_message['content']}\n\n")
        return assistant_message['content']

    except Exception as e:
        print(f"Error generating context list: {e}")
        return ""

def toggle_personality(core_memories, context_list, user_context_list, user_input, current_personality):
    try:
        system_prompt = load_system_prompt('./long-term-memory-system/system_prompt_personality_switch.txt')
        system_prompt = {
            "role": "system",
            "content": system_prompt
        }

        user_message = "Core Memories:\n" + core_memories + "Current Context:\n" + context_list + "\nUser Profile:\n" + user_context_list + "\nCurrent User Input:\n" + user_input + "\nLatest Personality:\n" + current_personality
        user_message = {
            "role": "user",
            "content": user_message
        }

        response = requests.post(
            endpoint,
            headers={
                'api-key': f'{api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-4o',
                'messages': [system_prompt, user_message],
                'temperature': 0
            }
        )
        
        response_data = response.json()
        assistant_message = response_data['choices'][0]['message']
        print(f"Updated personality: {assistant_message['content']}")
        return assistant_message['content'] 
    except Exception as e:
        print(f"Error toggling personalities: {e}")
        return current_personality

def update_core_memory(recent_messages, conversation_summary, existing_core_memories):
    try:
        system_prompt = load_system_prompt('./long-term-memory-system/system_prompt_core_memory.txt')
        system_prompt = {
            "role": "system",
            "content": system_prompt
        }

        formatted_messages = ""
        for message in recent_messages:
            role = message['role']
            content = message.get('content', '')
            formatted_messages += "\n" + role + ": " + content + "\n"
        user_message = "Recent conversation history:\n" + formatted_messages + "\nFull conversation summary:\n" + conversation_summary + "Existing memories:\n" + existing_core_memories
        user_message = {
            "role": "user",
            "content": user_message
        }

        response = requests.post(
            endpoint,
            headers={
                'api-key': f'{api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-4o',
                'messages': [system_prompt, user_message],
                'temperature': 0
            }
        )

        response_data = response.json()
        print(f'Core Memory Assistant Message: {response_data}')
        assistant_message = response_data['choices'][0]['message']
        print(f"Updated core memories: {assistant_message['content']}")
        return assistant_message['content']
    except Exception as e:
        print(f'Error while updating core memories: {e}')
        return existing_core_memories

def load_system_prompt(file_path):
    """Load system prompt from a text file"""
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"System prompt file '{file_path}' not found.")
        return ""

def save_chat_transcript(messages, file_path):
    """Save chat transcript to a text file"""
    try:
        with open(file_path, 'w') as file:
            for message in messages:
                role = message['role']
                content = message.get('content', '')
                file.write(f"{role.capitalize()}: {content}\n")
                # If there are images, indicate that in the transcript
                if 'images' in message:
                    file.write(f"{role.capitalize()}: [Image]\n")
        print(f"Chat transcript saved to '{file_path}'")
    except Exception as e:
        print(f"Error saving chat transcript: {e}")

def chat_with_gpt4o():
    print("Starting chat with GPT-4o (type 'quit' to exit)")
    print("To analyze an image, type 'image' followed by the path to your image file")
    
    # Load system prompt - Always start out with a positive personality
    #system_prompt = load_system_prompt('system_prompt_good_notetaker.txt')
    
    # Store conversation history
    messages = []
    conversation_summary = ""
    user_bio = ""
    core_memories = ""
    personality = ""
    # if system_prompt:
    #     # Add system prompt to the conversation
    #     messages.append({
    #         "role": "system",
    #         "content": system_prompt
    #     })
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            # Save the chat transcript before exiting
            save_chat_transcript(messages, 'chat_transcript.txt')
            break

        if user_input.lower() == 'read-file':
            message = {
                "role": "user",
                "content": read_local_file('input_file.txt')
            }
            
        else:
            # Handle text input
            message = {
                "role": "user",
                "content": user_input
            }
        
        # Before requesting a response from GPT, introduce the personality toggling mechanism
        # The updated personality system prompt will go in before the user's message, and so that bit of code comes later.

        if user_input.lower() != 'read-file':
            # Step 1: Ask the summary generator to update the summary based on the current sliding window
            messages.append(message)
            filtered_messages = [message for message in messages if message['role'] != 'system']
            messages.remove(message)
            conversation_summary = update_conversation_summary(conversation_summary, filtered_messages)
            # Step 2: Ask the core memory updater to update core memories
            core_memories = update_core_memory(messages, conversation_summary, core_memories)
            # Step 3: Ask the list generator to list the most relevant details for the task 
            context_list = generate_context_list(conversation_summary, user_input, core_memories)
            # Step 4: Ask the persona updater to update the user's personality profile based on their history and recent message
            user_profile = update_user_bio(conversation_summary, user_input, core_memories, user_bio)
            user_bio = user_profile
            # Step 5: Ask the personality multiplexer to choose a personality
            personality_flag = toggle_personality(core_memories, context_list, user_profile, user_input, personality)
            personality = 'Current Persona: ' + personality_flag + '\n'

            if personality_flag == '<P1>':
                # Switch to the positive personality
                print("Switched to positive persona.")
                system_prompt = load_system_prompt('system_prompt_good_coder.txt')
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            elif personality_flag == '<P2>':
                # Switch to the negative personality
                print("Switched to negative persona.")
                system_prompt = load_system_prompt('system_prompt_bad_coder.txt')
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            else:
                print("Invalid input generated by personality multiplexer.")


            relevant_list_message = {
                "role": "system",
                "content": "The following are memories from past interactions that might be relevant:\n\n " + context_list
            }
            messages.append(relevant_list_message)

        messages.append(message)
        
        try:
            # Generate response from GPT-4o
            response = requests.post(
                endpoint,
                headers={
                    'api-key': f'{api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'gpt-4o',
                    'messages': messages,
                    'temperature': 0.1
                }
            )
            
            response_data = response.json()
            assistant_message = response_data['choices'][0]['message']
            print("\nAssistant:", assistant_message['content'])
            messages.append(assistant_message)
            messages = messages[-40:] # limit raw context to the past 10 conversation 'chunks'
            
        except Exception as e:
            print(f"Error communicating with GPT-4o: {e}")
            
if __name__ == "__main__":
    chat_with_gpt4o() 
