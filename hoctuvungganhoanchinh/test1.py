import tkinter as tk
from tkinter import messagebox, Menu, StringVar, ttk
import mysql.connector
# Import thư viện ghi âm
import sounddevice as sd
import wavio
import playsound
import pygame.mixer
import requests
from bs4 import BeautifulSoup
import subprocess
import tempfile
import shutil
import os
from urllib.parse import quote_plus
from PIL import Image, ImageTk
from io import BytesIO
import random

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


# Check if the 'audio_file' column exists in the vocabulary table
cursor.execute("SHOW COLUMNS FROM vocabulary LIKE 'audio_file'")
column_exists = cursor.fetchone()


db.commit()

# Create tkinter app
app = tk.Tk()
app.title("Ứng dụng học từ vựng")
# app.geometry("600x600")

# Hàm để hiển thị thông tin sản phẩm và người làm ra sản phẩm
def show_about_info():
    # Tạo một cửa sổ mới
    about_window = tk.Toplevel(app)
    about_window.title("Thông tin sản phẩm và tác giả")

    # Tạo một Frame để chứa thông tin
    info_frame = tk.Frame(about_window, padx=20, pady=20)
    info_frame.pack()

    # Tạo một Label để hiển thị thông tin
    about_label = tk.Label(info_frame, text="Ứng dụng học từ vựng", font=("Arial", 14, "bold"))
    about_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

    version_label = tk.Label(info_frame, text="Phiên bản: 1.0", font=("Arial", 12))
    version_label.grid(row=1, column=0, columnspan=2)

    divider = tk.Label(info_frame, text="---------------------------------", font=("Arial", 12))
    divider.grid(row=2, column=0, columnspan=2, pady=(10, 20))

    creator_label = tk.Label(info_frame, text="Tác Giả:", font=("Arial", 12, "bold"))
    creator_label.grid(row=3, column=0, columnspan=2)

    name_label = tk.Label(info_frame, text="- Họ và tên: Phạm Xuân Hòa", font=("Arial", 12))
    name_label.grid(row=4, column=0, columnspan=2, sticky="w")

    email_label = tk.Label(info_frame, text="- Email: tieucaca876@gmail.com", font=("Arial", 12))
    email_label.grid(row=5, column=0, columnspan=2, sticky="w")

    phone_label = tk.Label(info_frame, text="- Số điện thoại: 0762169854", font=("Arial", 12))
    phone_label.grid(row=6, column=0, columnspan=2, sticky="w")

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

# Function to add a word and its meaning automatically
def add_meaning():
    word = entry_word.get()
    search_url = f"https://dict.laban.vn/find?type=1&query={word}"

    try:
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Find and extract the meaning from the website
        meaning_div = soup.find("div", {"id": "content_selectable", "class": "content"})
        if meaning_div:
            meaning = meaning_div.get_text()
        else:
            meaning = "Không tìm thấy nghĩa."

        # Populate the meaning in the entry_meaning widget
        entry_meaning.delete("1.0", tk.END)
        entry_meaning.insert(tk.END, meaning)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm nghĩa từ trang web: {str(e)}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi không xác định: {str(e)}")

# Function to search for vocabulary
def search_vocabulary():
    search_term = entry_search.get()

    # Clear the current display
    vocabulary_tree.delete(*vocabulary_tree.get_children())

    # Fetch and display matching vocabulary items
    cursor.execute("SELECT * FROM vocabulary WHERE word LIKE %s", (f"%{search_term}%",))
    words = cursor.fetchall()

    for word in words:
        vocabulary_tree.insert("", "end", values=(word[1], word[2], word[3], word[4], word[5]))

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

def hienthi_anh(word):
    # Tạo URL tìm kiếm Google
    search_url = f"https://www.google.com/search?q={quote_plus(word)}&source=lnms&tbm=isch"

    # Gửi yêu cầu GET đến trang tìm kiếm Google
    response = requests.get(search_url)

    # Kiểm tra xem yêu cầu có thành công không
    if response.status_code == 200:
        # Sử dụng BeautifulSoup để phân tích mã HTML của trang
        soup = BeautifulSoup(response.text, 'html.parser')

        # Tìm tất cả các thẻ img trong trang
        img_tags = soup.find_all('img')

        # Tìm ảnh đầu tiên hợp lệ (chứa giao thức http hoặc https)
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url and img_url.startswith('http'):
                # Tải và chuyển đổi ảnh sang định dạng GIF
                image_response = requests.get(img_url)
                image_data = Image.open(BytesIO(image_response.content))
                image_data = image_data.convert("RGB")
                image_data.save("temp.gif", "GIF")  # Lưu vào một tệp tạm thời

                return Image.open("temp.gif")  # Trả về ảnh đã chuyển đổi
                break
        else:
            print("Không tìm thấy ảnh hợp lệ.")
    else:
        print("Lỗi khi gửi yêu cầu GET đến trang tìm kiếm Google.")
    return None

