import random
from hangman_phrases import phrases

def show_section(str):
    print """
    ************
    %s
    ************
    """ % str

def greet_player():
    show_section("""
    WELCOME TO HANGMAN
    """)
    read_rules()

def read_rules():
    show_section("""
    GAME RULES

    To win:
    \tIdentify the secret phrase before you run out of guesses

    Each turn:
    \tGuess a single letter you think appears somewhere in the phrase...
    \t...or try to solve for the entire phrase

    Careful, though:
    \teach wrong attempt at solving for the entire phrase...
    \t...will cost you three guesses instead of just one
    """)

def create_puzzle_for(str):
    final_puzzle = list(str.upper())
    start_puzzle = []
    for item in range(len(str)):
        if str[item] is " ":
            start_puzzle.append(" ")
        else:
            start_puzzle.append("_")
    return [start_puzzle, final_puzzle]

def show_user_progress(puzzles, guesses_left):
    phrase_as_seen_by_user = " ".join(puzzles[0])
    show_section("""
    Guesses left: %d\n
    The puzzle so far:
    %s
    """ % (guesses_left, phrase_as_seen_by_user))
    if (puzzle_was_solved(puzzles)):
        print "Thanks for playing."
        exit(0)
    elif (guesses_left <= 0):
        print "Sorry, you have no more guesses."
        print "Game over."
        exit(0)
    else:
        play_again(puzzles, guesses_left)

def play_again(puzzles, guesses_left):
    player_guess = request_new_letter()
    found_in_puzzle = check_puzzle_for(player_guess.upper(), puzzles)

    while True:
        if (is_valid_answer(player_guess)):
            if (player_guess.upper() == "SOLVE"):
                player_guess = raw_input("> ")
                if (puzzle_was_solved([list(player_guess.upper()), puzzles[1]])):
                    print "Thanks for playing."
                    exit(0)
                else:
                    show_user_progress(
                        puzzles, notify_wrong_solution(
                            player_guess.upper(), guesses_left))
            elif (found_in_puzzle):
                show_user_progress(
                    update_player_puzzle(
                        puzzles, player_guess.upper()), guesses_left)
            else:
                show_user_progress(
                    puzzles, notify_bad_guess(
                        player_guess.upper(), guesses_left))

        else:
            play_again(puzzles, guesses_left)

def request_new_letter():
    print "Enter a letter or type %s to solve the puzzle" % "SOLVE"
    return raw_input("> ")

def is_valid_answer(str):
    if str.upper() == "SOLVE":
        print "Enter the solution to this puzzle:"
        return True
    elif len(str) > 1:
        print "Oops. You entered more than one character. Please only guess one letter.\n"
        return False
    elif len(str) == 0:
        print "Uh-oh. You did not guess anything. Please guess one letter.\n"
        return False
    elif len(str) == 1:
        return True
    else:
        return False

def check_puzzle_for(str, puzzles):
    times_found = 0
    for item in puzzles[1]:
        if item == str.upper():
            times_found += 1
        else:
            times_found += 0
    if times_found > 0:
        return True
    else:
        return False

def update_player_puzzle(puzzles, valid_correct_guess):
    number_found = 0
    for index, item in enumerate(puzzles[1]):
        if item == valid_correct_guess.upper():
            number_found += 1
            puzzles[0][index] = valid_correct_guess.upper()
    show_section("""
    Great guess! There are %d %s's
    """ % (number_found, valid_correct_guess.upper()))
    return puzzles

def notify_bad_guess(incorrect_guess, guesses_left):
    guesses_left -= 1
    show_section("""
    Sorry, there are no %s's.
    """ % (incorrect_guess))
    return guesses_left

def notify_wrong_solution(incorrect_guess, guesses_left):
    guesses_left -= 3
    show_section("""
    Sorry, that answer is incorrect.
    """)
    return guesses_left

def puzzle_was_solved(puzzles):
    if (puzzles[0] == puzzles[1]):
        show_section("""
        Congratulations. You solved the puzzle!
        """)
        return True
    else:
        return False

def start_new_game(selected_phrase, number_of_guesses):
    greet_player()
    puzzles = create_puzzle_for(selected_phrase)
    show_user_progress(puzzles, number_of_guesses)

selected_phrase = phrases[random.randint(0,len(phrases))]

start_new_game(selected_phrase, 10)
