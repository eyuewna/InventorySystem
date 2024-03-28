import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# idk pano iconnect :,DD
conn = sqlite3.connect('data.db')
cursor = conn.cursor()


# Functions for GUI
def logout():
    answer = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if answer:
        root.destroy()


# Select specific category
def handle_choice_click(choice):
    selected_choice.set(choice)

    tree.delete(*tree.get_children())

    if choice == "ALL MERCH":
        for item in data:
            tree.insert("", "end", values=item)
    else:
        for item in data:
            if item[0] == choice:
                tree.insert("", "end", values=item)



def add_item():
    category = category_entry.get()
    merch_id = merch_id_entry.get()
    merch_name = merch_name_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()

    # Check if the entered category is valid
    valid_categories = ["Albums", "Accessories", "Posters", "LightSticks", "Photocards", "Limited Edition"]
    if category not in valid_categories:
        messagebox.showerror("Error", "Invalid category. Please choose from: Albums, Accessories, Posters, LightSticks, Photocards, Limited Edition.")
        return

    # Check if the Merch ID already exists
    for child in tree.get_children():
        if tree.item(child, "values")[1] == merch_id:
            messagebox.showerror("Error", "Merch ID already exists.")
            return

    tree.insert("", "end", values=(category, merch_id, merch_name, price, quantity))


def delete_item():
    # Retrieve Merch ID and Merch Name from entry widgets
    merch_id_to_delete = merch_id_entry.get()
    merch_name_to_delete = merch_name_entry.get()

    # Search for the item in the Treeview
    found = False
    for child in tree.get_children():
        values = tree.item(child, "values")
        if values[1] == merch_id_to_delete and values[2] == merch_name_to_delete:
            tree.delete(child)
            found = True
            break

    # If the item is not found, show an error message
    if not found:
        messagebox.showerror("Error", "Item not found in the inventory.")

def update_item():
    # Retrieve Merch ID to identify the item to be updated
    merch_id_to_update = merch_id_entry.get()

    # Search for the item in the Treeview
    found = False
    for child in tree.get_children():
        values = tree.item(child, "values")
        if values[1] == merch_id_to_update:
            found = True
            break

    # , show a popup box for updating
    if found:
        update_window = tk.Toplevel(root)
        update_window.title("Update Item")

        # Function to handle update action
        def confirm_update():
            updated_category = category_var.get()
            updated_merch_name = merch_name_var.get()
            updated_price = price_var.get()
            updated_quantity = quantity_var.get()

            # Update values in the Treeview
            tree.item(child, values=(updated_category, values[1], updated_merch_name, updated_price, updated_quantity))
            update_window.destroy()

        # Cancel update action
        def cancel_update():
            update_window.destroy()

        # Labels and entry widgets for updating
        category_label = tk.Label(update_window, text="Category:")
        category_label.grid(row=0, column=0)
        category_var = tk.StringVar()
        category_entry = tk.Entry(update_window, textvariable=category_var)
        category_entry.grid(row=0, column=1)

        merch_name_label = tk.Label(update_window, text="Merch Name:")
        merch_name_label.grid(row=1, column=0)
        merch_name_var = tk.StringVar()
        merch_name_entry = tk.Entry(update_window, textvariable=merch_name_var)
        merch_name_entry.grid(row=1, column=1)

        price_label = tk.Label(update_window, text="Price:")
        price_label.grid(row=2, column=0)
        price_var = tk.StringVar()
        price_entry = tk.Entry(update_window, textvariable=price_var)
        price_entry.grid(row=2, column=1)

        quantity_label = tk.Label(update_window, text="Quantity:")
        quantity_label.grid(row=3, column=0)
        quantity_var = tk.StringVar()
        quantity_entry = tk.Entry(update_window, textvariable=quantity_var)
        quantity_entry.grid(row=3, column=1)

        # Update and Cancel buttons
        update_button = tk.Button(update_window, text="Update", command=confirm_update)
        update_button.grid(row=4, column=0, pady=10)

        cancel_button = tk.Button(update_window, text="Cancel", command=cancel_update)
        cancel_button.grid(row=4, column=1, pady=10)
    else:
        messagebox.showerror("Error", "Item not found in the inventory.")
 
