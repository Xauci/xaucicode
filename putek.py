from tkinter import *
from tkinter import ttk, filedialog
import tkinter as tk
from tkinter import messagebox
import customtkinter
import csv
import json
import Productdb_if


def add_to_treeview():
    products = Productdb_if.fetch_productlist()
    tree.delete(*tree.get_children())
    for item in products:
        tree.insert('', END, values = item)
    
def clear_form(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())
        tree.focus('')
    productcombox.set("Choose Product")
    quantitycombox.set("Box")
    price_entry.delete(0, END)
    dateorder_entry.delete(0, END)
    datepay_entry.delete(0, END)
    paymentcombox.set('Payment')
    statuscombox.set('Status')
    remarks_entry.delete(0, END)
    
def read_display_data(event):
    selected_item = tree.focus()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear_form()
        productcombox.set(row[0])
        quantitycombox.set(row[1])
        price_entry.delete(0, row[2])
        dateorder_entry.delete(0, row[3])
        datepay_entry.delete(0, row[4])
        paymentcombox.set(row[5])
        statuscombox.set(row[6])
        remarks_entry.delete(0, row[7])
    else:
        pass     
    

def add_entry_item():
    product = productcombox.get()
    box = quantitycombox.get()
    price = price_entry.get()
    dorder = dateorder_entry.get()
    dpay = datepay_entry.get()
    payment = paymentcombox.get()
    status = statuscombox.get()
    remarks = remarks_entry.get()
    if not (product and box and price and dorder and dpay and payment and status and remarks):
        messagebox.showerror('Error', 'Enter all fields.')
    else:
        Productdb_if.insert_product(product, box, price, dorder, dpay, payment, status, remarks)
        add_to_treeview()
        clear_form()
        messagebox.showinfo('Success', 'Data has been inserted')
    
def delete_entry_item():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose an item to delete')
    else:
   
        selected_values = tree.item(selected_item, 'values')
        selected_id = selected_values[0] 
        Productdb_if.delete_product(selected_id)
        add_to_treeview()
        clear_form()
        messagebox.showinfo('Success', 'Data has been deleted')
  
def update_entry_item():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose an item to update')
    else:

        selected_values = tree.item(selected_item, 'values')
        selected_id = selected_values[0]
        product = productcombox.get()
        box = quantitycombox.get()
        price = price_entry.get()
        dorder = dateorder_entry.get()
        dpay = datepay_entry.get()
        payment = paymentcombox.get()
        status = statuscombox.get()
        remarks = remarks_entry.get()
        Productdb_if.update_product(product, box, price, dorder, dpay, payment, status, remarks, selected_id)
        add_to_treeview()
        clear_form()
        messagebox.showinfo('Success', 'Data has been updated')
        
def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    if file_path:
        with open(file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            header = ['ID', 'Product', 'Box', 'Price', 'Date Ordered', 'Date Paid', 'Payment', 'Status', 'Remarks']
            csv_writer.writerow(header)

            for item in tree.get_children():
                values = tree.item(item, 'values')
                csv_writer.writerow(values)

def import_from_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    if file_path:
        tree.delete(*tree.get_children())
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader) 

            for row in csv_reader:
                tree.insert('', 'end', values=row)

def export_to_json():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

    if file_path:
        data = []
        for item in tree.get_children():
            values = tree.item(item, 'values')
            data.append(dict(zip(['Product', 'Box', 'Price', 'Date Ordered', 'Date Paid', 'Payment', 'Status', 'Remark'], values)))

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)



customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.title("Gavino Product Tracker")
app.geometry(f"{1250}x{580}")
app.resizable(False, False)

        # configure grid layout (4x4)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure((2, 3), weight=0)
app.grid_rowconfigure((0, 1, 2), weight=1)


app.sidebar_frame = customtkinter.CTkFrame(app, width=140, corner_radius=0)
app.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
app.sidebar_frame.grid_rowconfigure(4, weight=1)
app.logo_label = customtkinter.CTkLabel(app.sidebar_frame, text="Product Tracker", font=customtkinter.CTkFont(size=20, weight="bold"))
app.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))



add_entry = customtkinter.CTkButton(app.sidebar_frame, text="Add Product", command = add_entry_item)
add_entry.grid(row=1, column=0, padx=20, pady=10)
delete_entry = customtkinter.CTkButton(app.sidebar_frame, text="Delete Product", command = delete_entry_item)
delete_entry.grid(row=2, column=0, padx=20, pady=10)
update_entry = customtkinter.CTkButton(app.sidebar_frame, text="Update Product", command = update_entry_item)
update_entry.grid(row=3, column=0, padx=20, pady=10)
export_csv = customtkinter.CTkButton(app.sidebar_frame, text="Export to CSV", command = export_to_csv)
export_csv.grid(row=4, column=0, padx=20, pady=10)
import_csv = customtkinter.CTkButton(app.sidebar_frame, text="Import CSV", command = import_from_csv)
import_csv.grid(row=5, column=0, padx=20, pady=10)
export_json = customtkinter.CTkButton(app.sidebar_frame, text="Export to JSON", command = export_to_json)
export_json.grid(row=6, column=0, padx=20, pady=10)



