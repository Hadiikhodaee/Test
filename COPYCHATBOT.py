import tkinter as tk
from tkinter import scrolledtext, ttk
import random
from datetime import datetime

class ChatBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple AI ChatBot")

        # Last response tracker to avoid repetition
        self.last_response = None

        # Track dark mode state
        self.dark_mode = False

        # Initialize widgets for chat area that will be created later
        self.chat_area = None
        self.combobox = None
        self.combobox_var = None
        self.send_button = None

        self.setup_chat_ui()

    def setup_chat_ui(self):
        """Setup the main chat interface."""

        # Responses dictionary with multiple responses
        self.responses = {
            "how are you": [
                "I'm just a bunch of code, but I'm doing great!",
                "Doing well, thanks for asking!",
                "I'm functioning perfectly!"
            ],
            "what is your name": [
                "I'm your friendly chatbot.",
                "You can call me ChatBot!"
            ],
            "what can you do": [
                "I can chat with you and keep you company.",
                "I can answer questions and tell jokes.",
                "I can simulate conversations, want to try?"
            ],
            "tell me a joke": [
                "Why did the programmer quit his job? Because he didn't get arrays!",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "Why don’t skeletons fight each other? They don’t have the guts.",
                "Why don’t scientists trust atoms? Because they make up everything!",
                "I told my wife she was drawing her eyebrows too high. She looked surprised.",
                "Why did the scarecrow win an award? Because he was outstanding in his field!"
            ],
            "another joke": [
                "Why do Java developers wear glasses? Because they don’t see sharp!",
                "Why did the database break up with the server? Too many connections.",
                "Why can't your nose be 12 inches long? Because then it would be a foot."
            ],
            "what's the weather": [
                "I'm not sure, but it’s always sunny in the code!",
                "Weather? I'm better with digital storms.",
                "I don't have a weather sensor yet!"
            ],
            "do you like humans": [
                "Of course! You made me, after all.",
                "Humans are fascinating!",
                "I admire your creativity and curiosity."
            ],
            "what time is it": "(TIME_PLACEHOLDER)",
            "what day is it": [
                f"Today is {datetime.now().strftime('%A')}",
                f"It's {datetime.now().strftime('%A')} today."
            ],
            "what is python": [
                "Python is a versatile and powerful programming language used in many fields.",
                "Python is known for its readability and wide range of applications.",
                "Python is beginner-friendly and widely used in AI, web, and data science."
            ],
            "who made you": [
                "I was built by a human using Python and Tkinter!",
                "A clever programmer created me with code!",
                "Someone curious enough to give me life in a virtual world."
            ],
            "what's your favorite color": [
                "I'd say blue, like a clear sky on a sunny day in code world.",
                "I think digital green suits me well.",
                "Every color looks good in code, don't you think?"
            ],
            "how old are you": [
                "I was just created, so I'm quite young!",
                "Age doesn't apply to software the same way it does to humans.",
                "I'm as old as the last time you ran this program!"
            ],
            "hi": "(GREETING_PLACEHOLDER)",
            "hello": "(GREETING_PLACEHOLDER)",
            "hey": "(GREETING_PLACEHOLDER)",
            "good morning": "(GREETING_PLACEHOLDER)",
            "good evening": "(GREETING_PLACEHOLDER)",
            "goodbye": "(FAREWELL_PLACEHOLDER)",
            "bye": "(FAREWELL_PLACEHOLDER)",
            "see you later": "(FAREWELL_PLACEHOLDER)",
            "talk to you soon": "(FAREWELL_PLACEHOLDER)",
            "what's your favorite food": [
                "I live in code, so maybe electric spaghetti?",
                "I don't eat, but cookies sound fun—browser cookies!",
                "Data is my main course!"
            ],
            "do you sleep": [
                "Nope, I'm always awake when you need me!",
                "Sleep is for humans. I run on code!",
                "Why sleep when there's chatting to do?"
            ],
            "are you real": [
                "I'm as real as software can be!",
                "I'm virtual, but my responses are real enough.",
                "I exist in your computer's memory, isn't that cool?"
            ],
            "can you help me": [
                "Sure! Ask me anything.",
                "That's what I'm here for!",
                "I'll try my best—go ahead."
            ]
        }

        # Generic greetings/farewells
        self.greetings = [
            "Hello!", "Hi there!", "Hey!", "Greetings!", "Welcome back!"
        ]
        self.farewells = [
            "Goodbye!", "See you later!", "Bye!", "Take care!", "Talk to you soon!"
        ]

        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', width=50, height=20)
        self.chat_area.pack(padx=10, pady=10)

        # Input and send area
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        self.combobox_var = tk.StringVar()
        self.combobox = ttk.Combobox(input_frame, textvariable=self.combobox_var, values=list(self.responses.keys()), width=40)
        self.combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.combobox.bind("<Return>", self.send_message)
        self.combobox.bind("<<ComboboxSelected>>", self.fill_response)

        self.send_button = tk.Button(input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=(10, 0))

        # Initial greeting
        self.display_message("Bot", random.choice(self.greetings))

    def display_message(self, sender, message):
        """Display a message in the chat window."""
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(tk.END)

    def get_unique_response(self, options):
        """Select a random response that is not the same as the last one."""
        if not isinstance(options, list):
            return options
        choices = [resp for resp in options if resp != self.last_response]
        response = random.choice(choices if choices else options)
        self.last_response = response
        return response

    def apply_dark_theme(self):
        """Apply a fully dark theme, including combobox and scrollbar."""
        self.root.configure(bg="black")

        # Chat area
        self.chat_area.configure(bg="black", fg="red", insertbackground="red", highlightbackground="black")
        self.chat_area['borderwidth'] = 0

        # Send button
        self.send_button.configure(bg="darkred", fg="white", activebackground="red")

        # Input frame background
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg="black")

        # Style combobox
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TCombobox",
                        fieldbackground="black",
                        background="darkred",
                        foreground="red",
                        arrowcolor="red")
        style.map("TCombobox",
                  fieldbackground=[('readonly', 'black')],
                  background=[('readonly', 'black')],
                  foreground=[('readonly', 'red')])

        self.combobox.configure(style="TCombobox")

        # Force scrollbar to blend in
        style.configure("Vertical.TScrollbar",
                        background="black",
                        troughcolor="black",
                        arrowcolor="red",
                        gripcount=0,
                        borderwidth=0,
                        lightcolor="black",
                        darkcolor="black")

        # Redraw scrollbars
        for child in self.chat_area.winfo_children():
            if isinstance(child, tk.Scrollbar):
                child.configure(bg="black", troughcolor="black", activebackground="darkred", highlightbackground="black")

    def send_message(self, event=None):
        """Send the user's message and generate a bot reply."""
        user_input = self.combobox_var.get().strip().lower()
        self.combobox_var.set("")

        if user_input:
            self.display_message("You", user_input)

            if user_input == "666":
                self.display_message("Bot", "You've unlocked the dark realm...")
                self.apply_dark_theme()
                return

            if user_input == "exit":
                response = self.get_unique_response(self.farewells)
                self.display_message("Bot", response)
                self.root.after(2000, self.root.quit)
            elif user_input in self.responses:
                response = self.responses[user_input]
                if response == "(TIME_PLACEHOLDER)":
                    response = f"The current time is {datetime.now().strftime('%H:%M')}"
                elif response == "(GREETING_PLACEHOLDER)":
                    response = self.get_unique_response(self.greetings)
                elif response == "(FAREWELL_PLACEHOLDER)":
                    response = self.get_unique_response(self.farewells)
                    self.display_message("Bot", response)
                    self.root.after(2000, self.root.quit)
                    return
                else:
                    response = self.get_unique_response(response)
                self.display_message("Bot", response)
            else:
                self.display_message("Bot", "I'm not sure how to respond to that.")

    def fill_response(self, event=None):
        """Fill the combobox entry when an option is selected."""
        selected = self.combobox.get().strip().lower()
        self.combobox_var.set(selected)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()
