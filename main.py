import tkinter as tk
import mysql.connector
import subprocess
import pandas as pd
import sys

venv_path = sys.prefix

print("Virtual Environment Path:", venv_path)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="prijava_ispita"
)

# Vracanje na login
def log_out():
    try:
        window.destroy()
        subprocess.run(["python", "login.py"])
    except Exception as e:
        print(f"Error: {e}")

window = tk.Tk()
window.title("Prijava ispita")

frame = tk.Frame(window)
frame.pack()

# Frame za prikaz naloga i opcija za log out (gornji deo)
header_frame = tk.Frame(frame, bg='#D3D3D3', width=300, height=50)
header_frame.grid(row=0, column=0, sticky='nsew')

header_frame.grid_propagate(0)

label = tk.Label(header_frame, bg="#D3D3D3")
label.grid(row=0, column=0, columnspan=2)

log_out_dugme = tk.Button(header_frame, text="Log out", command=log_out)
log_out_dugme.grid(row=0, column=3, sticky="e")

username_label = tk.Label(header_frame, bg="#D3D3D3", text="User123", width=16, font=('Arial', 12, 'bold'))
username_label.grid(row=0, column=1, pady = 15, sticky="w")

# Frame za unos podataka (leva strana)
unos_frame = tk.LabelFrame(frame, text="Unos podataka studenta")
unos_frame.grid(row=1, column=0)

unos_studenta_frame = tk.LabelFrame(unos_frame)
unos_studenta_frame.grid(row = 0, column = 0)

def insert_student():
    ime = entry_ime.get()
    student_index = entry_index.get()
    prijavljeni_ispiti = "nema"
    mycursor = mydb.cursor()
    sql = "INSERT INTO studenti (ime, student_index, prijavljeni_ispiti) VALUES (%s, %s, %s)"
    mycursor.execute(sql, (ime, student_index, prijavljeni_ispiti))
    mydb.commit()

    print("Uspesno su uneti podaci ucenika")

# Funkcija za stvaranje excel fajla
def excel_izvoz():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM studenti")
    data = mycursor.fetchall()
    columns = ["id", "ime", "student_index", "prijavljeni_ispiti"]
    df = pd.DataFrame(data, columns=columns)
    excel_file = "studenti.xlsx"
    df.to_excel(excel_file, index=False, engine='openpyxl')
    print(f"Podatak uspesno izvozen kao {excel_file}")


label_ime = tk.Label(unos_studenta_frame, text="Ime:")
label_ime.grid(row=0, column=0, padx=10, pady=10)

entry_ime = tk.Entry(unos_studenta_frame, width=30)
entry_ime.grid(row=0, column=1, padx=10, pady=10)

label_index = tk.Label(unos_studenta_frame, text="Index:")
label_index.grid(row=1, column=0, padx=10, pady=10)

entry_index = tk.Entry(unos_studenta_frame, width=10)
entry_index.grid(row=1, column=1, padx=10, pady=10)

insert_button = tk.Button(unos_studenta_frame, text="Insert", command=insert_student)
insert_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Frame za tabelu
tabela_frame = tk.LabelFrame(unos_frame)
tabela_frame.grid(row=1, column = 0)

excel_dugme = tk.Button(unos_frame, text="Prikaz tabele kao .xlsx", command=excel_izvoz)
excel_dugme.grid(row = 2, column = 0)