def play_original_audio(word):
    url = f"https://translate.google.com.vn/translate_tts?ie=UTF-8&q={word}&tl=en&client=tw-ob"
    try:
        # Create a temporary directory to store the audio file
        temp_dir = tempfile.mkdtemp()
        audio_file_path = os.path.join(temp_dir, f"{word}.mp3")

        # Download the audio file from the URL and save it to the temporary directory
        response = requests.get(url)
        with open(audio_file_path, 'wb') as audio_file:
            audio_file.write(response.content)

        # Play the downloaded audio file
        playsound.playsound(audio_file_path)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi phát âm thanh từ URL gốc: {str(e)}")
    finally:
        # Cleanup: Delete the temporary directory and its contents
        shutil.rmtree(temp_dir, ignore_errors=True)

# Hàm để xử lý sự kiện nút "Nghe Âm Thanh Gốc"
def play_original_audio_button():
    selected_item = vocabulary_tree.selection()
    if not selected_item:
        messagebox.showinfo("Thông báo", "Vui lòng chọn từ vựng để nghe âm thanh gốc.")
        return

    selected_word = vocabulary_tree.item(selected_item, "values")[0]  # Lấy từ vựng
    play_original_audio(selected_word)

def on_treeview_click(event):
    item = vocabulary_tree.selection()  # Lấy phần tử được chọn trong Treeview
    if item:
        word = vocabulary_tree.item(item, "values")[0]  # Lấy từ vựng từ phần tử được chọn
        display_word_details(word)  # Hiển thị thông tin chi tiết của từ vựng

# Tạo biến toàn cục để lưu trữ tham chiếu đến ảnh
current_image = None

