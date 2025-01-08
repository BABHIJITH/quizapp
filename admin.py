import tkinter as tk
from tkinter import messagebox
from database import fetch_categories, add_question_to_db

def admin_page(root):
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()

    # Set up the admin page
    admin_label = tk.Label(root, text="Admin Page", font=("Arial", 24))
    admin_label.pack(pady=20)

    # Category dropdown for adding questions
    categories = fetch_categories()
    unique_categories = list({category[0]: category for category in categories}.values())  # Ensure unique category names
    category_names = [category[1] for category in unique_categories]  
    selected_category = tk.StringVar(root)
    selected_category.set(category_names[0])  # Default selection
    
    category_menu = tk.OptionMenu(root, selected_category, *category_names)
    category_menu.pack(pady=10)

    # Question input field
    question_label = tk.Label(root, text="Enter Question:")
    question_label.pack(pady=5)
    question_entry = tk.Entry(root, width=50)
    question_entry.pack(pady=5)

    # Answer options input fields
    options_label = tk.Label(root, text="Enter Options (separate with commas):")
    options_label.pack(pady=5)
    options_entry = tk.Entry(root, width=50)
    options_entry.pack(pady=5)

    # Correct answer input field
    correct_option_label = tk.Label(root, text="Enter Correct Answer Index (0-3):")
    correct_option_label.pack(pady=5)
    correct_option_entry = tk.Entry(root, width=50)
    correct_option_entry.pack(pady=5)

    # Button to submit the question
    def submit_question():
        question = question_entry.get()
        options = options_entry.get().split(',')
        correct_option = int(correct_option_entry.get())
        
        # Add the question to the database
        category_id = category_names.index(selected_category.get()) + 1  # Assuming categories start at ID 1
        if add_question_to_db(question, options, correct_option, category_id):
            messagebox.showinfo("Success", "Question added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add question.")
    
    submit_button = tk.Button(root, text="Add Question", command=submit_question)
    submit_button.pack(pady=20)

    # Back to home button
    back_button = tk.Button(root, text="Back to Home", command=lambda: root.destroy())
    back_button.pack(pady=10)

    root.mainloop()
