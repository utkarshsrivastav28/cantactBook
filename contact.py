import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# ---------------- Contact Book Logic ----------------
CONTACTS_FILE = "contacts.json"

contacts = {}

def load_contacts():
    global contacts
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as f:
            contacts = json.load(f)
    else:
        contacts = {}

def save_contacts():
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if not name:
        messagebox.showwarning("Error", "Name is required!")
        return

    contacts[name] = {"phone": phone, "email": email}
    refresh_list()
    save_contacts()
    clear_entries()

def edit_contact():
    selected = contact_list.curselection()
    if not selected:
        messagebox.showwarning("Error", "Select a contact to edit!")
        return
    name = contact_list.get(selected)
    new_name = simpledialog.askstring("Edit Name", "Enter new name:", initialvalue=name)
    if new_name:
        contacts[new_name] = contacts.pop(name)
        refresh_list()
        save_contacts()

def delete_contact():
    selected = contact_list.curselection()
    if not selected:
        messagebox.showwarning("Error", "Select a contact to delete!")
        return
    name = contact_list.get(selected)
    if messagebox.askyesno("Confirm Delete", f"Delete contact {name}?"):
        contacts.pop(name)
        refresh_list()
        save_contacts()

def search_contact():
    query = search_entry.get().lower()
    contact_list.delete(0, tk.END)
    for name in contacts:
        if query in name.lower() or query in contacts[name]["phone"] or query in contacts[name]["email"]:
            contact_list.insert(tk.END, name)

def refresh_list():
    contact_list.delete(0, tk.END)
    for name in sorted(contacts.keys()):
        contact_list.insert(tk.END, name)

def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

def show_contact_details(event):
    selected = contact_list.curselection()
    if selected:
        name = contact_list.get(selected)
        details = contacts[name]
        phone_var.set(details["phone"])
        email_var.set(details["email"])

# ---------------- GUI ----------------
root = tk.Tk()
root.title("📇 Contact Book")
root.geometry("600x500")
root.config(bg="white")

# Left frame: list of contacts
left_frame = tk.Frame(root, bg="white")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=True)

tk.Label(left_frame, text="Contacts", font=("Arial", 14, "bold"), bg="white").pack(pady=5)

search_entry = tk.Entry(left_frame, font=("Arial", 12))
search_entry.pack(pady=5, fill=tk.X)
search_btn = tk.Button(left_frame, text="Search", command=search_contact, bg="lightblue")
search_btn.pack(pady=5, fill=tk.X)

contact_list = tk.Listbox(left_frame, font=("Arial", 12))
contact_list.pack(pady=5, fill=tk.BOTH, expand=True)
contact_list.bind("<<ListboxSelect>>", show_contact_details)

# Right frame: contact details
right_frame = tk.Frame(root, bg="white")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)

tk.Label(right_frame, text="Name:", font=("Arial", 12), bg="white").pack(pady=5)
name_entry = tk.Entry(right_frame, font=("Arial", 12))
name_entry.pack(pady=5, fill=tk.X)

tk.Label(right_frame, text="Phone:", font=("Arial", 12), bg="white").pack(pady=5)
phone_entry = tk.Entry(right_frame, font=("Arial", 12))
phone_entry.pack(pady=5, fill=tk.X)

tk.Label(right_frame, text="Email:", font=("Arial", 12), bg="white").pack(pady=5)
email_entry = tk.Entry(right_frame, font=("Arial", 12))
email_entry.pack(pady=5, fill=tk.X)

phone_var = tk.StringVar()
email_var = tk.StringVar()
tk.Label(right_frame, text="Phone: ", font=("Arial", 12), bg="white").pack(pady=5)
tk.Label(right_frame, textvariable=phone_var, font=("Arial", 12), bg="white").pack()
tk.Label(right_frame, text="Email: ", font=("Arial", 12), bg="white").pack(pady=5)
tk.Label(right_frame, textvariable=email_var, font=("Arial", 12), bg="white").pack()

# Buttons
btn_frame = tk.Frame(right_frame, bg="white")
btn_frame.pack(pady=10, fill=tk.X)
tk.Button(btn_frame, text="Add", command=add_contact, bg="lightgreen").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Edit", command=edit_contact, bg="orange").grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_contact, bg="tomato").grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Clear Fields", command=clear_entries, bg="lightblue").grid(row=0, column=3, padx=5)

# Load contacts and refresh list
load_contacts()
refresh_list()

root.mainloop()
