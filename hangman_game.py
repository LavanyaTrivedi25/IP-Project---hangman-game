import pandas as pd
import random
import time
import pyttsx3
import matplotlib.pyplot as plt

def load_periodic_table():
    df = pd.read_csv("C:\\Users\\HP\\OneDrive\\Desktop\\School Work\\Projects\\IP Project 12th\\IP-Project-12th-Hangman-game-main\\periodic_table.csv")
    return df

def select_random_element(df, category=None, difficulty='medium'):
    if category:
        df = df[df['AtomicNumber'] == category]
    if difficulty == 'easy':
        df = df[df['Name'].str.len() <= 5]
    elif difficulty == 'medium':
        df = df[(df['Name'].str.len() > 5) & (df['Name'].str.len() <= 8)]
    elif difficulty == 'hard':
        df = df[df['Name'].str.len() > 8]
    return df.sample()

def display_word(word):
    return '_ ' * len(word)

def update_displayed_word(word, guessed_letter, displayed_word):
    new_displayed_word = ''
    for i in range(len(word)):
        if word[i].lower() == guessed_letter.lower():
            new_displayed_word += guessed_letter + ' '
        else:
            new_displayed_word += displayed_word[i*2] + ' '
    return new_displayed_word

def get_hint(element_row):
    atomic_number = element_row['AtomicNumber'].values[0]
    print(f"The atomic number of the element is {atomic_number}.")

def draw_hangman(attempts, excited=False):
    stages = [
        # final state: excited hangman
        r"""
           |
           |       \ 0 / 
           |        \|/
           |         | 
           |         |
           |--------/-\----------
        """,
        # final state: head, torso, both arms, and both legs
        r"""
           --------
           |      |
           |      O
           |     \|/
           |      |
           |     / \
          ---
        """,
        # head, torso, both arms, and one leg
        r"""
           --------
           |      |
           |      O
           |     \|/
           |      |
           |     / 
          ---
        """,
        # head, torso, and both arms
        r"""
           --------
           |      |
           |      O
           |     \|/
           |      |
           |      
          ---
        """,
        # head, torso, and one arm
        r"""
           --------
           |      |
           |      O
           |     \|
           |      |
           |     
          ---
        """,
        # head and torso
        r"""
           --------
           |      |
           |      O
           |      |
           |      |
           |     
          ---
        """,
        # head
        r"""
           --------
           |      |
           |      O
           |    
           |      
           |     
          ---
        """,
        # initial empty state
        r"""
           --------
           |      |
           |      
           |    
           |      
           |     
          ---
        """
    ]
    if excited:
        print(stages[0])
    else:
        print(stages[attempts])


def hangman(player):
    while True:
        print("Welcome to Hangman - Periodic Table Edition!")
        print("Try to guess the name of the chemical element.")
        print("You have 6 attempts to guess the word correctly.\n")

        df = load_periodic_table()
        difficulty = input("Select difficulty level (easy/medium/hard): ").lower()
        element_row = select_random_element(df, difficulty=difficulty)
        element_name = element_row['Name'].values[0]
        symbol = element_row['Symbol'].values[0]
        atomic_mass = element_row['AtomicMass'].values[0]
        nature = element_row['Nature'].values[0]
        category = element_row['AtomicNumber'].values[0]
        word = element_name.lower()

        displayed_word = display_word(word)

        attempts = 6
        guessed_letters = []
        start_time = time.time()
        total_time = 30  # Total time allowed for the game in seconds


        while attempts > 0 and '_ ' in displayed_word:
            elapsed_time = time.time() - start_time
            remaining_time = total_time - elapsed_time
            if remaining_time <= 0:
                print("\nTime's up!")
                break  # End the game if time is up
        
            print("\nWord to guess:", displayed_word)
            print("Attempts left:", attempts)
            print("Time left: {:.2f} seconds".format(remaining_time))
            draw_hangman(attempts)
            
            guess = input("Guess a letter: ").strip().lower()

            if guess == "hint":
                get_hint(element_row)
                continue

            if len(guess) != 1 or not guess.isalpha():
                print("Please enter a single letter.")
                continue
            elif guess in guessed_letters:
                print("You already guessed that letter.")
                continue

            guessed_letters.append(guess)

            if guess in word:
                displayed_word = update_displayed_word(word, guess, displayed_word)
                print("Correct!")
                if '_ ' not in displayed_word:
                    print("Excited Hangman!")
                    draw_hangman(attempts, excited=True)  
            else:
                print("Incorrect!")
                attempts -= 1

            elapsed_time = time.time() - start_time
            if elapsed_time > 120:  
                print("\nTime's up!")
                break

        if '_ ' not in displayed_word:
            print("\nCongratulations! You guessed the word:", element_name)
            print("Symbol:", symbol)
            print("Atomic Number:", category)
            print("Atomic Mass:", atomic_mass)
            print("Nature:", nature)
        else:
            print("\nYou ran out of attempts or time. The word was:", element_name)
            print("Symbol:", symbol)
            print("Atomic Number:", category)
            print("Atomic Mass:", atomic_mass)
            print("Nature:", nature)

        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        print()
        if play_again != 'yes':
            print("Thank you for playing! Keep studying, keep playing!")
            break



def multiplayer(players):
    print("\nLet's begin the multiplayer game!\n")
    for i, player in enumerate(players):
        print(f"It's {player}'s turn.")
        hangman(player)
        if i < len(players) - 1:
            print("\nNext player's turn.")

def main():
    while True:
        print("Welcome to Hangman - Periodic Table Edition!")
        print('***********************************************')
        print("Select an option:")
        print("1. Single Player")
        print("2. Multiplayer")
        choice = input("Enter your choice: ")

        if choice == '1':
            player = input("Enter your name: ").capitalize()  # Capitalize the first letter of the name
            greet_player(player)
            hangman(player)
            break
        elif choice == '2':
            num_players = int(input("Enter the number of players: "))
            players = [input(f"Enter player {i+1}'s name: ").capitalize() for i in range(num_players)]  # Capitalize the first letter of each player's name
            for player in players:
                greet_player(player)
            multiplayer(players)
            break
        else:
            print("Invalid choice. Please enter either 1 or 2.")
def greet_player(player):
    print(f"Hello, {player}! Let's play Hangman game.\n")

if __name__ == "__main__":
    main()
