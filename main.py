from tkinter import Tk
from user import login_page

# Initialize the main Tkinter window
def main():
    root = Tk()
    root.geometry("400x400")
    root.title("Quiz App")
    
    # Start with the login page
    login_page(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
