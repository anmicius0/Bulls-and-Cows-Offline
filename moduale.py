import random
import sqlite3
import datetime

conn = sqlite3.connect('score.db')

def check_input(guess):
    """
    Args
        guess: user's input
    Return
        result: a boolen value
    """
    result = True

    # if the input is not 4-dig
    if len(guess) != 4:
        result = False

    # if input is not numerical
    try:
        temp = int(guess)
    except ValueError:
        result = False

    return result

def check_answer(guess, answer):
    """
        Args:
            guess: the number player guess (str)
            answer: the answer (str)
        Return:
            a: a
            b: b
    """
    a = 0
    b = 0
    list_answer = []

    # turn answer into type "list"
    for x in answer:
        list_answer.append(x)
    
    # check amount of "b"
    for i in range(4):
        if guess[i] == answer[i]:
            b += 1
    # check the amount of "a"
    for i in guess:
        if i in list_answer:
            a += 1
            list_answer.remove(i)

    return a,b

def game():
    """
    Main part of game
    """
    answer = str(random.randint(1000, 9999))
    guess = str(input('Guess a number: '))
    counter = 0

    print(answer)

    # user will  get out the loop only when they have the right answer
    while guess != answer:
        
        # check user's input
        while not check_input(guess):
            print("Invalid input (4-dig number)")
            guess = str(input('Try another number: '))

        # get the numbet of a, b
        counter += 1
        a, b = check_answer(guess, answer)
        print("{a}A{b}B".format(a=a, b=b))
        guess = str(input   ('Try another number: '))
    
    print("Congragulation!")

    # record game score
    try:
        record(counter)
    except ValueError:
        pass

    again()

def again():
    """
    Do after game choices (ex: play again)
    """
    again = input("Do yout want to play again(y/n): ")

    if again in ['y', 'yes', 'Y', "Yes"]:
        game()
    else:
        print_scores()

def record(score):
    """
    Check the score, if it's top five highest
    than
    Write score, name, timenow into db

    Args:
        score: the score
    """
    # get the connection to db
    c = conn.cursor()
    
    scores = []
    for i in c.execute("SELECT score FROM score ORDER BY score LIMIT 5"):
        scores.append(i[0])

    #  if it's top 5 than add it into db
    if (len(scores) < 5) or (score < scores[4]):
        name = str(input("Please enter your name: "))
        query = "INSERT INTO score (score, name, time) VALUES ({}, '{}', datetime('now', 'localtime'))".format(score, name)
        c.execute(query)
        conn.commit()


def print_scores():
    c = conn.cursor()

    for i in c.execute("SELECT score, name, time FROM score ORDER BY score LIMIT 5"):
        print(i)

    conn.close()
    
if __name__=="__main__":
    game()  
