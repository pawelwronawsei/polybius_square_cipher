import tkinter as tk
import csv

valid_alphabet = ['a', 'ą', 'b', 'c', 'ć', 'd', 'e', 'ę', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'ł',
'm', 'n', 'ń', 'o', 'ó', 'p', 'q', 'r', 's', 'ś', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ź', 'ż']

def load_key(file_name):
    with open(file_name, newline='', encoding='utf-8') as key_file:
        key = csv.reader(key_file)
        key = [row for row in key]

        key_reshaped = [item for row in key for item in row]

        if sorted(key_reshaped) != sorted(valid_alphabet):
            raise ValueError("The key matrix is incorrect.")

        return key

def use_key(char_to_encrypt):
    for row_idx, row in enumerate(key):
        for c_idx, c in enumerate(row):
            if c == char_to_encrypt:
                return str(row_idx + 1) + str(c_idx + 1)

def encrypt():
    input_text = encrypt_entry1.get()
    if any(x in valid_alphabet for x in input_text):
        text_with_key = [use_key(c) for c in input_text if c in valid_alphabet]
        x = int(''.join(text_with_key))
        transformed_number = 2 * x + 1234
        encrypt_response.config(text=str(transformed_number))
    else:
        encrypt_response.config(text="Wpisz tekst do zaszyfrowania!")

def can_convert_to_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def divide_into_pairs(number):
    number_as_str = str(number)
    result = []

    for i in range(0, len(number_as_str), 2):
        result.append(int(number_as_str[i:i+2]))

    return result

def decrypt():
    input_text = decrypt_entry1.get()

    if not input_text.isdigit():
        decrypt_response.config(text="Wprowadzony szyfr jest niepoprawny!")
        return

    if can_convert_to_number(input_text) and int(input_text) >= (11 * 2) + 1234:
        input_text_as_num_decrypted = (int(input_text) - 1234) // 2
        if len(str(input_text_as_num_decrypted)) % 2 == 0:
            num_pairs = divide_into_pairs(input_text_as_num_decrypted)
            decrypted_result = []

            for p in num_pairs:
                row_idx = p // 10 - 1
                col_idx = p % 10 - 1
                if 0 <= row_idx < len(key) and 0 <= col_idx < len(key[0]):
                    decrypted_result.append(key[row_idx][col_idx])
                else:
                    decrypt_response.config(text="Wprowadzony szyfr jest niepoprawny!")
                    return

            decrypted_result_str = ''.join(decrypted_result)
            decrypt_response.config(text=decrypted_result_str)
        else:
            decrypt_response.config(text="Wprowadzony szyfr jest niepoprawny! Zły format!")
    else:
        decrypt_response.config(text="Wprowadzony szyfr jest niepoprawny lub za krótki!")

key = load_key('key.csv')
print(key)

#TWORZY GŁÓWNE OKNO
root = tk.Tk()
root.title("Szyfr Polibiusza")
root.geometry("800x400")

root.configure(bg="#2D2D2D")

#SZYFROWANIE
encrypt_box = tk.Frame(root, padx=10, pady=10, bg="#2D2D2D")
encrypt_box.pack(pady=20)

encrypt_label0 = tk.Label(encrypt_box, text="SZYFROWANIE", bg="#2D2D2D", fg="#FFFFFF", font=("Helvetica", 16))
encrypt_label0.grid(row=0, column=0, columnspan=2, pady=10)

enccrypt_label1 = tk.Label(encrypt_box, text="Tekst do zaszyfrowania:", bg="#2D2D2D", fg="#FFFFFF")
enccrypt_label1.grid(row=1, column=0, pady=10)

encrypt_entry1 = tk.Entry(encrypt_box, width=50, bg="#4D4D4D", fg="#FFFFFF", insertbackground='white')
encrypt_entry1.grid(row=1, column=1, pady=10)

encrypt_btn = tk.Button(encrypt_box, text="Szyfruj", command=encrypt, bg="#3E3E3E", fg="#FFFFFF")
encrypt_btn.grid(row=2, column=0, columnspan=2, pady=10)

encrypt_response = tk.Label(encrypt_box, text="", bg="#2D2D2D", fg="#00FF00")  # Green text for encrypted response
encrypt_response.grid(row=3, column=0, columnspan=2)

#DESZYFROWANIE
decrypt_box = tk.Frame(root, padx=10, pady=10, bg="#2D2D2D")
decrypt_box.pack(pady=20)

decrypt_label0 = tk.Label(decrypt_box, text="DESZYFROWANIE", bg="#2D2D2D", fg="#FFFFFF", font=("Helvetica", 16))
decrypt_label0.grid(row=0, column=0, columnspan=2, pady=10)

deccrypt_label1 = tk.Label(decrypt_box, text="Tekst do odszyfrowania:", bg="#2D2D2D", fg="#FFFFFF")
deccrypt_label1.grid(row=1, column=0, pady=10)

decrypt_entry1 = tk.Entry(decrypt_box, width=50, bg="#4D4D4D", fg="#FFFFFF", insertbackground='white')
decrypt_entry1.grid(row=1, column=1, pady=10)

decrypt_btn = tk.Button(decrypt_box, text="Odszyfruj", command=decrypt, bg="#3E3E3E", fg="#FFFFFF")
decrypt_btn.grid(row=2, column=0, columnspan=2, pady=10)

decrypt_response = tk.Label(decrypt_box, text="", bg="#2D2D2D", fg="#00FF00")  # Green text for decrypted response
decrypt_response.grid(row=3, column=0, columnspan=2)

#ODPALA APLIKACJE
root.mainloop()
