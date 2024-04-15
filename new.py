import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from PIL import Image, ImageTk

# Establish a connection to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["GadaElectronics_Management"]
collection = db["Items"]

def view_items():
    result_text.delete(1.0, tk.END)  # Clear previous data
    documents = collection.find()

    # Display header
    header = "{:<20}{:<20}{:<20}{:<20}{:<20}{:<20}\n".format("Category", "Price", "Company", "Model", "Quantity",
                                                             "Total Price")
    result_text.insert(tk.END, header)
    result_text.insert(tk.END, "-" * 115 + "\n")

    # Display document data
    for doc in documents:
        category = doc["category"]
        price = doc["price"]
        company = doc["company"]
        model = doc["model"]
        quantity = doc["quantity"]
        total_price = price * quantity if price != 0 else 0
        line = f"{category:<20}{price:<20}{company:<20}{quantity:<20}{model:<20}{total_price:<20}\n"
        result_text.insert(tk.END, line)
        result_text.insert(tk.END, "-" * 115 + "\n")


def show_items():
    result_text.delete(1.0, tk.END)  # Clear previous data
    documents = collection.find()

    # Display header
    header = "{:<20}{:<20}{:<20}{:<20}{:<20}{:<20}\n".format("Category", "Price", "Company", "Quantity", "Model",
                                                             "Total Price")
    result_text.insert(tk.END, header)
    result_text.insert(tk.END, "-" * 115 + "\n")

    # Display document data
    for doc in documents:
        category = doc["category"]
        price = doc["price"]
        company = doc["company"]
        quantity = doc["quantity"]
        model = doc["model"]
        total_price = price * quantity
        line = f"{category:<20}{price:<20}{company:<20}{quantity:<20}{model:<20}{total_price:<20}\n"
        result_text.insert(tk.END, line)
        result_text.insert(tk.END, "-" * 115 + "\n")


def view_by_category():
    category = category_filter_entry.get()
    result_text.delete(1.0, tk.END)  # Clear previous data

    # Aggregate query to filter items by category
    pipeline = [
        {"$match": {"category": category}},
        {"$project": {"category": 1, "price": 1, "company": 1, "quantity": 1, "model": 1,
                      "total_price": {"$multiply": ["$price", "$quantity"]}}},
        {"$project": {"category": 1, "price": 1, "company": 1, "quantity": 1, "model": 1,
                      "total_price": {"$cond": [{"$eq": ["$price", 0]}, 0, "$total_price"]}}},
        {"$sort": {"category": 1}}
    ]

    documents = collection.aggregate(pipeline)

    # Display header
    header = "{:<20}{:<20}{:<20}{:<20}{:<20}{:<20}\n".format("Category", "Price", "Company", "Quantity", "Model",
                                                             "Total Price")
    result_text.insert(tk.END, header)
    result_text.insert(tk.END, "-" * 115 + "\n")

    # Display document data
    for doc in documents:
        category = doc["category"]
        price = doc["price"]
        company = doc["company"]
        quantity = doc["quantity"]
        model = doc["model"]
        total_price = doc["total_price"]
        line = f"{category:<20}{price:<20}{company:<20}{quantity:<20}{model:<20}{total_price:<20}\n"
        result_text.insert(tk.END, line)
        result_text.insert(tk.END, "-" * 115 + "\n")


def view_by_company():
    company = company_filter_entry.get()
    result_text.delete(1.0, tk.END)  # Clear previous data

    # Aggregate query to filter items by company
    pipeline = [
        {"$match": {"company": company}},
        {"$project": {"category": 1, "price": 1, "company": 1, "quantity": 1, "model": 1,
                      "total_price": {"$multiply": ["$price", "$quantity"]}}},
        {"$project": {"category": 1, "price": 1, "company": 1, "quantity": 1, "model": 1,
                      "total_price": {"$cond": [{"$eq": ["$price", 0]}, 0, "$total_price"]}}},
        {"$sort": {"category": 1}}
    ]

    documents = collection.aggregate(pipeline)

    # Display header
    header = "{:<20}{:<20}{:<20}{:<20}{:<20}{:<20}\n".format("Category", "Price", "Company", "Quantity", "Model",
                                                             "Total Price")
    result_text.insert(tk.END, header)
    result_text.insert(tk.END, "-" * 115 + "\n")

    # Display document data
    for doc in documents:
        category = doc["category"]
        price = doc["price"]
        company = doc["company"]
        quantity = doc["quantity"]
        model = doc["model"]
        total_price = doc["total_price"]
        line = f"{category:<20}{price:<20}{company:<20}{quantity:<20}{model:<20}{total_price:<20}\n"
        result_text.insert(tk.END, line)
        result_text.insert(tk.END, "-" * 115 + "\n")

def add_item():
    category = category_add_entry.get()
    price = float(price_add_entry.get())
    company = company_add_entry.get()
    model = model_add_entry.get()
    quantity = int(quantity_add_entry.get())

    item = {
        "category": category,
        "price": price,
        "company": company,
        "model": model,
        "quantity": quantity,
    }

    collection.insert_one(item)
    messagebox.showinfo("Success", "Item added successfully.")
    clear_entries("add")


def update_item():
    category = category_update_entry.get()
    company = company_update_entry.get()
    model = model_update_entry.get()

    new_price = float(new_price_update_entry.get())
    new_company = new_company_update_entry.get()
    new_model = new_model_update_entry.get()
    new_quantity = int(new_quantity_update_entry.get())

    update_data = {
        "$set": {
            "price": new_price,
            "company": new_company,
            "model": new_model,
            "quantity": new_quantity
        }
    }

    # Update item based on category, company, and model
    collection.update_one({"category": category, "company": company, "model": model}, update_data)
    messagebox.showinfo("Success", "Item updated successfully.")
    clear_entries("update")


