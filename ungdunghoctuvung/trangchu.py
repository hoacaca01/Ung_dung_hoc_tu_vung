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
app.title("Vocabulary Learning App")
app.geometry("500x500")

# Function to add a word to the database
def add_word():
    word = entry_word.get()
    meaning = entry_meaning.get("1.0", tk.END)
    word_type = word_type_combobox.get()
    # word_type = word_type_var.get()

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
        # Sau khi thêm từ vựng, cập nhật lại hiển thị tại trang chủ
        display_vocabulary()

    entry_word.delete(0, tk.END)
    entry_meaning.delete("1.0", tk.END)
    # word_type_var.set("")  # Đặt loại từ vựng về mặc định
    word_type_combobox.set("Chọn loại")

# Function to switch to the "Add Vocabulary" page
# def open_add_vocabulary():
#     add_window = tk.Toplevel(app)
#     add_window.title("Thêm từ vựng")
#
#     label_word = tk.Label(add_window, text="Word:")
#     global entry_word
#     entry_word = tk.Entry(add_window)
#
#     label_meaning = tk.Label(add_window, text="Meaning:")
#     global entry_meaning
#     entry_meaning = tk.Text(add_window, height=5, width=30)
#
#     label_word_type = tk.Label(add_window, text="Loại từ vựng:")
#
#     # Sử dụng Radiobutton để chọn loại từ vựng
#     word_type_var.set("")  # Mặc định không chọn loại
#     radio_verb = tk.Radiobutton(add_window, text="Động từ", variable=word_type_var, value="Động từ")
#     radio_noun = tk.Radiobutton(add_window, text="Danh từ", variable=word_type_var, value="Danh từ")
#     radio_adj = tk.Radiobutton(add_window, text="Tính từ", variable=word_type_var, value="Tính từ")
#
#     add_button = tk.Button(add_window, text="Thêm từ vựng", command=add_word)
#
#     label_word.pack()
#     entry_word.pack()
#     label_meaning.pack()
#     entry_meaning.pack()
#     label_word_type.pack()
#     radio_verb.pack()
#     radio_noun.pack()
#     radio_adj.pack()
#     add_button.pack()
def open_add_vocabulary():
    add_window = tk.Toplevel(app)
    add_window.title("Thêm từ vựng")

    # Tạo một frame để chứa các thành phần
    add_frame = tk.Frame(add_window)
    add_frame.pack(padx=20, pady=20)

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

    # Sử dụng Radiobutton để chọn loại từ vựng
    # word_type_var.set("")  # Mặc định không chọn loại
    # radio_verb = tk.Radiobutton(add_frame, text="Động từ", variable=word_type_var, value="Động từ")
    # radio_noun = tk.Radiobutton(add_frame, text="Danh từ", variable=word_type_var, value="Danh từ")
    # radio_adj = tk.Radiobutton(add_frame, text="Tính từ", variable=word_type_var, value="Tính từ")
    #
    # radio_verb.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    # radio_noun.grid(row=2, column=1, padx=10, pady=5, sticky="e")
    # radio_adj.grid(row=2, column=1, padx=10, pady=5, sticky="e")
    label_word_type = tk.Label(add_frame, text="Loại từ vựng:")
    label_word_type.grid(row=2, column=0, sticky="w")

    # Tạo một Combobox cho loại từ vựng
    word_type_combobox = ttk.Combobox(add_frame, values=["Động từ", "Danh từ", "Tính từ"])
    word_type_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    word_type_combobox.set("Chọn loại")  # Giá trị mặc định khi ban đầu

    add_button = tk.Button(add_frame, text="Thêm từ vựng", command=add_word)
    add_button.grid(row=3, columnspan=2, pady=10)

    # Thiết lập đối tượng Text để có thể scroll nếu cần
    scrollbar = tk.Scrollbar(add_frame, command=entry_meaning.yview)
    scrollbar.grid(row=1, column=2, sticky="nse")

    entry_meaning.config(yscrollcommand=scrollbar.set)

# Function to display vocabulary on the main page
def display_vocabulary():
    main_frame = tk.Frame(app, width=400, height=400, bg="white")
    main_frame.pack(expand=True, fill="both")

    menu_bar = Menu(app)
    app.config(menu=menu_bar)

    vocabulary_menu = Menu(menu_bar)
    menu_bar.add_cascade(label="Từ vựng", menu=vocabulary_menu)
    vocabulary_menu.add_command(label="Thêm từ vựng", command=open_add_vocabulary)

    cursor.execute("SELECT * FROM vocabulary")
    words = cursor.fetchall()

    vocab_display = tk.Text(main_frame, height=10, width=65, bg="white", wrap=tk.NONE)
    vocab_display.pack(expand=True, fill="both")

    for i, word in enumerate(words, start=1):
        display_text = f"{i}. Từ vựng: {word[1]} - Nghĩa: {word[2]} - Loại: {word[3]}"
        vocab_display.insert(tk.END, display_text + "\n")
        # vocab_display.insert(tk.END, f"{i}.Từ vựng:{word[1]}, Nghĩa:{word[2]}, Loại:{word[3]}.\n")


word_type_combobox = StringVar()

display_vocabulary()

app.mainloop()
