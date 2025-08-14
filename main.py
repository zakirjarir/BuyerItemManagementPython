import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime, timezone, timedelta

# Company Info
COMPANY_NAME = 'Zakir Store'
COMPANY_ADDRESS = 'Pabna, Bangladesh'
inventory = []

#  Get Current Time
def get_current_time():
    return datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=6))).strftime("%Y-%m-%d %H:%M:%S")

#  PDF Generator
def generate_pdf():
    if not inventory:
        messagebox.showwarning("Warning", "No items in inventory!")
        return

    # File save location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Save Invoice As"
    )
    if not file_path:
        return

    buyer_id = entry_id.get()
    buyer_name = entry_name.get()
    buyer_phone = entry_phone.get()
    buyer_address = entry_address.get()
    dateTime = get_current_time()

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 50, COMPANY_NAME)
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 70, COMPANY_ADDRESS)

    # Buyer Info
    y = height - 100
    c.drawString(50, y, f'Date: {dateTime}'); y -= 20
    c.drawString(50, y, f'Buyer Name: {buyer_name}'); y -= 20
    c.drawString(50, y, f'Phone: {buyer_phone}'); y -= 20
    c.drawString(50, y, f'Address: {buyer_address}'); y -= 20
    c.drawString(50, y, f'Buyer ID: {buyer_id}'); y -= 30

    # Table Header
    c.setFont('Helvetica-Bold', 12)
    c.drawString(50, y, 'Item')
    c.drawString(200, y, 'Unit Price')
    c.drawString(300, y, 'Quantity')
    c.drawString(400, y, 'Total')
    y -= 15
    c.line(50, y, 500, y)
    y -= 15

    # Table Data
    c.setFont('Helvetica', 12)
    grand_total = 0
    for item in inventory:
        c.drawString(50, y, item['name'])
        c.drawString(200, y, f"{item['price']:.2f}")
        c.drawString(300, y, f"{item['quantity']:.2f}")
        c.drawString(400, y, f"{item['total']:.2f}")
        grand_total += item['total']
        y -= 20

    # Grand Total
    c.setFont('Helvetica-Bold', 12)
    c.drawString(300, y, 'Grand Total:')
    c.drawString(400, y, f"{grand_total:.2f}")

    c.save()
    messagebox.showinfo("Success", f"Invoice saved at:\n{file_path}")

# Add Item
def add_item():
    try:
        name = entry_item.get()
        price = float(entry_price.get())
        quantity = float(entry_quantity.get())
        total = price * quantity

        inventory.append({'name': name, 'price': price, 'quantity': quantity, 'total': total})
        messagebox.showinfo("Added", f"{name} added successfully!")

        entry_item.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for price and quantity.")

# 🖥️ UI Setup
root = tk.Tk()
root.title("Invoice Generator - Zakir Store")
root.geometry("700x500")
root.configure(bg="#f5f5f5")

# Frames
buyer_frame = tk.LabelFrame(root, text=" Buyer Information ", font=("Helvetica", 14, "bold"), bg="#f5f5f5", padx=10, pady=10)
buyer_frame.pack(fill="x", padx=20, pady=10)

item_frame = tk.LabelFrame(root, text=" Item Information ", font=("Helvetica", 14, "bold"), bg="#f5f5f5", padx=10, pady=10)
item_frame.pack(fill="x", padx=20, pady=10)

button_frame = tk.Frame(root, bg="#f5f5f5")
button_frame.pack(pady=20)

# Buyer Info Widgets
tk.Label(buyer_frame, text="Buyer ID", font=("Helvetica", 12), bg="#f5f5f5").grid(row=0, column=0, sticky="e", pady=5)
entry_id = tk.Entry(buyer_frame, font=("Helvetica", 12), width=30)
entry_id.grid(row=0, column=1, pady=5)

tk.Label(buyer_frame, text="Buyer Name", font=("Helvetica", 12), bg="#f5f5f5").grid(row=1, column=0, sticky="e", pady=5)
entry_name = tk.Entry(buyer_frame, font=("Helvetica", 12), width=30)
entry_name.grid(row=1, column=1, pady=5)

tk.Label(buyer_frame, text="Phone", font=("Helvetica", 12), bg="#f5f5f5").grid(row=2, column=0, sticky="e", pady=5)
entry_phone = tk.Entry(buyer_frame, font=("Helvetica", 12), width=30)
entry_phone.grid(row=2, column=1, pady=5)

tk.Label(buyer_frame, text="Address", font=("Helvetica", 12), bg="#f5f5f5").grid(row=3, column=0, sticky="e", pady=5)
entry_address = tk.Entry(buyer_frame, font=("Helvetica", 12), width=30)
entry_address.grid(row=3, column=1, pady=5)

# Item Info Widgets
tk.Label(item_frame, text="Item Name", font=("Helvetica", 12), bg="#f5f5f5").grid(row=0, column=0, sticky="e", pady=5)
entry_item = tk.Entry(item_frame, font=("Helvetica", 12), width=30)
entry_item.grid(row=0, column=1, pady=5)

tk.Label(item_frame, text="Unit Price", font=("Helvetica", 12), bg="#f5f5f5").grid(row=1, column=0, sticky="e", pady=5)
entry_price = tk.Entry(item_frame, font=("Helvetica", 12), width=30)
entry_price.grid(row=1, column=1, pady=5)

tk.Label(item_frame, text="Quantity (KG)", font=("Helvetica", 12), bg="#f5f5f5").grid(row=2, column=0, sticky="e", pady=5)
entry_quantity = tk.Entry(item_frame, font=("Helvetica", 12), width=30)
entry_quantity.grid(row=2, column=1, pady=5)

# Buttons
tk.Button(button_frame, text="Add Item", command=add_item, font=("Helvetica", 12, "bold"), bg="#0C86EA", fg="white", padx=15, pady=5).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Generate PDF", command=generate_pdf, font=("Helvetica", 12, "bold"), bg="green", fg="white", padx=15, pady=5).grid(row=0, column=1, padx=10)

root.mainloop()
