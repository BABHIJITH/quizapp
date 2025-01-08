import tkinter as tk
from tkinter import messagebox
from database import login_user, register_user, fetch_categories, fetch_questions, update_score
import json
from tkinter import Scrollbar, Canvas

# Function for login page
def login_page(root):
    def login_action():
        username = username_entry.get()
        password = password_entry.get()

        # Perform login
        user = login_user(username, password)
        if user:
            user_home_page(root, user[0])  # Pass root and user_id
        else:
            messagebox.showerror("Error", "Invalid credentials")

    # Create login page UI
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Login").pack(pady=10)
    tk.Label(root, text="Username").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)
    
    tk.Label(root, text="Password").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)
    
    login_button = tk.Button(root, text="Login", command=login_action)
    login_button.pack(pady=20)
    
    register_button = tk.Button(root, text="Register", command=lambda: register_page(root))
    register_button.pack(pady=5)

# Function for user home page
def user_home_page(root, user_id):
    def on_category_click(category_id):
        quiz_page(root, user_id, category_id)

    # Create user home page UI
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Welcome to Quiz App").pack(pady=10)

    # Fetch and display unique categories
    categories = fetch_categories()
    displayed_categories = set()  # Track displayed categories
    for category in categories:
        category_id, category_name = category
        if category_name not in displayed_categories:
            tk.Button(root, text=category_name, command=lambda cid=category_id: on_category_click(cid)).pack(pady=5)
            displayed_categories.add(category_name)  # Add to the set of displayed categories

def quiz_page(root, user_id, category_id):
    def submit_quiz():
        score = calculate_score()  # Calculate the score based on correct answers
        update_score(user_id, score, category_id)

        # Display score after quiz submission
        score_label = tk.Label(scrollable_frame, text=f"Your score: {score}")
        score_label.pack(pady=10)

        # Show back to home button
        back_button = tk.Button(scrollable_frame, text="Back to Home", command=lambda: user_home_page(root, user_id))
        back_button.pack(pady=20)

    def calculate_score():
        # Logic to calculate the score
        score = 0
        for i, question in enumerate(questions):
            selected_option = int(option_vars[i].get())  # Get the selected option for this question as integer
            correct_option = question[3]  # Assuming correct_option is stored in the 4th column of the database
            if selected_option == correct_option:  # Compare with the correct option
                score += 4  # Add 4 points for correct answer
        return score

    # Fetch the questions for the selected category
    questions = fetch_questions(category_id)

    # Create a scrollable frame within a canvas
    canvas = Canvas(root)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))  # Update scrollable area
    )

    # Create quiz UI
    tk.Label(scrollable_frame, text="Quiz Time!").pack(pady=10)

    option_vars = []
    for question in questions:
        question_label = tk.Label(scrollable_frame, text=question[1])  # Assuming the question is at index 1
        question_label.pack()

        options = json.loads(question[2])  # Assuming options are stored as a JSON string
        option_var = tk.IntVar(value=-1)  # Use IntVar to store option indices
        option_vars.append(option_var)

        for i, option in enumerate(options):
            option_button = tk.Radiobutton(scrollable_frame, text=option, variable=option_var, value=i)
            option_button.pack()

    submit_button = tk.Button(scrollable_frame, text="Submit Quiz", command=submit_quiz)
    submit_button.pack(pady=20)

    # Ensure the back button is displayed after the quiz is finished
    root.update_idletasks()  # Force update of the UI
