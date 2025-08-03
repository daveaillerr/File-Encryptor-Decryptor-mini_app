import customtkinter
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import base64

# GUI
window = customtkinter.CTk()
window.geometry("600x500")
window.title("Encrypt & Decrypt Text Files")
window.resizable(False, False)
window.background_color = "#383838"

# ASSETS
def top_bar():

    top_bar_frame = customtkinter.CTkFrame(
        master = window,
        width=600, 
        height=117,
        corner_radius= 30,
        fg_color="#42484A",
    )
    top_bar_frame.pack()
    
    top_over = customtkinter.CTkFrame(
        master = window,
        width=600, 
        height=100,
        fg_color="#42484A", 
        corner_radius=0,
    )
    top_over.place(x=0, y=0, relwidth=1)

    header = customtkinter.CTkLabel(
        master = top_over,
        text="TEXT ENCRPTOR & DECRYPTOR",
        font=("Arial", 32, 'bold'),
        text_color="white",
        fg_color="transparent",
    )
    header.pack(pady=(25, 0))

    add_info = customtkinter.CTkLabel(
        master = top_over,
        text="SYMMETRIC ENCRYPTION",
        font=("Arial", 16),
        text_color="white",
        fg_color = "transparent",
    )
    add_info.pack()


# Upload File Function
upload = customtkinter.CTkLabel(
    window, 
       text="Upload text file: ",
      font=("Arial", 16, 'bold'),
)  
upload.place(x=52, y=135)

upload_label = customtkinter.CTkEntry(
    window,
    placeholder_text="Select a text file to encrypt or decrypt",
    font=("Arial", 14),
    text_color="#7C7C7C",
    width=390,
    height=36,
    corner_radius=10,
    fg_color="#D9D9D9",
)
upload_label.place(x=158, y=170)

upload_button = customtkinter.CTkButton(
    master = window,
    text="Browse",
    font=("Arial", 14, 'bold'),
    command=lambda: file_path(),
    width=105,
    height=36,
    corner_radius=10,
    fg_color="#0D54A6"
)
upload_button.place(x=52, y=170)

# File Dialog
def file_path():
     file_path = filedialog.askopenfilename(
        title="Select a text file",
        filetypes=(("All files", "*.*"), ("Text files", "*.txt"))
    )
     if file_path:
        upload_label.delete(0, 'end')  # Clear the entry field
        upload_label.insert(0, file_path)

# Secret Key 
key = customtkinter.CTkLabel(
    window,
    text = "Input Secret Key: ",
    font=("Arial", 16, 'bold'),
)
key.place(x=52, y=250)

key_input = customtkinter.CTkEntry(
    window,
    placeholder_text="Enter your secret key",
    font=("Arial", 14),
    text_color="#7C7C7C",
    width=495,
    height=36,
    corner_radius=10,
    fg_color="#D9D9D9",
)
key_input.place(x=52, y=285)

# Encryption Function
def encryption():
        if upload_label.get() == "" or upload_label.get() == "Select a file to encrypt or decrypt":
            messagebox.showerror("Error", "Please select a file to encrypt.")
            return
        
        if key_input.get() == "" or key_input.get() == "Enter your secret key":
            messagebox.showerror("Error", "Please enter a secret key.")
        else:
            key = key_input.get().encode()
            key_updated = base64.urlsafe_b64encode(key.ljust(32)[:32])  # Ensure key is 32 bytes
            f = Fernet(key_updated)
            try:
                with open(upload_label.get(), 'rb') as file:
                    original = file.read()
                    content_encrypted = f.encrypt(original)
                with open(upload_label.get() + '.encrypted', 'wb') as file_enc:
                    file_enc.write(content_encrypted)
                    messagebox.showinfo("Success", "File encrypted successfully!")
            except Exception as e:
                messagebox.showerror("Error", "Encryption failed. Please check the file and key.")

# Decryption Function
def decryption():
        if upload_label.get() == "" or upload_label.get() == "Select a file to encrypt or decrypt":
            messagebox.showerror("Error", "Please select a file to decrypt.")
            return
        
        if key_input.get() == "" or key_input.get() == "Enter your secret key":
            messagebox.showerror("Error", "Please enter a secret key.")
            return
        else:
            key = key_input.get().encode()
            key_updated = base64.urlsafe_b64encode(key.ljust(32)[:32])
            f = Fernet(key_updated)
            try:
                with open(upload_label.get(), 'rb') as file:
                    content_encrypted = file.read()
                    content_decrypted = f.decrypt(content_encrypted)
                with open(upload_label.get().replace('.encrypted', '.decrypted'), 'wb') as file_dec:
                    file_dec.write(content_decrypted)
                    messagebox.showinfo("Success", "File decrypted successfully!")
            except Exception as e:
                messagebox.showerror("Error", "Decryption failed. Please check the file and key.")

def enc_dnc_button():
    encrypt_button = customtkinter.CTkButton(
        window,
        text = "Encrypt",
        font=("Arial", 14, 'bold'),
        width=170,
        height=36,
        corner_radius=10,
        fg_color="#0D54A6",
        command=lambda: encryption()  # Call the encryption function
    )
    encrypt_button.place(x=52, y=383)

    decrypt_button = customtkinter.CTkButton(
        window,
        text = "Decrypt",
        font=("Arial", 14, 'bold'),
        width=170,
        height=36,
        corner_radius=10,
        fg_color="#0D54A6",
        command=lambda: decryption()  # Call the decryption function
    )
    decrypt_button.place(x=379, y=383)



top_bar()
enc_dnc_button()

window.mainloop()