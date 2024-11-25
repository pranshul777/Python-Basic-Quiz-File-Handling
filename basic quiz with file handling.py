import random

# File paths
USERS_FILE = "users.txt"
QUESTIONS_FILE = "questions.txt"

# Initialize files
def setup_files():
    open(USERS_FILE, "a").close()
    open(QUESTIONS_FILE, "a").close()

# User functions
def load_users():
    users = {}
    with open(USERS_FILE, "r") as f:
        for line in f:
            username, password, score = line.strip().split(":")
            users[username] = {"password": password, "score": int(score)}
    return users

def save_user(username, password, score=0):
    with open(USERS_FILE, "a") as f:
        f.write(f"{username}:{password}:{score}\n")

def update_score(username, score):
    users = load_users()
    users[username]["score"] += score
    with open(USERS_FILE, "w") as f:
        for user, data in users.items():
            f.write(f"{user}:{data['password']}:{data['score']}\n")

# Question functions
def load_questions():
    questions = []
    with open(QUESTIONS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            questions.append({
                "question": parts[0],
                "options": parts[1:5],
                "answer": int(parts[5])
            })
    return questions


# Authentication
def register_user():
    username = input("Enter a username: ").strip()
    users = load_users()
    if username in users:
        print("Username already exists. Please try logging in.")
        return None
    password = input("Enter a password: ").strip()
    save_user(username, password)
    print("Registration successful!")
    return username

def login_user():
    username = input("Enter your username: ").strip()
    users = load_users()
    if username not in users:
        print("User not found. Please register.")
        return None
    password = input("Enter your password: ").strip()
    if users[username]["password"] == password:
        print("Login successful!")
        return username
    else:
        print("Incorrect password.")
        return None

# Quiz game
def play_game(username):
    questions = load_questions()
    random_questions = random.sample(questions, 10)
    score = 0
    for i, q in enumerate(random_questions, start=1):
        print(f"\nQuestion {i}: {q['question']}")
        for idx, option in enumerate(q["options"]):
            print(f"{idx}. {option}")
        try:
            answer = int(input("Enter your choice (0-3): ").strip())
            if answer == q["answer"]:
                print("Correct!")
                score += 1
            else:
                print("Wrong!")
        except ValueError:
            print("Invalid input. Moving to next question.")
    print(f"\nYou scored {score} out of 10!")
    update_score(username, score)
    
# Main menu
def main():
    setup_files()
    current_user = None
    while True:
        print("\n--- Quiz App ---")
        if current_user:
            print(f"Logged in as: {current_user}")
            print("1. Play Quiz")
            print("2. Logout")
        else:
            print("1. Login")
            print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            if current_user:
                play_game(current_user)
            else:
                current_user = login_user()
        elif choice == "2":
            if current_user:
                current_user = None
                print("Logged out successfully.")
            else:
                current_user = register_user()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# Run the application
if __name__ == "__main__":
    main()