def search_items():
    # Retrieve search criteria from entry widgets
    search_category = category_entry.get()
    search_merch_id = merch_id_entry.get()
    search_merch_name = merch_name_entry.get()
    search_price = price_entry.get()
    search_quantity = quantity_entry.get()

    # Filter items in the Treeview based on search criteria
    for child in tree.get_children():
        values = tree.item(child, "values")
        category_match = search_category.lower() in values[0].lower() or search_category == ""
        merch_id_match = search_merch_id.lower() in values[1].lower() or search_merch_id == ""
        merch_name_match = search_merch_name.lower() in values[2].lower() or search_merch_name == ""
        price_match = search_price.lower() in values[3].lower() or search_price == ""
        quantity_match = search_quantity.lower() in values[4].lower() or search_quantity == ""

        # Show only items that match all search criteria
        if category_match and merch_id_match and merch_name_match and price_match and quantity_match:
            tree.item(child, open=True)
            tree.selection_add(child)
        else:
            tree.item(child, open=False)
            tree.selection_remove(child)
            
# Clear all entry 
def clear_entries():
    category_entry.delete(0, tk.END)
    merch_id_entry.delete(0, tk.END)
    merch_name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)

# Create main window
root = tk.Tk()
root.title("KPOP INVENTORY SYSTEM")
root.geometry("1920x1080+0+0")


# Header Frame
header_frame = tk.Frame(root, bg="#104A99", width=1920, height=100)
header_frame.pack_propagate(0)
header_frame.pack(side="top", fill="x")

# Logo Image
logo_image = tk.PhotoImage(file="logo.png").subsample(2)
logo_label = tk.Label(header_frame, image=logo_image, bg="#104A99")
logo_label.pack(side="left", padx=(10, 0), pady=10)

# Logout Button and Username
user_image = tk.PhotoImage(file="user.png").subsample(3)
user_label = tk.Label(header_frame, image=user_image, bg="#104A99")
user_label.pack(side="right", pady=10)

username_label = tk.Label(header_frame, text="Euna Angeles", font=("Arial", 16, "bold"), bg="#104A99", fg="white")
username_label.place(x=1310, y=25)

logout_button = tk.Button(header_frame, font=("Arial", 10), bg="#ff94c4", text="Logout", command=logout)
logout_button.place(x=1390, y=57)


# navigation frame
nav_frame = tk.Frame(root, bg="white", width=1720, height=55)
nav_frame.pack(side="top", fill="x", pady=(0, 0))

# Categories Title
label1 = tk.Label(nav_frame, text="CATEGORIES", font=("Cooper Black", 20), bg="white", fg="#ff94c4")
label1.place(x=10, y=10)

# Search button
search_button_image = tk.PhotoImage(file="search.png").subsample(4)
search_button = tk.Button(nav_frame, image=search_button_image, bg="white", bd=0, command=search_items)
search_button.place(x=1280, y=0)

# update button
update_button_image = tk.PhotoImage(file="update.png").subsample(4)
update_button = tk.Button(nav_frame, image=update_button_image, bg="white", bd=0, command=update_item)
update_button.place(x=1332, y=0)

# Add button
add_button_image = tk.PhotoImage(file="add.png").subsample(4)
add_button = tk.Button(nav_frame, image=add_button_image, bg="white", bd=0, command=add_item)
add_button.place(x=1380, y=0)

# Trash button
trash_button_image = tk.PhotoImage(file="trash.png").subsample(4)
trash_button = tk.Button(nav_frame, image=trash_button_image, bg="white", bd=0, command=delete_item)
trash_button.place(x=1440, y=0)

# View categories Frame
view_frame = tk.Frame(root, width=200, height=1080) 
view_frame.pack(side="left", fill="y")

# Category choices
choices = ["ALL MERCH", "Albums", "Accessories", "Posters", "LightSticks", "Photocards", "Limited Edition"]
selected_choice = tk.StringVar(value="ALL MERCH")
button_width = 20 

