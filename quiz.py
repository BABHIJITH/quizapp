import tkinter as tk
from tkinter import messagebox
from database import fetch_questions, update_score

def start_quiz_ui(root, category_id):
    root.destroy()
    root = tk.Tk()
    root.title("Quiz")

    questions = fetch_questions(category_id)
    score = [0]
    current_question = [0]

    def display_question():
        if current_question[0] < len(questions):
            question, options, correct_option = questions[current_question[0]][1], eval(questions[current_question[0]][2]), questions[current_question[0]][3]

            question_label.config(text=question)
            for idx, option in enumerate(options):
                option_buttons[idx].config(text=option, command=lambda i=idx: check_answer(i, correct_option))
        else:
            update_score(current_user["id"], score[0], category_id)
            messagebox.showinfo("Quiz Finished", f"Your score: {score[0]}")
            show_back_to_home_button()  # Show back to home button

    def check_answer(selected, correct):
        if selected == correct:
            score[0] += 1
        current_question[0] += 1
        display_question()

    def show_back_to_home_button():
        # Add back to home button after finishing the quiz
        back_button = tk.Button(root, text="Back to Home", command=lambda: root.destroy())
        back_button.pack(pady=20)

    question_label = tk.Label(root, text="")
    question_label.pack()

    option_buttons = [tk.Button(root) for _ in range(4)]
    for btn in option_buttons:
        btn.pack()

    display_question()
    root.mainloop()
