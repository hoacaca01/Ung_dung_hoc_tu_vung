import tkinter as tk
import random

# Danh sách cặp từ vựng và nghĩa
word_meaning_pairs = [("apple", "quả táo"), ("banana", "quả chuối"), ("cat", "con mèo"), ("dog", "con chó")]

# Trộn ngẫu nhiên cặp từ vựng và nghĩa
random.shuffle(word_meaning_pairs)

# Tạo danh sách để lưu trữ các cặp từ vựng và nghĩa đã nối đúng
correct_matches = []
# print(correct_matches)

def check_completion():
    incorrect_matches = []
    for word, meaning in word_meaning_pairs:
        user_input = word_meaning_entries[word].get()
        print("----------")
        print(user_input)
        print("----------")
        if user_input.lower() != meaning.lower():
            print("***********")
            print(meaning)
            print("***********")
            incorrect_matches.append((word, meaning))
            print("++++++++++++++")
            print(incorrect_matches)
            print("++++++++++++++")

    if len(incorrect_matches) == 0:
        result_label.config(text="Chúc mừng! Bạn đã nối đúng tất cả các từ vựng.")
    else:
        result_label.config(text="Các cặp sau không đúng:")
        for word, meaning in incorrect_matches:
            result_label.config(text=result_label.cget("text") + f"\n{word} - {meaning}")

app = tk.Tk()
app.title("Trò chơi nối từ vựng")

# Tạo Label để hiển thị hướng dẫn
instruction_label = tk.Label(app, text="Nối từ và nghĩa phù hợp:", font=("Arial", 12))
instruction_label.pack(pady=10)

word_meaning_entries = {}  # Dictionary để lưu trữ Entry widgets

# Tạo các Entry widgets để người dùng nhập từ
for word, _ in word_meaning_pairs:
    label = tk.Label(app, text=word, font=("Arial", 12))
    label.pack()
    entry = tk.Entry(app, font=("Arial", 12))
    entry.pack()
    word_meaning_entries[word] = entry

# Tạo nút để kiểm tra hoàn thành
check_button = tk.Button(app, text="Kiểm tra hoàn thành", command=check_completion, font=("Arial", 12))
check_button.pack(pady=10)

result_label = tk.Label(app, text="", font=("Arial", 12))
result_label.pack()

app.mainloop()
