import tkinter as tk
from tkinter import messagebox
import sqlite3

# ---------------- DATABASE ----------------
def connect_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            course TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_student():
    name = name_var.get()
    age = age_var.get()
    course = course_var.get()

    if name == "" or age == "" or course == "":
        messagebox.showerror("Error", "All fields are required")
        return

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
                   (name, age, course))
    conn.commit()
    conn.close()
    clear_fields()
    fetch_students()
    messagebox.showinfo("Success", "Student added successfully")

def fetch_students():
    listbox.delete(0, tk.END)
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        listbox.insert(tk.END, row)

def select_student(event):
    try:
        selected = listbox.get(listbox.curselection())
        id_var.set(selected[0])
        name_var.set(selected[1])
        age_var.set(selected[2])
        course_var.set(selected[3])
    except:
        pass

def update_student():
    if id_var.get() == "":
        messagebox.showerror("Error", "Select a student first")
        return

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE students
        SET name=?, age=?, course=?
        WHERE id=?
    """, (name_var.get(), age_var.get(), course_var.get(), id_var.get()))
    conn.commit()
    conn.close()
    fetch_students()
    clear_fields()
    messagebox.showinfo("Success", "Student updated successfully")

def delete_student():
    if id_var.get() == "":
        messagebox.showerror("Error", "Select a student first")
        return

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id_var.get(),))
    conn.commit()
    conn.close()
    fetch_students()
    clear_fields()
    messagebox.showinfo("Success", "Student deleted successfully")

def clear_fields():
    id_var.set("")
    name_var.set("")
    age_var.set("")
    course_var.set("")

# ---------------- GUI ----------------
connect_db()

root = tk.Tk()
root.title("Student Information Management System")
root.geometry("600x400")

# Variables
id_var = tk.StringVar()
name_var = tk.StringVar()
age_var = tk.StringVar()
course_var = tk.StringVar()

# Labels & Entries
tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=name_var).grid(row=0, column=1)

tk.Label(root, text="Age").grid(row=1, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=age_var).grid(row=1, column=1)

tk.Label(root, text="Course").grid(row=2, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=course_var).grid(row=2, column=1)

# Buttons
tk.Button(root, text="Add", width=12, command=insert_student).grid(row=3, column=0)
tk.Button(root, text="Update", width=12, command=update_student).grid(row=3, column=1)
tk.Button(root, text="Delete", width=12, command=delete_student).grid(row=4, column=0)
tk.Button(root, text="Clear", width=12, command=clear_fields).grid(row=4, column=1)

# Listbox
listbox = tk.Listbox(root, width=50)
listbox.grid(row=0, column=2, rowspan=6, padx=10)
listbox.bind("<<ListboxSelect>>", select_student)

fetch_students()

root.mainloop()