class Table:

    def __init__(self, root, data):
        self.total_rows = len(data)
        self.total_columns = len(data[0])

        for i in range(self.total_rows):
            for j in range(self.total_columns):
                self.e = tk.Entry(root, width=15, fg='blue', font=('Arial', 12, 'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert(tk.END, data[i][j])

# Create a MySQL database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="prijava_ispita"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM studenti")
data = mycursor.fetchall()

t = Table(tabela_frame, data)


# FRAME ZA PRIJAVU ISPITA (desna strana)
def pretraga():
    index = index_entry.get()
    mycursor = mydb.cursor()
    sql = "SELECT ime, prijavljeni_ispiti FROM studenti WHERE student_index = %s"
    mycursor.execute(sql, (index,))
    myresult = mycursor.fetchone()
    if myresult:
        naziv_label.config(text=myresult[0])
        predmeti_listbox.delete(0, tk.END)
    if myresult[1] is not None:
        courses = myresult[1].split(', ')
        for course in courses:
            predmeti_listbox.insert(tk.END, course)
    else:
        naziv_label.config(text="Nije pronadjen student")
        predmeti_listbox.delete(0, tk.END)
    return myresult[0]


# Funkcija prilikom pritiska dugme Prijava
def prijava():
    ime = pretraga()
    if ime is not None:
        sortirani_predmeti = ', '.join(odabrani_predmeti)
        mycursor = mydb.cursor()
        sql = "UPDATE studenti SET prijavljeni_ispiti = %s WHERE ime = %s"
        mycursor.execute(sql, (sortirani_predmeti, ime))
        mydb.commit()
    odabrani_predmeti.clear()
    reset_checkbuttons()
    pretraga()


odabrani_predmeti = []
def biranje_predmeta(predmet):
    odabrani_predmeti.append(predmet)
def matematika_callback():
    biranje_predmeta("matematika")
def info_sys_callback():
    biranje_predmeta("informacioni sistemi")
def statistika_callback():
    biranje_predmeta("statistika")

def reset_checkbuttons():
    matematika_cb.deselect()
    info_sys_cb.deselect()
    statistika_cb.deselect()

def brisanje():
    ime = pretraga()
    mycursor = mydb.cursor()
    sql = "DELETE FROM studenti WHERE ime = %s"
    mycursor.execute(sql, (ime,))
    mydb.commit()


# Window i Frame
prijava_ispita_frame = tk.LabelFrame(frame, text = "Prijava ispita")
prijava_ispita_frame.grid(row = 1, column=1)

# Frame za unos podataka
unos_podataka_frame = tk.LabelFrame(prijava_ispita_frame)
unos_podataka_frame.grid(row = 0, column = 0, sticky='w')

index_label = tk.Label(unos_podataka_frame, text="Index studenta")
index_label.grid(row = 0, column = 0, padx= 10, pady = 10)
index_entry = tk.Entry(unos_podataka_frame)
index_entry.grid(row= 0, column= 1, padx= 10, pady = 10)
pretrage_dugme = tk.Button(unos_podataka_frame, text="Pretraga", command=pretraga)
pretrage_dugme.grid(row= 0, column= 2, padx= 10, pady = 10)
brisanje_dugme = tk.Button(unos_podataka_frame, text="Brisanje", command=brisanje)
brisanje_dugme.grid(row = 0, column = 3, padx = 10, pady =10)


# Prikaz frame
prikaz_prijava_frame = tk.LabelFrame(prijava_ispita_frame)
prikaz_prijava_frame.grid(row=1, column=1, padx=10, pady=10, sticky = 'w')

# Ime i prezime
naziv_label = tk.Label(prikaz_prijava_frame, bg="grey", text="", width=16)
naziv_label.grid(row = 0, column = 0, sticky = 'w')

# Listbox
predmeti_listbox = tk.Listbox(prikaz_prijava_frame, selectmode=tk.MULTIPLE)
predmeti_listbox.grid(row=2, column=0)





# Frame za prikaz prijavljenog studenta i dugme za prijavu
predmeti_frame = tk.LabelFrame(prijava_ispita_frame, text="Predmeti za polaganje")
predmeti_frame.grid(row = 1, column = 0, sticky = 'w')

prijava_dugme = tk.Button(predmeti_frame, text="Prijava", command=prijava)
prijava_dugme.grid(row= 0, column= 4, padx= 20, pady = 20)

matematika_cb = tk.Checkbutton(predmeti_frame, text="matematika", command=matematika_callback)
matematika_cb.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'w')
info_sys_cb = tk.Checkbutton(predmeti_frame, text="Informacioni sistemi", command=info_sys_callback)
info_sys_cb.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'w')
statistika_cb = tk.Checkbutton(predmeti_frame, text="statistika", command=statistika_callback)
statistika_cb.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'w')



window.mainloop()