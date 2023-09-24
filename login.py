import tkinter as tk
import mysql.connector
from tkinter import messagebox
import subprocess



mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="prijava_ispita"
)

mycursor = mydb.cursor()

def login():
    korisnik = username_entry.get()
    lozinka = password_entry.get()

    query = "SELECT * FROM nalozi WHERE korisnik = %s AND lozinka = %s"
    mycursor.execute(query, (korisnik, lozinka))
    result = mycursor.fetchone()

    if result:
        window.destroy()
        open_menu()
    else:
        messagebox.showerror("Login Failed", "Uneli ste pogresnu sifru ili ime")

def open_menu():
    try:
        subprocess.run(["python", "main.py"])
    except Exception as e:
        print(f"Error: {e}")


window = tk.Tk()
window.title("Login Form")

frame = tk.Frame(window)
frame.pack()


username_label = tk.Label(frame, text="Korisnik")
username_label.grid(row = 0, column = 0, padx = 35, pady = 15)
username_entry = tk.Entry(frame)
username_entry.grid(row = 0, column = 1, padx = 35, pady = 15)


password_label = tk.Label(frame, text="Lozinka")
password_label.grid(row = 1, column = 0, padx = 35, pady = 15)
password_entry = tk.Entry(frame, show="*")
password_entry.grid(row = 1, column = 1, padx = 35, pady = 15)


login_button = tk.Button(frame, text="Login", command=login)
login_button.grid(row = 2, column = 0, padx = 35, pady = 15)

hint_label = tk.Label(frame, text="(user123, sifra123)")
hint_label.grid(row = 2, column = 1, padx = 35, pady = 20)


window.mainloop()