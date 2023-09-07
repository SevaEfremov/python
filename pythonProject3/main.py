#pip install PyMySQL
import pymysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

#connection for phpmyadmin
def connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='buD15rate',
        db='student_db',
    )
    return conn

def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)

    for array in read():
        my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")

    my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))
    my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20)

root = Tk()
root.title("DataBase.Manage")
my_tree = ttk.Treeview(root)
root.geometry('600x500')

ph1 = tk.StringVar()
ph2 = tk.StringVar()
ph3 = tk.StringVar()
ph4 = tk.StringVar()
ph5 = tk.StringVar()

def setph(word, num):
    if num == 1:
        ph1.set(word)
    if num == 2:
        ph2.set(word)
    if num == 3:
        ph3.set(word)
    if num == 4:
        ph4.set(word)
    if num == 5:
        ph5.set(word)
def read():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM moba")
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def add():
    character = str(characterEntry.get())
    role = str(roleEntry.get())
    lvl = str(lvlEntry.get())
    vs = str(vsEntry.get())

    if (character == "" or character == " ") or (role == "" or role == " ") or (lvl == "" or lvl == " ") or (vs == "" or vs == " "):
        messagebox.showinfo("Error", "Please fill up the blank entry")
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO moba VALUES('"+character+"', '"+role+"', '"+lvl+"', '"+vs+"') ")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Character already exist")
            return

    refreshTable()

def delete():
    decision = messagebox.askquestion("Warning!!", "Delete the selected data?")
    if decision != "yes":
        return
    else:
        selected_item = my_tree.selection()[0]
        deleteData = str(my_tree.item(selected_item)['value'][0])
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM moba WHERE Character='"+str(deleteData)+"'")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Sorry an error occured")
            return

        refreshTable()

# idEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable=ph1)
characterEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable=ph2)
roleEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable=ph3)
lvlEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable=ph4)
vsEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable=ph5)

addBtn = Button (root, text="Добавить", bd=5, command=add)
deleteBtn = Button(root, text="Удалить", bd=5, command=delete)

addBtn.grid(column=0, row=25)
deleteBtn.grid(column=3, row=25)

my_tree['columns'] = ["Character", "Role", "Lvl", "Vs"]
my_tree.column("#0", width=0, stretch=NO)
# my_tree.column("id", anchor=W, width=130)
my_tree.column("Character", anchor=W, width=130)
my_tree.column("Role", anchor=W, width=130)
my_tree.column("Lvl", anchor=W, width=130)
my_tree.column("Vs", anchor=W, width=130)

# my_tree.heading("id", text="ID", anchor=W)
my_tree.heading("Character", text="Character name", anchor=W)
my_tree.heading("Role", text="Role in game", anchor=W)
my_tree.heading("Lvl", text="Character's level", anchor=W)
my_tree.heading("Vs", text="Who verses you", anchor=W)

refreshTable()

root.mainloop()