# List to hold button objects
choice_buttons = []
for i, choice in enumerate(choices):
    choice_button = tk.Button(view_frame, text=choice, bg="#AA336A" if selected_choice.get() == choice else "#ff94c4", fg="white", font=("Helvetica", 16, "bold"), width=button_width, command=lambda choice=choice: handle_choice_click(choice))
    choice_button.place(x=0, y=90*i, width=200, height=90)
    choice_buttons.append(choice_button)

    
# Center bg image
center_frame = tk.Frame(root, bg="light blue", width=1920, height=900)
center_frame.pack_propagate(0)
center_frame.pack(side="top", fill="both", expand=True)

# Entry Frame for Inputs
entry_frame = tk.Frame(center_frame, bg="light blue", width=1520, height=50)
entry_frame.pack(side="top", fill="x", padx=50, pady=(20, 10)) 

# Input Boxes
category_label = tk.Label(entry_frame, text="Category:", font=("Cooper Black", 14), bg="light blue", fg="#104A99")
category_label.grid(row=0, column=0, padx=10)

category_entry = tk.Entry(entry_frame, font=("Arial", 12), bd=2, width=15) 
category_entry.grid(row=0, column=1, padx=10)

merch_id_label = tk.Label(entry_frame, text="Merch ID:", font=("Cooper Black", 14), bg="light blue", fg="#104A99")
merch_id_label.grid(row=0, column=2, padx=10)

merch_id_entry = tk.Entry(entry_frame, font=("Arial", 12), bd=2, width=10) 
merch_id_entry.grid(row=0, column=3, padx=10)

merch_name_label = tk.Label(entry_frame, text="Merch Name:", font=("Cooper Black", 14), bg="light blue", fg="#104A99")
merch_name_label.grid(row=0, column=4, padx=10)

merch_name_entry = tk.Entry(entry_frame, font=("Arial", 12), bd=2, width=15) 
merch_name_entry.grid(row=0, column=5, padx=10)

price_label = tk.Label(entry_frame, text="Price:", font=("Cooper Black", 14), bg="light blue", fg="#104A99")
price_label.grid(row=0, column=6, padx=10)

price_entry = tk.Entry(entry_frame, font=("Arial", 12), bd=2, width=8)  
price_entry.grid(row=0, column=7, padx=10)

quantity_label = tk.Label(entry_frame, text="Quantity:", font=("Cooper Black", 14), bg="light blue", fg="#104A99")
quantity_label.grid(row=0, column=8, padx=10)

quantity_entry = tk.Entry(entry_frame, font=("Arial", 12), bd=2, width=8) 
quantity_entry.grid(row=0, column=9, padx=10)

# Treeview
tree_frame = tk.Frame(center_frame, bg="white", width=1520, height=800)  
tree_frame.pack_propagate(0)
tree_frame.pack(side="top", fill="both", padx=50, pady=(10, 100)) 


# Clear all entry text button
clear_button = tk.Button(center_frame, text="Clear all Entry", font=("Arial", 10), bg="white", bd=0, command=clear_entries)
clear_button.place(x=50, y=600)  


tree = ttk.Treeview(tree_frame, columns=("Category", "Merch ID", "Merch Name", "Price", "Quantity"), show="headings")
tree.column("Category", width=200)
tree.column("Merch ID", width=150, anchor='center')
tree.column("Merch Name", width=400)
tree.column("Price", width=100, anchor='center')
tree.column("Quantity", width=100, anchor='center')
tree.heading("Category", text="Category")
tree.heading("Merch ID", text="Merch ID")
tree.heading("Merch Name", text="Merch Name")
tree.heading("Price", text="Price")
tree.heading("Quantity", text="Quantity")
data = [
    ("Albums", "#001", "Album A", "P2000", 10),
    ("Albums", "#002", "Album B", "P2500", 5),
    ("Posters", "#003", "Poster A", "P1000", 20),
]

for item in data:
    tree.insert("", "end", values=item)

#style for treeview
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 16, "bold"))

tree.pack(expand=True, fill="both")

root.mainloop()
