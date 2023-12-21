import tkinter as tk
from tkinter import messagebox


def toggle_color(square):
    current_color = square.cget("bg")
    if current_color == "red":
        square.config(bg="blue")
    else:
        square.config(bg="red")


def check_match(word_label, meaning_label):
    word = word_label.cget("text")
    meaning = meaning_label.cget("text")

    if word_to_meaning[word] == meaning:
        messagebox.showinfo("Kết quả", "Bạn đã chọn đúng nghĩa từ vựng!")
        word_label.config(text="")
        meaning_label.config(text="")
        check_game_over()


def check_game_over():
    if all(label.cget("text") == "" for label in left_labels) and all(
            label.cget("text") == "" for label in right_labels):
        messagebox.showinfo("Kết thúc", "Chúc mừng bạn đã hoàn thành trò chơi!")
        root.quit()


root = tk.Tk()
root.title("Giao diện 3x3")

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

for i in range(3):
    row_frame_left = tk.Frame(left_frame)
    row_frame_left.pack()
    row_frame_right = tk.Frame(right_frame)
    row_frame_right.pack()

    for j in range(3):
        index = i * 3 + j
        left_label = tk.Label(row_frame_left, width=10, height=5, bg="red", relief="solid", text=vocabulary[index])
        left_label.pack(side=tk.LEFT)
        left_label.bind("<Button-1>", lambda event, word=left_label: toggle_color(word))
        left_labels.append(left_label)

        right_label = tk.Label(row_frame_right, width=10, height=5, bg="blue", relief="solid", text=meanings[index])
        right_label.pack(side=tk.LEFT)
        right_label.bind("<Button-1>", lambda event, meaning=right_label, word=left_label: check_match(word, meaning))
        right_labels.append(right_label)

root.mainloop()
