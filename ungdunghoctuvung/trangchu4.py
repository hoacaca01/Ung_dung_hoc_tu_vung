import tkinter as tk
from tkinter import messagebox, Menu
import mysql.connector

# Create a MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="vocab_app"
)
cursor = db.cursor()

# Create the vocabulary table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS vocabulary (
        id INT AUTO_INCREMENT PRIMARY KEY,
        word VARCHAR(255) NOT NULL,
        meaning TEXT
    )
""")
db.commit()

# Create tkinter app
app = tk.Tk()
app.title("Vocabulary Learning App")
app.geometry("500x500")


# Function to add a word to the database
def add_word():
    word = entry_word.get()
    meaning = entry_meaning.get("1.0", tk.END)

    # Check if the word already exists in the database
    cursor.execute("SELECT * FROM vocabulary WHERE word=%s", (word,))
    existing_word = cursor.fetchone()

    if existing_word:
        messagebox.showinfo("Thông báo", "Từ vựng đã tồn tại.")
    else:
        cursor.execute("INSERT INTO vocabulary (word, meaning) VALUES (%s, %s)", (word, meaning))
        db.commit()
        messagebox.showinfo("Thông báo", "Thêm từ vựng thành công.")

    entry_word.delete(0, tk.END)
    entry_meaning.delete("1.0", tk.END)


# Function to switch to the "Add Vocabulary" page
def open_add_vocabulary():
    add_window = tk.Toplevel(app)
    add_window.title("Thêm từ vựng")

    label_word = tk.Label(add_window, text="Word:")
    global entry_word
    entry_word = tk.Entry(add_window)

    label_meaning = tk.Label(add_window, text="Meaning:")
    global entry_meaning
    entry_meaning = tk.Text(add_window, height=5, width=30)

    add_button = tk.Button(add_window, text="Thêm từ vựng", command=add_word)

    label_word.pack()
    entry_word.pack()
    label_meaning.pack()
    entry_meaning.pack()
    add_button.pack()


# Function to display vocabulary on the main page
def display_vocabulary():
    main_frame = tk.Frame(app)
    main_frame.pack()

    menu_bar = Menu(app)
    app.config(menu=menu_bar)

    vocabulary_menu = Menu(menu_bar)
    menu_bar.add_cascade(label="Từ vựng", menu=vocabulary_menu)
    vocabulary_menu.add_command(label="Thêm từ vựng", command=open_add_vocabulary)

    vocabulary1_menu = Menu(menu_bar)
    menu_bar.add_cascade(label="Vui", menu=vocabulary1_menu)
    vocabulary1_menu.add_command(label="vui1", command="trỏ tới hàm")

    cursor.execute("SELECT * FROM vocabulary")
    words = cursor.fetchall()

    vocab_display = tk.Text(main_frame, height=len(words), width=50)
    vocab_display.pack()

    for i, word in enumerate(words, start=1):
        vocab_display.insert(tk.END, f"{i}. Từ vựng: {word[1]}, Nghĩa: {word[2]}\n")


display_vocabulary()

app.mainloop()
