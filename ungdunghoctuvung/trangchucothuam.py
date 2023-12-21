import tkinter as tk
from tkinter import messagebox, Menu, StringVar, ttk
import mysql.connector
# Import thư viện ghi âm
import sounddevice as sd
import wavio
import playsound
import os
import pygame.mixer

# Khởi tạo mixer của pygame
pygame.mixer.init()

# Create a MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hoctuvung"
)
cursor = db.cursor()

# Create the vocabulary table if it doesn't exist
# Check if the 'completed' column exists in the vocabulary table
cursor.execute("SHOW COLUMNS FROM vocabulary LIKE 'completed'")
column_exists = cursor.fetchone()

# If the column does not exist, add it
if not column_exists:
    cursor.execute("""
        ALTER TABLE vocabulary
        ADD COLUMN completed BOOLEAN NOT NULL DEFAULT 0
    """)
    db.commit()
else:
    print("The 'completed' column already exists in the vocabulary table.")
# Check if the 'audio_file' column exists in the vocabulary table
cursor.execute("SHOW COLUMNS FROM vocabulary LIKE 'audio_file'")
column_exists = cursor.fetchone()

# If the column does not exist, add it
if not column_exists:
    cursor.execute("""
        ALTER TABLE vocabulary
        ADD COLUMN audio_file VARCHAR(255)
    """)
    db.commit()
else:
    print("The 'audio_file' column already exists in the vocabulary table.")

db.commit()

# Create tkinter app
app = tk.Tk()
app.title("Ứng dụng học từ vựng")
app.geometry("600x600")
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

# Function to search for vocabulary
def search_vocabulary():
    search_term = entry_search.get()

    # Clear the current display
    vocabulary_tree.delete(*vocabulary_tree.get_children())

    # Fetch and display matching vocabulary items
    cursor.execute("SELECT * FROM vocabulary WHERE word LIKE %s", (f"%{search_term}%",))
    words = cursor.fetchall()

    for word in words:
        vocabulary_tree.insert("", "end", values=(word[1], word[2], word[3]))

# Function to delete a word from the database
def delete_word():
    selected_item = vocabulary_tree.selection()
    if not selected_item:
        messagebox.showinfo("Thông báo", "Vui lòng chọn từ vựng để xóa.")
        return

    word = vocabulary_tree.item(selected_item, "values")[0]

    if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa từ vựng '{word}' này?"):
        cursor.execute("DELETE FROM vocabulary WHERE word=%s", (word,))
        db.commit()
        messagebox.showinfo("Thông báo", f"Xóa từ vựng '{word}' thành công.")
        display_vocabulary()

# Function to toggle the completion status of a word
# def toggle_completion():
#     selected_item = vocabulary_tree.selection()
#     if not selected_item:
#         messagebox.showinfo("Thông báo", "Vui lòng chọn từ vựng để đánh dấu hoàn thành hoặc chưa hoàn thành.")
#         return
#
#     word_id = vocabulary_tree.item(selected_item, "values")[0]
#     cursor.execute("SELECT completed FROM vocabulary WHERE id=%s", (word_id,))
#     current_status = cursor.fetchone()[0]
#
#     new_status = not current_status
#     cursor.execute("UPDATE vocabulary SET completed=%s WHERE id=%s", (new_status, word_id))
#     db.commit()
#     display_vocabulary()
def toggle_completion():
    selected_item = vocabulary_tree.selection()
    if not selected_item:
        messagebox.showinfo("Thông báo", "Vui lòng chọn từ vựng để đánh dấu hoàn thành hoặc chưa hoàn thành.")
        return

    word = vocabulary_tree.item(selected_item, "values")[0]  # Get the word itself
    cursor.execute("SELECT completed FROM vocabulary WHERE word=%s", (word,))
    row = cursor.fetchone()

    if row is not None:
        current_status = row[0]
        new_status = not current_status
        cursor.execute("UPDATE vocabulary SET completed=%s WHERE word=%s", (new_status, word))
        db.commit()
        display_vocabulary()
    else:
        messagebox.showinfo("Thông báo", f"Không tìm thấy từ vựng '{word}' trong cơ sở dữ liệu.")

# Function to display the total count of vocabulary items
def display_total_count():
    cursor.execute("SELECT COUNT(*) FROM vocabulary")
    total_count = cursor.fetchone()[0]
    total_count_label.config(text=f"Tổng số từ vựng đã có: {total_count}")

# Function to record and save audio for a vocabulary word
def record_audio():
    selected_item = vocabulary_tree.selection()
    if not selected_item:
        messagebox.showinfo("Thông báo", "Vui lòng chọn từ vựng để ghi âm.")
        return

    word = vocabulary_tree.item(selected_item, "values")[0]  # Get the word itself

    # Ghi âm
    fs = 44100  # Tần số lấy mẫu
    duration = 5  # Thời gian ghi âm (ví dụ: 5 giây)
    recording = sd.rec(int(fs * duration), samplerate=fs, channels=2)
    sd.wait()

    # Lưu file âm thanh
    file_name = f"{word}.wav"
    wavio.write(file_name, recording, fs, sampwidth=3)

    # Lưu tên tệp âm thanh vào cơ sở dữ liệu hoặc thông báo thành công
    cursor.execute("UPDATE vocabulary SET audio_file=%s WHERE word=%s", (file_name, word))
    db.commit()
    messagebox.showinfo("Thông báo", f"Đã ghi âm cho từ vựng '{word}' và lưu thành công.")