def delete_item():
    category = category_delete_entry.get()
    company = company_delete_entry.get()
    model = model_delete_entry.get()

    # Delete item based on category, company, and model
    collection.delete_one({"category": category, "company": company, "model": model})
    messagebox.showinfo("Success", "Item deleted successfully.")
    clear_entries("delete")


def clear_entries(operation):
    if operation == "add":
        category_add_entry.delete(0, tk.END)
        price_add_entry.delete(0, tk.END)
        company_add_entry.delete(0, tk.END)
        model_add_entry.delete(0, tk.END)
        quantity_add_entry.delete(0, tk.END)
    elif operation == "update":
        category_update_entry.delete(0, tk.END)
        company_update_entry.delete(0, tk.END)
        model_update_entry.delete(0, tk.END)
        new_price_update_entry.delete(0, tk.END)
        new_company_update_entry.delete(0, tk.END)
        new_model_update_entry.delete(0, tk.END)
        new_quantity_update_entry.delete(0, tk.END)
    elif operation == "delete":
        category_delete_entry.delete(0, tk.END)
        company_delete_entry.delete(0, tk.END)
        model_delete_entry.delete(0, tk.END)

def close_connection():
    client.close()
    root.destroy()

root = tk.Tk()
root.title("Store Management System")

# Frames
add_frame = tk.LabelFrame(root)
add_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")
update_frame = tk.LabelFrame(root)
update_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")
delete_frame = tk.LabelFrame(root)
delete_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")
view_frame = tk.LabelFrame(root)
view_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

# Load and display image
image = Image.open("gada.png")
image = image.resize((300, 100))
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo)
image_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Labels and Entries for Add Frame
tk.Label(add_frame, text="Category:").grid(row=0, column=0)
category_add_entry = tk.Entry(add_frame)
category_add_entry.grid(row=0, column=1)
tk.Label(add_frame, text="Price:").grid(row=1, column=0)
price_add_entry = tk.Entry(add_frame)
price_add_entry.grid(row=1, column=1)
tk.Label(add_frame, text="Company:").grid(row=2, column=0)
company_add_entry = tk.Entry(add_frame)
company_add_entry.grid(row=2, column=1)
tk.Label(add_frame, text="Model:").grid(row=3, column=0)
model_add_entry = tk.Entry(add_frame)
model_add_entry.grid(row=3, column=1)
tk.Label(add_frame, text="Quantity:").grid(row=4, column=0)
quantity_add_entry = tk.Entry(add_frame)
quantity_add_entry.grid(row=4, column=1)
tk.Button(add_frame, text="Add Item", command=add_item).grid(row=5, columnspan=2, pady=5)

# Labels and Entries for Update Frame
tk.Label(update_frame, text="Category:").grid(row=0, column=0)
category_update_entry = tk.Entry(update_frame)
category_update_entry.grid(row=0, column=1)
tk.Label(update_frame, text="Company:").grid(row=1, column=0)
company_update_entry = tk.Entry(update_frame)
company_update_entry.grid(row=1, column=1)
tk.Label(update_frame, text="Model:").grid(row=2, column=0)
model_update_entry = tk.Entry(update_frame)
model_update_entry.grid(row=2, column=1)
tk.Label(update_frame, text="New Price:").grid(row=3, column=0)
new_price_update_entry = tk.Entry(update_frame)
new_price_update_entry.grid(row=3, column=1)
tk.Label(update_frame, text="New Company:").grid(row=4, column=0)
new_company_update_entry = tk.Entry(update_frame)
new_company_update_entry.grid(row=4, column=1)
tk.Label(update_frame, text="New Model:").grid(row=5, column=0)
new_model_update_entry = tk.Entry(update_frame)
new_model_update_entry.grid(row=5, column=1)
tk.Label(update_frame, text="New Quantity:").grid(row=6, column=0)
new_quantity_update_entry = tk.Entry(update_frame)
new_quantity_update_entry.grid(row=6, column=1)
tk.Button(update_frame, text="Update Item", command=update_item).grid(row=7, columnspan=2, pady=5)

# Labels and Entries for Delete Frame
tk.Label(delete_frame, text="Category:").grid(row=0, column=0)
category_delete_entry = tk.Entry(delete_frame)
category_delete_entry.grid(row=0, column=1)
tk.Label(delete_frame, text="Company:").grid(row=1, column=0)
company_delete_entry = tk.Entry(delete_frame)
company_delete_entry.grid(row=1, column=1)
tk.Label(delete_frame, text="Model:").grid(row=2, column=0)
model_delete_entry = tk.Entry(delete_frame)
model_delete_entry.grid(row=2, column=1)
tk.Button(delete_frame, text="Delete Item", command=delete_item).grid(row=3, columnspan=2, pady=5)

# Button for View Frame
tk.Button(view_frame, text="View All Items", command=show_items).grid(row=0, column=0)
tk.Label(view_frame, text="Filter by Category:").grid(row=1,column=0)
category_filter_entry = tk.Entry(view_frame)
category_filter_entry.grid(row=1,column=1)
tk.Button(view_frame, text="View by Category", command=view_by_category).grid(row=2,column=0)
tk.Label(view_frame, text="Filter by Company:").grid(row=3,column=0)
company_filter_entry = tk.Entry(view_frame)
company_filter_entry.grid(row=3,column=1)
tk.Button(view_frame, text="View by Company", command=view_by_company).grid(row=4,column=0)

# Text widget to display result
result_text = tk.Text(root, width=115, height=25)
result_text.grid(row=1, column=4, columnspan=3, padx=10, pady=10)

# Close button
tk.Button(root, text="Close", command=close_connection).grid(row=2, column=4, columnspan=3, pady=5)

root.mainloop()
