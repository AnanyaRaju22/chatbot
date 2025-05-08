from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")  # instance of Generative model
chat = model.start_chat(history=[])  # new chat object

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)  # chunks, waiting response
    return response

def is_domain_specific(question, domain_keywords):
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in domain_keywords)

def main():
    print("Welcome to the Hackathon Chatbot!")
    print("Type your question below (or type 'exit' to quit):")

    chat_history = []
    domain_keywords = ["hackathon", "coding competition", "programming contest", "code fest", "hack"]

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if is_domain_specific(user_input, domain_keywords):
            print("Fetching response...")
            response = get_gemini_response(user_input)
            response_text = "".join([chunk.text for chunk in response])
        else:
            response_text = "I can only answer questions related to hackathons."

        chat_history.append(("You", user_input))
        chat_history.append(("Bot", response_text))
        print(f"Bot: {response_text}")

    print("\nChat History:")
    for role, text in chat_history:
        print(f"{role}: {text}")

if __name__ == "__main__":  # directly run, not imported
    main()