app.bar_frame = customtkinter.CTkFrame(app, height=300, corner_radius=0)
app.bar_frame.grid(row=4, column=0, columnspan=7, sticky="nsew")
app.bar_frame.grid_columnconfigure(4, weight=1)
app.productcbox = customtkinter.CTkOptionMenu(app.bar_frame, values=["Cassava", "Brownies"])
app.productcbox.grid(row=1, column=1, padx=(200, 10), pady=(20, 20))
app.productcbox.set("Choose Product")
app.quantitycbox = customtkinter.CTkOptionMenu(app.bar_frame, values=["Half", "Whole"])
app.quantitycbox.grid(row=1, column=2, padx=5, pady=(20, 20))
app.quantitycbox.set("Box")
app.price = customtkinter.CTkEntry(app.bar_frame, placeholder_text="Price")
app.price.grid(row=1, column=3, padx=5, pady=(20, 20), sticky="nsew")
app.dateorder = customtkinter.CTkEntry(app.bar_frame, placeholder_text="Date Ordered")
app.dateorder.grid(row=1, column=4, padx=5, pady=(20, 20), sticky="nsew")
app.datepay = customtkinter.CTkEntry(app.bar_frame, placeholder_text="Date Paid")
app.datepay.grid(row=1, column=5, padx=5, pady=(20, 20), sticky="nsew")       
app.paymentcbox = customtkinter.CTkOptionMenu(app.bar_frame, values=["CASH", "GCash"])
app.paymentcbox.grid(row=1, column=6, padx=5, pady=(20, 20))
app.paymentcbox.set("Payment")       
app.statuscbox = customtkinter.CTkOptionMenu(app.bar_frame, values=["Paid", "Not Paid"])
app.statuscbox.grid(row=1, column=7, padx=5, pady=(20, 20))
app.statuscbox.set("Status")
app.remarks = customtkinter.CTkEntry(app.bar_frame, placeholder_text="Remarks")
app.remarks.grid(row=2, column=2, columnspan = 4, padx=20, pady=(0, 10), sticky="nsew")









    

productcombox = app.productcbox
quantitycombox = app.quantitycbox
price_entry = app.price
dateorder_entry = app.dateorder
datepay_entry = app.datepay
paymentcombox = app.paymentcbox
statuscombox = app.statuscbox
remarks_entry = app.remarks






style = ttk.Style()

style.theme_use("default")

style.configure("Treeview",
                background="#F5F5F5",  # Light gray background
                foreground="#000000",  # Black text color
                rowheight=25,
                fieldbackground="#FFFFFF",  # White field background
                bordercolor="#CCCCCC",  # Light gray border color
                borderwidth=1)
style.map('Treeview', background=[('selected', '#ADD8E6')])  # Light blue when selected

style.configure("Treeview.Heading",
                background="#3399FF",  # Dodger Blue header background
                foreground="white",  # White header text color
                relief="flat")
style.map("Treeview.Heading",
          background=[('active', '#4682B4')])  # Steel Blue when active



tree = ttk.Treeview(app, height=15)
tree['columns'] = ('ID', 'Product', 'Box', 'Price', 'Date Ordered', 'Date Paid', 'Payment', 'Status', 'Remarks')
tree.column('#0', width=0, stretch=tk.NO)
tree.column('ID', anchor=tk.CENTER, width=10)
tree.column('Product', anchor=tk.CENTER, width=80)
tree.column('Box', anchor=tk.CENTER, width=30)
tree.column('Price', anchor=tk.CENTER, width=50)
tree.column('Date Ordered', anchor=tk.CENTER, width=60)
tree.column('Date Paid', anchor=tk.CENTER, width=60)
tree.column('Payment', anchor=tk.CENTER, width=50)
tree.column('Status', anchor=tk.CENTER, width=40)
tree.column('Remarks', anchor=tk.CENTER, width=150)


tree.heading('ID', text='ID')
tree.heading('Product', text='Product')
tree.heading('Box', text='Box')
tree.heading('Price', text='Price')
tree.heading('Date Ordered', text='Date Ordered')
tree.heading('Date Paid', text='Date Paid')
tree.heading('Payment', text='Payment')
tree.heading('Status', text='Status')
tree.heading('Remarks', text='Remarks')

tree.place(x=200, y=20, width=1040, height=435)




if __name__ == "__main__": 
    app.mainloop()