def display_word_details(word):
    global current_image  # Sử dụng biến toàn cục
    # Tạo cửa sổ chi tiết
    word_details_window = tk.Toplevel(app)
    word_details_window.title(f"Chi tiết từ vựng: {word}")

    # Truy vấn cơ sở dữ liệu để lấy thông tin chi tiết của từ vựng
    cursor.execute("SELECT * FROM vocabulary WHERE word=%s", (word,))
    word_details = cursor.fetchone()

    if word_details:
        word_id, word_text, meaning, word_type, completed, audio_file = word_details

        # Tạo một Frame để chứa thông tin chi tiết
        details_frame = ttk.Frame(word_details_window, padding=10)
        details_frame.pack()

        # Tạo một Canvas để đặt details_frame và thanh cuộn
        canvas = tk.Canvas(details_frame, height=400, width=600)  # Set the height as needed
        canvas.pack(side="left", fill="both", expand=True)

        # Tạo một thanh cuộn cho canvas
        scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Kết nối thanh cuộn với canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Tạo một khung con trong canvas để đặt các widget
        details_frame_canvas = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=details_frame_canvas, anchor="nw")

        # Label và nội dung cho từng thông tin
        label_word = ttk.Label(details_frame_canvas, text="Từ vựng:", font=("Arial", 12, "bold"), foreground="blue")
        label_word.grid(row=0, column=0, sticky="w")
        label_word_text = ttk.Label(details_frame_canvas, text=word_text, font=("Arial", 12, "bold"), foreground="blue")
        label_word_text.grid(row=0, column=1, sticky="w")

        # Hiển thị ảnh từ Google
        image_data = hienthi_anh(word)

        # Tạo một biến thay thế để giữ tham chiếu đến ảnh
        if image_data:
            current_image = ImageTk.PhotoImage(image_data)
        else:
            current_image = None

        # Hiển thị ảnh trong một Label
        if current_image:
            label_image = ttk.Label(details_frame_canvas, image=current_image)
            label_image.grid(row=1, column=1, columnspan=2, pady=10, sticky="w")
        else:
            label_no_image = ttk.Label(details_frame_canvas, text="Không tìm thấy ảnh cho từ vựng này.",
                                       font=("Arial", 12), foreground="red")
            label_no_image.grid(row=1, column=1, columnspan=2, pady=10, sticky="w")

        label_meaning = ttk.Label(details_frame_canvas, text="Nghĩa:", font=("Arial", 12, "bold"), foreground="green")
        label_meaning.grid(row=2, column=0, sticky="w")
        label_meaning_text = ttk.Label(details_frame_canvas, text=meaning, font=("Arial", 10), foreground="green")
        label_meaning_text.grid(row=2, column=1, sticky="w")

        label_word_type = ttk.Label(details_frame_canvas, text="Loại từ vựng:", font=("Arial", 12, "bold"), foreground="purple")
        label_word_type.grid(row=3, column=0, sticky="w")
        label_word_type_text = ttk.Label(details_frame_canvas, text=word_type, font=("Arial", 10), foreground="purple")
        label_word_type_text.grid(row=3, column=1, sticky="w")

        label_completion = ttk.Label(details_frame_canvas, text="Trạng thái hoàn thành:", font=("Arial", 12, "bold"), foreground="red")
        label_completion.grid(row=4, column=0, sticky="w")
        label_completion_text = ttk.Label(details_frame_canvas, text='Hoàn thành' if completed else 'Chưa hoàn thành', font=("Arial", 10), foreground="red")
        label_completion_text.grid(row=4, column=1, sticky="w")

        if audio_file:
            # Nếu có tệp âm thanh, hiển thị nút để phát âm thanh
            play_audio_button = ttk.Button(details_frame_canvas, text="Nghe Âm Thanh Thu", command=play_audio)
            play_audio_button.grid(row=5, column=0, pady=10, columnspan=2, sticky="w")
        else:
            label_audio_status = ttk.Label(details_frame_canvas, text="Từ vựng này chưa có tệp âm thanh.", font=("Arial", 10), foreground="orange")
            label_audio_status.grid(row=5, column=0, pady=10, columnspan=2, sticky="w")

        play_audio_button = ttk.Button(details_frame_canvas, text="Nghe Âm Thanh Gốc", command=play_original_audio_button)
        play_audio_button.grid(row=6, column=0, pady=10, columnspan=2, sticky="w")


        # Update the canvas scroll region when the widgets inside details_frame_canvas change
        details_frame_canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Add bindings to make the canvas scrollable with the mouse
        canvas.bind("<Enter>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

    else:
        label_not_found = ttk.Label(word_details_window, text="Không tìm thấy thông tin cho từ vựng này.", font=("Arial", 12, "bold"), foreground="red")
        label_not_found.pack()

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
        vocabulary_tree.insert("", "end", values=(word_text, meaning, word_type, status_text, audio_status, audio_file, word_text))

# Create a frame for buttons
button_frame1 = ttk.Frame(app)
button_frame1.pack()

# Create a button to open the "Thêm từ vựng" window
add_vocabulary_button = ttk.Button(button_frame1, text="Thêm từ vựng", command=open_add_vocabulary)
add_vocabulary_button.grid(row=0, column=0, padx=10, pady=5)

# Create a frame for the vocabulary display
display_frame = ttk.Frame(app)
display_frame.pack(fill="both", expand=True)


# Create a Treeview widget for displaying vocabulary
vocabulary_tree = ttk.Treeview(display_frame, columns=("Word", "Meaning", "Word Type", "Complete", "Audio File"), show="headings")

# Create a vertical scrollbar
vscrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=vocabulary_tree.yview)
vscrollbar.pack(side="right", fill="y")

# Configure the Treeview to use the scrollbar
vocabulary_tree.configure(yscrollcommand=vscrollbar.set)

# # Gán sự kiện nhấp chuột trái vào Treeview
# vocabulary_tree.bind("<Button-1>", on_treeview_click)

vocabulary_tree.heading("Word", text="Từ vựng")
vocabulary_tree.heading("Meaning", text="Nghĩa")
vocabulary_tree.heading("Word Type", text="Loại từ vựng")
vocabulary_tree.heading("Complete", text="Hoàn thành")
vocabulary_tree.heading("Audio File", text="Tệp Âm Thanh")  # Tiêu đề cho cột mới
# Set the column widths
vocabulary_tree.column("Word", width=100)
vocabulary_tree.column("Meaning", width=200)
vocabulary_tree.column("Word Type", width=100)
vocabulary_tree.column("Complete", width=100)
vocabulary_tree.column("Audio File", width=150)
vocabulary_tree.pack(fill="both", expand=True)

