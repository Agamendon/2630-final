#!/usr/bin/env python3
"""
Simple Command Line Chatbot
A basic chatbot that can be compiled into an executable file.
"""

import sys
import requests
import json
import urllib3

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Backend server URL
SERVER_URL = "https://localhost:4000"


def get_response(user_input):
    """
    Get response from the backend server via HTTPS request.
    """
    if not user_input.strip():
        return "Please say something!"
    
    try:
        # Make POST request to the backend server
        response = requests.post(
            f"{SERVER_URL}/chat",
            json={"message": user_input},
            verify=False,  # Disable SSL verification for self-signed certificates
            timeout=5
        )
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            # Assume the response has a 'response' or 'message' field
            return data.get('response', data.get('message', 'No response from server'))
        else:
            return f"Error: Server returned status code {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the server. Make sure the backend is running on localhost:4000"
    except requests.exceptions.Timeout:
        return "Error: Request timed out. The server may be slow to respond."
    except requests.exceptions.RequestException as e:
        return f"Error: Failed to communicate with server: {str(e)}"
    except json.JSONDecodeError:
        return "Error: Invalid response format from server"
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"


def main():
    """
    Main function to run the chatbot.
    """
    print("=" * 50)
    print("Welcome to the Simple Chatbot!")
    print("Type 'quit', 'exit', or 'bye' to exit.")
    print("=" * 50)
    print()
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nChatbot: Goodbye! Thanks for chatting!")
                break
            
            # Get and print response
            response = get_response(user_input)
            print(f"Chatbot: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nChatbot: Goodbye! Thanks for chatting!")
            break
        except EOFError:
            print("\n\nChatbot: Goodbye! Thanks for chatting!")
            break


if __name__ == "__main__":
    main()

