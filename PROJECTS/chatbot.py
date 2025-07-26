import random
import re

class SimpleChatBot:
    def __init__(self):
        self.responses = {
            r"(hi|hello|hey|hola)": ["Hello!", "Hi there!", "Hey!"],
            r"how are you": ["I'm just a program, but I'm functioning well!", "All systems go!"],
            r"your name": ["I'm ChatBot 1.0", "You can call me CB!"],
            r"bye|goodbye": ["Goodbye!", "See you later!", "Bye! Have a great day!"],
            r"weather": ["I don't have weather access right now", "You might want to check a weather app!"],
            r"thank(s| you)": ["You're welcome!", "My pleasure!", "Anytime!"],
            r"": ["I'm not sure I understand", "Could you rephrase that?", "Interesting tell me more"]
        }
    
    def respond(self, message):
        message = message.lower().strip()
        for pattern, responses in self.responses.items():
            if re.search(pattern, message):
                return random.choice(responses)
        return random.choice(self.responses[""])

if __name__ == "__main__":
    bot = SimpleChatBot()
    print("ChatBot: Hello! Type something to start chatting (type 'quit' to exit)")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("ChatBot: Goodbye! Thanks for chatting!")
            break
        response = bot.respond(user_input)
        print(f"ChatBot: {response}")