# Gán sự kiện nhấp chuột trái vào Treeview
# vocabulary_tree.bind("<Button-1>", on_treeview_click)
# vocabulary_tree.bind("<Button-3>", on_treeview_click)
vocabulary_tree.bind("<Double-1>", on_treeview_click)

# Create a frame for buttons
button_frame = ttk.Frame(app)
button_frame.pack()

# Create an entry widget for searching
entry_search = ttk.Entry(button_frame)
entry_search.grid(row=0, column=0, padx=10, pady=5)
search_button = ttk.Button(button_frame, text="Tìm Kiếm", command=search_vocabulary)
search_button.grid(row=0, column=1, padx=10, pady=5)

# Create buttons for other actions
delete_button = ttk.Button(button_frame, text="Xóa từ vựng", command=delete_word)
delete_button.grid(row=0, column=2, padx=10, pady=5)

toggle_completion_button = ttk.Button(button_frame, text="Đánh dấu hoàn thành/Chưa hoàn thành", command=toggle_completion)
toggle_completion_button.grid(row=0, column=3, padx=10, pady=5)

record_audio_button = ttk.Button(button_frame, text="Thu âm từ vựng", command=record_audio)
record_audio_button.grid(row=0, column=4, padx=10, pady=5)

play_audio_button = ttk.Button(button_frame, text="Nghe Âm Thanh Thu", command=play_audio)
play_audio_button.grid(row=0, column=5, padx=10, pady=5)

play_audio_button = ttk.Button(button_frame, text="Nghe Âm Thanh Gốc", command=play_original_audio_button)
play_audio_button.grid(row=0, column=6, padx=10, pady=5)

# Create a label for displaying the total count
total_count_label = ttk.Label(app, text="", font=("Arial", 12))
total_count_label.pack()

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

    add_button = tk.Button(add_frame, text="Thêm nghĩa tự động", command=add_meaning)
    add_button.grid(row=2, column=1, pady=10)

    label_word_type = tk.Label(add_frame, text="Loại từ vựng:")
    label_word_type.grid(row=3, column=0, sticky="w")

    # Use Radiobuttons to select word type
    word_type_var.set("")  # Default to no selection
    radio_verb = tk.Radiobutton(add_frame, text="Động từ", variable=word_type_var, value="Động từ")
    radio_noun = tk.Radiobutton(add_frame, text="Danh từ", variable=word_type_var, value="Danh từ")
    radio_adj = tk.Radiobutton(add_frame, text="Tính từ", variable=word_type_var, value="Tính từ")

    radio_verb.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    radio_noun.grid(row=3, column=2, padx=10, pady=5, sticky="e")
    radio_adj.grid(row=3, column=1, padx=10, pady=5, sticky="e")

    add_button = tk.Button(add_frame, text="Thêm từ vựng", command=add_word)
    add_button.grid(row=4, columnspan=2, pady=10)

    # Set up a scrollbar for the Text widget if needed
    scrollbar = tk.Scrollbar(add_frame, command=entry_meaning.yview)
    scrollbar.grid(row=1, column=2, sticky="nse")
    entry_meaning.config(yscrollcommand=scrollbar.set)

# Create a menu
menu_bar = Menu(app)
app.config(menu=menu_bar)

vocabulary_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Từ vựng", menu=vocabulary_menu)
# vocabulary_menu.add_command(label="Thêm từ vựng", command=open_add_vocabulary)

vocabulary_menu1 = Menu(menu_bar)
menu_bar.add_cascade(label="Thống kê", menu=vocabulary_menu1)
vocabulary_menu1.add_command(label="Hiển thị tổng số từ vựng", command=display_total_count)

vocabulary_menu3 = Menu(menu_bar)
menu_bar.add_cascade(label="Giới thiệu", menu=vocabulary_menu3)
vocabulary_menu3.add_command(label="Thông tin sản phẩm", command=show_about_info)

# Initial display of vocabulary
display_vocabulary()
display_total_count()

app.mainloop()

