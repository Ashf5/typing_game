import time
import sqlite3
from random import sample

#TODO Integrate the database


def main():
    """
    This function is the controller of the app. It displays a menu with a infinite loop offering some options and calls the appropriate functions.
    """
    while True:
        print("0: Quit\n1: Play Game\n2: My Average\n3: Reset")
        try:
            choice = int(input())
        except ValueError:
            print("Invalid Entry")
            continue

        if choice == 0:
            break
        elif choice == 1:
            print("How many words would you like to type? (Maximum 500)")
            while True:
                try:
                    num = int(input())
                except ValueError:
                    print("Invalid Entry")
                    continue
                if num < 1:
                    print("You must enter at least 1")
                    continue
                else:
                    break
            play_game(num)
        elif choice == 2:
            average()
        elif choice == 3:
            print("Are you sure you want to reset the scores? (y/n)")
            answer = input()
            if answer.startswith("y"):
                reset()
                print("Scores were reset")
            else:
                continue
        else:
            print("Invalid Choice")
            continue


def write_file(num):
    """
    This function takes in a number of words and generates a file with that number of random words
    """
    if num > 500:
        num = 500
    try:
        with open("large", "r") as f:
            data = f.read()
    except:
        print("Error writing file, please restart the program")
        return -1
        
    if len(data) < 1:
        print("Error occured")
        return -1
    li = data.split()
    words = sample(li, num)
    string = " ".join(words)

    with open("type.txt", "w") as f:
        f.write(string)
    return 0


def play_game(num):
    """
    This function accepts the typing input from the command line and grades the input.
    """
    code = write_file(num)
    with open("type.txt", "r") as f:
        data = f.read()
    if code != 0:
        return
    print("Open the type.txt file and then press Enter")
    input()
    print("Get Ready")
    time.sleep(3)
    print("Start")
    start_time = time.time()

    # Do the grading calculations
    test = input()
    end_time = time.time()
    total_time = end_time - start_time
    wpm = 60 / total_time * num
    print(f"You took {int(total_time)} seconds")
    print(f"you averaged {int(wpm)} words per minute")
    errors = grader(test)
    print(f"You made {errors} errors")
    accuracy = 100 - int(errors * 100 / len(test))
    print(f"You typed at %{accuracy} accuracy")
    if accuracy > 79:
        print("Good job!")
    else:
        print("Maybe next time take a little slower and work on your accuracy")

    update_database(wpm, accuracy)


def grader(text):
    """
    This function takes in the input text and grades it against the type.txt file. It then returns the number of errors made.
    Note: This function does not count white space.
    """
    input_text = text.split()
    with open("type.txt", "r") as f:
        data = f.read()

    test_text = data.split()

    errors = 0

    for i in range(len(test_text)):
        for h in range(len(test_text[i])):
            try:
                if input_text[i][h] != test_text[i][h]:
                    errors += 1
            except IndexError:
                errors += 1

    return errors


def update_database(wpm, accuracy):
    """
    This function takes in two numbers, the wpm and accuracy and adds it to the scores table in the data.db database.
    """
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY AUTOINCREMENT, wpm INTEGER NOT NULL, accuracy INTEGER NOT NULL);")

    if wpm == None or accuracy == None:
        return -1
    cur.execute("INSERT INTO scores (wpm, accuracy) VALUES (?, ?);", (wpm, accuracy))
    conn.commit()
    return 0
    

def average():
    """
    This function prints the average wpm and accuracy.
    """
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM scores;")
    num_entries = cur.fetchall()[0][0]

    cur.execute("SELECT wpm FROM scores;")
    data = cur.fetchall()
    li = [i[0] for i in data]
    avg_wpm = int(sum(li) / num_entries)
    print(f"Your average words per minute is {avg_wpm}")
    cur.execute("SELECT accuracy FROM scores")
    data = cur.fetchall()
    li = [i[0] for i in data]
    avg_accuracy = sum(li) / num_entries
    print(f"Your average accuracy is {avg_accuracy}")


def reset():
    """
    This function resets the database.
    """
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE scores")
    cur.execute("CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY AUTOINCREMENT, wpm INTEGER NOT NULL, accuracy INTEGER NOT NULL);")

if __name__ == "__main__":
    main()

