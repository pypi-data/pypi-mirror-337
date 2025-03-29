# app.py
import requests
import json
import os
from dotenv import load_dotenv
from .simplesearch import SimpleSearch
from .search import perform_search
from . import importdocs
# Removed check import and call

class ChatWrapper:
    def __init__(self):
        self.cloud_service_url = "http://localhost:8000"
        self.ollama_url = "http://localhost:11434/api/chat"
        self.api_key = None
        self.available_models = []
        self.current_model = None
        self.simple_search = None
        self.history = []
        self.initialize_env()  # Initialize .env file
        load_dotenv()  # Load environment variables

    def initialize_env(self):
        """Create .env file if it doesn't exist."""
        if not os.path.exists(".env"):
            with open(".env", "w") as f:
                f.write("# API Key for the application\n")
                f.write("API_KEY=\n")  # Empty key by default

    def get_available_models(self):
        """Fetch available models from Ollama."""
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.get("http://localhost:11434/api/tags", headers=headers)
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except Exception as e:
            print(f"Error getting models: {e}")
            return []

    def select_model(self):
        """Allow the user to select a model from the available ones."""
        self.available_models = self.get_available_models()
        if not self.available_models:
            print("No models available. Please install or configure models first.")
            return False

        print("\nAvailable models:")
        for i, model in enumerate(self.available_models, 1):
            print(f"{i}. {model}")

        while True:
            try:
                choice = int(input("\nSelect model (number): "))
                if 1 <= choice <= len(self.available_models):
                    self.current_model = self.available_models[choice - 1]
                    print(f"Selected model: {self.current_model}")
                    self.simple_search = SimpleSearch(
                        self.cloud_service_url,
                        self.ollama_url,
                        self.current_model,
                        self.api_key
                    )
                    return True
                print("Invalid selection. Try again.")
            except ValueError:
                print("Please enter a valid number.")

    def call_ollama(self, query):
        """Send a query to Ollama and stream the response."""
        self.history.append({"role": "user", "content": query})
        payload = {
            "model": self.current_model,
            "messages": self.history,
            "stream": True
        }
        headers = {"Content-Type": "application/json"}
        try:
            with requests.post(self.ollama_url, json=payload, headers=headers, stream=True) as response:
                response.raise_for_status()
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        content = chunk.get("message", {}).get("content", "")
                        print(content, end="", flush=True)
                        full_response += content
                print()  # Newline after streaming
                self.history.append({"role": "assistant", "content": full_response})
        except Exception as e:
            print(f"Error calling Ollama: {e}")

    def process_query(self, query):
        """Process the user query using the appropriate pipeline."""
        perform_search(query, self.current_model, self.api_key)

    def handle_api_key_change(self):
        """Allow the user to change the API key."""
        new_key = input("Enter new API key: ").strip()
        if not new_key:
            print("No key provided. Operation canceled.")
            return
        
        # Update .env file
        with open(".env", "w") as f:
            f.write(f"API_KEY={new_key}\n")
        
        # Update current instance
        self.api_key = new_key
        if self.current_model:
            self.simple_search = SimpleSearch(
                self.cloud_service_url,
                self.ollama_url,
                self.current_model,
                self.api_key
            )
        print("API key updated successfully.")

    def start_chat(self):
        """Start the chat session."""
        # Load API key from .env or prompt user
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            self.api_key = input("Enter your API key: ").strip()
            if not self.api_key:
                print("API key is required. Exiting...")
                return
            # Save to .env
            with open(".env", "w") as f:
                f.write(f"API_KEY={self.api_key}\n")

        if not self.select_model():
            return

        print("\nChat started. Type '//exit' to quit. Type '//api_key' to change API key.")
        while True:
            try:
                query = input("\n>>> ").strip()
                if query == "//exit":
                    print("Exiting...")
                    break
                if query == "//api_key":
                    self.handle_api_key_change()
                    continue
                if not query:
                    continue

                print("\nProcessing...")
                self.process_query(query)

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"\nError: {e}")

def main():
    wrapper = ChatWrapper()
    wrapper.start_chat()

if __name__ == "__main__":
    main()
