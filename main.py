import random
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Splash Screen")
        self.root.geometry("800x600")

        self.bg_label = ttk.Label(root, background="#FF5733")
        self.bg_label.place(relwidth=1, relheight=1)

        self.logo_label = ttk.Label(root, text="Jumbled Words App", font=("Helvetica", 36), foreground="white", background="#FF5733")
        self.logo_label.pack(pady=200)

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate")
        self.progress_bar.pack(pady=10)

        self.loading_label = ttk.Label(root, text="Loading...", font=("Helvetica", 16), foreground="white", background="#FF5733")
        self.loading_label.pack()

        self.root.after(100, self.start_loading)

    def start_loading(self):
        for i in range(101):
            self.progress_bar["value"] = i
            self.root.update_idletasks()
            self.root.after(30)  # Adjust the delay time
        self.root.destroy()
        self.open_main_app()

    def open_main_app(self):
        main_window = tk.Tk()
        app = MainApp(main_window)  # Create an instance of your main application class
        main_window.mainloop()

# List of words for different difficulty levels
beginner_words = ["apple", "basic", "table", "chair", "drink"]
moderate_words = ["chocolate", "guitar", "kangaroo", "puzzle", "library"]
expert_words = ["elephant", "university", "butterfly", "experience", "television"]

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x800+100+100")
        self.root.title("Find a Word Game")

        # Apply a themed style
        style = ThemedStyle(root)
        style.set_theme("plastik")

        # Choose difficulty level
        level_label = ttk.Label(root, text="Choose a difficulty level:")
        level_label.pack()

        level_var = tk.StringVar()
        level_var.set("Beginner")
        level_option_menu = ttk.Combobox(root, textvariable=level_var, values=["Beginner", "Moderate", "Expert"])
        level_option_menu.pack()

        # Start the game
        start_button = ttk.Button(root, text="Start Game", command=lambda: self.start_game(level_var.get()))
        start_button.config(style="Large.TButton")
        start_button.pack()

        # Game variables
        self.guessed_letters = set()
        self.attempts_left = 5
        self.word_to_guess = ""
        self.guessed_word = ""

        # Create game window
        self.word_label = ttk.Label(root, text="", font=("Helvetica", 24))
        self.attempts_left_label = ttk.Label(root, text="", font=("Helvetica", 14))
        self.guess_entry = ttk.Entry(root, width=2, font=("Helvetica", 14))
        self.guess_button = ttk.Button(root, text="Guess", command=lambda: self.check_guess())

    def choose_word(self, level):
        if level == "Beginner":
            return random.choice(beginner_words)
        elif level == "Moderate":
            return random.choice(moderate_words)
        elif level == "Expert":
            return random.choice(expert_words)
        else:
            return None

    def is_valid_input(self, input_str):
        return input_str.isalpha() and len(input_str) == 1

    def check_guess(self):
        guess = self.guess_entry.get().lower()
        if not self.is_valid_input(guess):
            messagebox.showerror("Invalid Input", "Please enter a single letter.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Duplicate Guess", "You've already guessed that letter.")
            return

        self.guessed_letters.add(guess)
        if guess in self.word_to_guess:
            for i in range(len(self.word_to_guess)):
                if self.word_to_guess[i] == guess and self.guessed_word[i] == '_':
                    self.guessed_word = self.guessed_word[:i] + guess + self.guessed_word[i+1:]

            self.word_label.config(text=self.guessed_word)
        else:
            self.attempts_left -= 1

        self.attempts_left_label.config(text=f"Attempts left: {self.attempts_left}")

        if self.guessed_word == self.word_to_guess:
            messagebox.showinfo("Congratulations", "You've guessed the word correctly.")
            self.root.quit()
        elif self.attempts_left == 0:
            messagebox.showinfo("Out of Attempts", f"Sorry, you're out of attempts. The word was: {self.word_to_guess}")
            self.root.quit()

    def start_game(self, level):
        self.guessed_letters.clear()
        self.word_to_guess = self.choose_word(level)
        self.guessed_word = "_" * len(self.word_to_guess)
        self.attempts_left = len(self.word_to_guess)
        if not self.word_to_guess:
            messagebox.showerror("Invalid Level", "Please choose a valid difficulty level.")
            return
        self.word_label.config(text=self.guessed_word)
        self.attempts_left_label.config(text=f"Attempts left: {self.attempts_left}")
        self.guess_entry.delete(0, tk.END)
        self.word_label.pack()
        self.attempts_left_label.pack()
        self.guess_entry.pack()
        self.guess_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = SplashScreen(root)
    root.mainloop()