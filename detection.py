import os
import wmi
from cryptography.fernet import Fernet
import tkinter

from tkinter import Button, Label, Tk, TkVersion,filedialog
my_key='key'
files='path'
c = wmi.WMI()
def check_for_key():
   for disk in c.Win32_LogicalDisk():
      if disk.VolumeName==my_key:
         return disk
def load_key(usbDisk):
    port= usbDisk.DeviceID
    try:
        print('trying to find key')
        with open(f'{port}\\encryptionKey.key','rb') as encryptKey:
            key=encryptKey.read()
            print('key found')
    except:
        print('key not found, creating a new key')
        key=Fernet.generate_key()
        with open(f'{port}\\encryptionKey.key','wb') as encryptKey:
            encryptKey.write(key)
            return key

def encryptFile(key,directory):
    files=os.listdr(directory)
    cipher=Fernet(key)
    global state 
    state='encrypted'
    for file in files:
        with open(f'{directory}\{file}','rb') as old:
            original=old.read()
            encrypted=cipher.encrypt(original)
            with open(f'{directory}\{file}','wb') as old:
              old.write(encrypted)

def decryptFile(key,directory):
    files=os.listdr(directory)
    global state
    cipher = Fernet(key)
    state='decrypted'
    for file in files:
      with open(f'{directory}\{file}','rb') as old:
         encrypted = old.read()
         decrypted=cipher.decrypt(encrypted)
         
         with open(f'{directory}\{file}','wb') as old:
           old.write(decrypted)


state = 'decrypted'

def toggle_encryption():
    disk = check_for_key()
    try:
        key = load_key(disk)
    except:
        print('No Key Available')
        return

    if disk is not None:
        global state
        current_state = 'decrypted'

        if current_state != state:
            decryptFile(key, files)
            state_label.config(text="State: Decrypted")
        else:
            current_state = 'encrypted'
            if current_state != state:
                encryptFile(key, files)
                state_label.config(text="State: Encrypted")


def select_directory():
    global files
    files = filedialog.askdirectory()
    directory_label.config(text=f"Selected Directory: {files}")


# Create the main window
root = Tk()
root.title("File Encryption GUI")

# Create and place GUI elements
select_button = Button(root, text="Select Directory", command=select_directory)
select_button.pack(pady=10)

directory_label = Label(root, text=f"Selected Directory: {files}")
directory_label.pack()

encrypt_button = Button(root, text="Toggle Encryption", command=toggle_encryption)
encrypt_button.pack(pady=10)

state_label = Label(root, text="State: Decrypted")
state_label.pack()

# Start the Tkinter event loop
root.mainloop()