# def play_audio():
#     selected_item = vocabulary_tree.selection()
#     if not selected_item:
#         messagebox.showinfo("Thông báo", "Vui lòng chọn từ vựng để nghe âm thanh.")
#         return
#
#     audio_file = vocabulary_tree.item(selected_item, "values")[5]  # Lấy tên tệp âm thanh từ cột "Tệp Âm Thanh"
#     print(f"Attempting to play audio file: {audio_file}")
#     if audio_file:
#         # Kiểm tra xem tệp âm thanh có tồn tại trước khi thử phát nó
#         import os
#         if os.path.exists(audio_file):
#             try:
#                 # Sử dụng thư viện để phát tệp âm thanh ở đây (ví dụ: pygame hoặc playsound)
#                 # Đảm bảo cài đặt thư viện phát âm thanh trước
#                 # Ví dụ sử dụng thư viện playsound
#                 import playsound
#                 playsound.playsound(audio_file)
#             except Exception as e:
#                 messagebox.showerror("Lỗi", f"Lỗi khi phát âm thanh: {str(e)}")
#         else:
#             messagebox.showinfo("Thông báo", "Tệp âm thanh không tồn tại.")
#     else:
#         messagebox.showinfo("Thông báo", "Từ vựng này chưa có tệp âm thanh.")

def play_audio():
    selected_item = vocabulary_tree.selection()
    if not selected_item:
        messagebox.showinfo("Thông báo", "Vui lòng chọn từ vựng để nghe âm thanh.")
        return

    audio_file = vocabulary_tree.item(selected_item, "values")[5]  # Lấy tên tệp âm thanh từ cột "Tệp Âm Thanh"
    print(audio_file)
    if audio_file:
        # Kiểm tra xem tệp âm thanh có tồn tại trước khi thử phát nó
        if os.path.exists(audio_file):
            try:
                # Sử dụng thư viện pygame để phát âm thanh
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi phát âm thanh: {str(e)}")
        else:
            messagebox.showinfo("Thông báo", "Tệp âm thanh không tồn tại.")
    else:
        messagebox.showinfo("Thông báo", "Từ vựng này chưa có tệp âm thanh.")

# Function to display vocabulary in a table on the home page
def display_vocabulary():
    if "vocabulary_tree" in globals():
        vocabulary_tree.delete(*vocabulary_tree.get_children())

    cursor.execute("SELECT * FROM vocabulary")
    words = cursor.fetchall()

    for word in words:
        word_id, word_text, meaning, word_type, completed, audio_file = word
        status_text = "Hoàn thành" if completed else "Chưa hoàn thành"
        if audio_file:
            audio_status = "Có âm thanh"
        else:
            audio_status = "Không có âm thanh"
        vocabulary_tree.insert("", "end", values=(word_text, meaning, word_type, status_text, audio_status, audio_file))
    # for word in words:
    #     word_id, word_text, meaning, word_type, completed, audio_file = word
    #     status_text = "Hoàn thành" if completed else "Chưa hoàn thành"
    #     vocabulary_tree.insert("", "end", values=(word_text, meaning, word_type, status_text, audio_file))

# Create a frame for the vocabulary display
display_frame = ttk.Frame(app)
display_frame.pack(fill="both", expand=True)

# Create an entry widget for searching
entry_search = ttk.Entry(app)
entry_search.pack(pady=10)
search_button = ttk.Button(app, text="Tìm Kiếm", command=search_vocabulary)
search_button.pack()
# Create a button for deleting vocabulary items on the "Home" page
delete_button = ttk.Button(app, text="Xóa từ vựng", command=delete_word)
delete_button.pack()

# Create a button for toggling the completion status of vocabulary items on the "Home" page
toggle_completion_button = ttk.Button(app, text="Đánh dấu hoàn thành/Chưa hoàn thành", command=toggle_completion)
toggle_completion_button.pack()

# Thêm nút "Thu âm" vào giao diện
record_audio_button = ttk.Button(app, text="Thu âm từ vựng", command=record_audio)
record_audio_button.pack()

play_audio_button = ttk.Button(app, text="Nghe Âm Thanh", command=play_audio)
play_audio_button.pack()

# Create a label for displaying the total count
total_count_label = ttk.Label(app, text="", font=("Arial", 12))
total_count_label.pack()

# Create a Treeview widget for displaying vocabulary
vocabulary_tree = ttk.Treeview(display_frame, columns=("Word", "Meaning", "Word Type", "Complete", "Audio File"), show="headings")
vocabulary_tree.heading("Word", text="Từ vựng")
vocabulary_tree.heading("Meaning", text="Nghĩa")
vocabulary_tree.heading("Word Type", text="Loại từ vựng")
vocabulary_tree.heading("Complete", text="Hoàn thành")
vocabulary_tree.heading("Audio File", text="Tệp Âm Thanh")  # Tiêu đề cho cột mới
# Set the column widths
vocabulary_tree.column("Word", width=60)  # Adjust the width as needed
vocabulary_tree.column("Meaning", width=200)  # Adjust the width as needed
vocabulary_tree.column("Word Type", width=100)  # Adjust the width as needed
vocabulary_tree.column("Complete", width=120)  # Adjust the width as needed
vocabulary_tree.column("Audio File", width=150)
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
vocabulary_menu.add_command(label="Hiển thị tổng số từ vựng", command=display_total_count)

# Initial display of vocabulary
display_vocabulary()
display_total_count()

app.mainloop()
