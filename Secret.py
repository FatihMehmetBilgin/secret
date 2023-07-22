import tkinter
from tkinter import messagebox
from PIL import ImageTk,Image
import os
import base64

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

window= tkinter.Tk()
window.config(padx=30 ,pady=30)
window.title("SecretFile")

## image ##
img = Image.open("example.jpg")
img = img.resize((150, 150))
img = ImageTk.PhotoImage(img)
panel= tkinter.Label(window,image=img)

## save and encrypt ##
def clickButton1(): 
    nameFile= entry1.get()
    secretText= text1.get("1.0",tkinter.END)
    secretKey= entry2.get()
    
    if len(nameFile)==0 or len(secretText)==0 or len(secretKey)==0:
        messagebox.showerror(title="ERROR!", message="Please enter all info.")
    
    else:    
        encryption= encode(secretKey,secretText)
        try:
            with open(f'{nameFile}.txt','a') as data_file: 
                data_file.write(f'\n{nameFile}\n{encryption}')

        except FileNotFoundError:
            with open(f'{nameFile}.txt','w') as data_file:
                data_file.write(f'\n{nameFile}\n{encryption}')
        finally:
            entry1.delete(0,tkinter.END)
            text1.delete("1.0",tkinter.END)
            entry2.delete(0,tkinter.END)



    
    
## decrypt
def clickButton2():
    encryption=text1.get("1.0",tkinter.END)
    secretKey=entry2.get()
    if len(encryption)== 0 or len(secretKey)==0:
        messagebox.showerror(title="Error!", message="please enter all information")
    else:

        try:
            decrypted_message = decode(secretKey,encryption)

            text1.delete("1.0",tkinter.END)
            text1.insert("1.0", decrypted_message)
        except:
            messagebox.showinfo(title="Error!", message="Please make sure of encrypted info.")



    






FONT=("Arial",10,"bold")

title1=tkinter.Label(text="Enter your title",font=FONT)
title2=tkinter.Label(text="Enter your secret",font=FONT)
title3= tkinter.Label(text=" Enter master key",font=FONT)
button1= tkinter.Button(text="Save & Encrypt",command=clickButton1)
button2= tkinter.Button(text="Decrypt",command=clickButton2)
entry1= tkinter.Entry(width=35)
entry2= tkinter.Entry(width=35)
text1 = tkinter.Text(width=40)


panel.pack(pady=10)
title1.pack(pady=10)
entry1.pack()
title2.pack(pady=10)
text1.pack()
title3.pack(pady=10)
entry2.pack()
button1.pack(pady=10)
button2.pack()

window.mainloop()