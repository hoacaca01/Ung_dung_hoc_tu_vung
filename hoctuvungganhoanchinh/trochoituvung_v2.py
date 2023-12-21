import tkinter as tk
from tkinter import messagebox
import random

def toggle_color(word_label):
    current_color = word_label.cget("bg")
    if current_color == "red":
        word_label.config(bg="yellow")
        selected_words.append(word_label)
    else:
        word_label.config(bg="red")
        selected_words.remove(word_label)
    check_match()

def toggle_meaning_color(meaning_label):
    current_color = meaning_label.cget("bg")
    if current_color == "red":
        meaning_label.config(bg="yellow")
        selected_meanings.append(meaning_label)
    else:
        meaning_label.config(bg="red")
        selected_meanings.remove(meaning_label)
    check_match()

def check_match():
    if len(selected_words) == 1 and len(selected_meanings) == 1:
        word_label = selected_words[0]
        meaning_label = selected_meanings[0]

        word = word_label.cget("text")
        meaning = meaning_label.cget("text")

        if word_to_meaning[word] == meaning:
            messagebox.showinfo("Kết quả", "Bạn đã chọn đúng nghĩa từ vựng!")
            word_label.config(text="")
            meaning_label.config(text="")
            selected_words.remove(word_label)
            selected_meanings.remove(meaning_label)
            check_game_over()
        else:
            messagebox.showinfo("Kết quả", "Bạn đã chọn sai nghĩa của từ vựng!")
            for label in selected_words + selected_meanings:
                label.config(bg="red")
            selected_words.clear()
            selected_meanings.clear()

def check_game_over():
    if all(label.cget("text") == "" for label in left_labels) and all(
            label.cget("text") == "" for label in right_labels):
        messagebox.showinfo("Kết thúc", "Chúc mừng bạn đã hoàn thành trò chơi!")
        root.quit()

def shuffle_and_create_labels():
    # Trộn ngẫu nhiên danh sách từ vựng và nghĩa từ vựng
    random.shuffle(vocabulary)
    random.shuffle(meanings)

    for i in range(3):
        row_frame_left = tk.Frame(left_frame)
        row_frame_left.pack()
        row_frame_right = tk.Frame(right_frame)
        row_frame_right.pack()

        for j in range(3):
            index = i * 3 + j
            left_label = tk.Label(row_frame_left, width=10, height=5, bg="red", relief="solid", text=vocabulary[index])
            left_label.pack(side=tk.LEFT)
            left_labels.append(left_label)
            left_label.bind("<Button-1>", lambda event, word_label=left_label: toggle_color(word_label))

            right_label = tk.Label(row_frame_right, width=10, height=5, bg="red", relief="solid", text=meanings[index])
            right_label.pack(side=tk.LEFT)
            right_labels.append(right_label)
            right_label.bind("<Button-1>", lambda event, meaning_label=right_label: toggle_meaning_color(meaning_label))

# Khởi tạo cửa sổ gốc
root = tk.Tk()
root.title("Giao diện 3x3")
root.geometry("600x600")

# Khai báo danh sách từ vựng và nghĩa từ vựng
vocabulary = ["hello", "sun", "tree", "cat", "dog", "house", "car", "book", "computer"]
meanings = ["xin chào", "mặt trời", "cây", "mèo", "chó", "nhà", "xe hơi", "sách", "máy tính"]
word_to_meaning = {vocabulary[i]: meanings[i] for i in range(len(vocabulary))}

separator = tk.Frame(root, width=2, bd=2, relief=tk.SUNKEN)
separator.pack(side=tk.LEFT, fill=tk.Y)

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT)

vocab_label = tk.Label(left_frame, text="Từ Vựng", font=("Helvetica", 12))
vocab_label.pack()

meaning_label = tk.Label(right_frame, text="Nghĩa Từ Vựng", font=("Helvetica", 12))
meaning_label.pack()

left_labels = []
right_labels = []
selected_words = []
selected_meanings = []

# Gọi hàm để xáo trộn danh sách và tạo các ô Label
shuffle_and_create_labels()

root.mainloop()
