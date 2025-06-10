# Task 4: Closure Practice
def make_hangman(secret_word):
    guesses = []
    def hangman_closure(letter):
        guesses.append(letter)
        display = ""
        all_guessed = True
        for char in secret_word:
            if char.lower() in guesses:
                display += char
            else:
                display += "_"
                all_guessed = False
        print(display)
        return all_guessed
    return hangman_closure

if __name__ == "__main__":
    secret = input("Enter the secret word: ").lower()
    game = make_hangman(secret)
    while True:
        guess = input("Guess a letter: ").lower()
        if len(guess) != 1:
            print("Please enter a single letter.")
            continue
        if game(guess):
            print("Congratulations, you guessed the word!")
            break