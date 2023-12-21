import tkinter as tk
from tkinter import messagebox, Menu, StringVar, ttk
import mysql.connector

# Create a MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hoctuvung"
)
cursor = db.cursor()

# Create the vocabulary table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS vocabulary (
        id INT AUTO_INCREMENT PRIMARY KEY,
        word VARCHAR(255) NOT NULL,
        meaning TEXT,
        word_type VARCHAR(50)
    )
""")
db.commit()

# Create tkinter app
app = tk.Tk()
app.title("Ứng dụng học từ vựng")
app.geometry("600x400")
word_type_var = StringVar()
# Function to add a word to the database
def add_word():
    word = entry_word.get()
    meaning = entry_meaning.get("1.0", tk.END)
    word_type = word_type_var.get()

    # Check if the word already exists in the database
    cursor.execute("SELECT * FROM vocabulary WHERE word=%s", (word,))
    existing_word = cursor.fetchone()

    if existing_word:
        messagebox.showinfo("Thông báo", "Từ vựng đã tồn tại.")
    else:
        cursor.execute("INSERT INTO vocabulary (word, meaning, word_type) VALUES (%s, %s, %s)",
                       (word, meaning, word_type))
        db.commit()
        messagebox.showinfo("Thông báo", "Thêm từ vựng thành công.")
        # After adding a word, refresh the display on the home page
        display_vocabulary()

    entry_word.delete(0, tk.END)
    entry_meaning.delete("1.0", tk.END)
    word_type_var.set("")  # Set word type back to default

# Function to display vocabulary in a table on the home page
def display_vocabulary():
    if "vocabulary_tree" in globals():
        vocabulary_tree.delete(*vocabulary_tree.get_children())

    cursor.execute("SELECT * FROM vocabulary")
    words = cursor.fetchall()

    for word in words:
        vocabulary_tree.insert("", "end", values=(word[1], word[2], word[3]))

# Create a frame for the vocabulary display
display_frame = ttk.Frame(app)
display_frame.pack(fill="both", expand=True)

# Create a Treeview widget for displaying vocabulary
vocabulary_tree = ttk.Treeview(display_frame, columns=("Word", "Meaning", "Word Type"), show="headings")
vocabulary_tree.heading("Word", text="Từ vựng")
vocabulary_tree.heading("Meaning", text="Nghĩa")
vocabulary_tree.heading("Word Type", text="Loại từ vựng")
vocabulary_tree.pack(fill="both", expand=True)

# Function to switch to the "Add Vocabulary" page
def open_add_vocabulary():
    add_window = tk.Toplevel(app)
    add_window.title("Thêm từ vựng")

    # Create a frame to organize widgets
    add_frame = tk.Frame(add_window, padx=20, pady=20)
    add_frame.pack()

    label_word = tk.Label(add_frame, text="Từ vựng:")
    label_word.grid(row=0, column=0, sticky="w")
    global entry_word
    entry_word = tk.Entry(add_frame)
    entry_word.grid(row=0, column=1, padx=10, pady=5)

    label_meaning = tk.Label(add_frame, text="Nghĩa:")
    label_meaning.grid(row=1, column=0, sticky="w")
    global entry_meaning
    entry_meaning = tk.Text(add_frame, height=5, width=30)
    entry_meaning.grid(row=1, column=1, padx=10, pady=5)

    label_word_type = tk.Label(add_frame, text="Loại từ vựng:")
    label_word_type.grid(row=2, column=0, sticky="w")

    # Use Radiobuttons to select word type
    word_type_var.set("")  # Default to no selection
    radio_verb = tk.Radiobutton(add_frame, text="Động từ", variable=word_type_var, value="Động từ")
    radio_noun = tk.Radiobutton(add_frame, text="Danh từ", variable=word_type_var, value="Danh từ")
    radio_adj = tk.Radiobutton(add_frame, text="Tính từ", variable=word_type_var, value="Tính từ")

    radio_verb.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    radio_noun.grid(row=2, column=2, padx=10, pady=5, sticky="e")
    radio_adj.grid(row=2, column=1, padx=10, pady=5, sticky="e")

    add_button = tk.Button(add_frame, text="Thêm từ vựng", command=add_word)
    add_button.grid(row=3, columnspan=2, pady=10)

    # Set up a scrollbar for the Text widget if needed
    scrollbar = tk.Scrollbar(add_frame, command=entry_meaning.yview)
    scrollbar.grid(row=1, column=2, sticky="nse")
    entry_meaning.config(yscrollcommand=scrollbar.set)

# Create a menu
menu_bar = Menu(app)
app.config(menu=menu_bar)

vocabulary_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Từ vựng", menu=vocabulary_menu)
vocabulary_menu.add_command(label="Thêm từ vựng", command=open_add_vocabulary)

# Initial display of vocabulary
display_vocabulary()

app.mainloop()
