import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import mysql.connector as mysql


# im going to create simple inventory system crud application using tkinter and mysql with design

def connectDB():
    # create connection to database
    conn = mysql.connect(host='localhost', user='root', password='', database='inventory')
    cursor = conn.cursor()
    return conn, cursor
# create table for id, name, quantity, size, price in database
def createTable():
    conn, cursor = connectDB()
    cursor.execute('CREATE TABLE IF NOT EXISTS inventory(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), quantity VARCHAR(255), size VARCHAR(255), price VARCHAR(255))')
    cursor.close()
    conn.close()
def addItem():
    def insertData():
        createTable()
        conn, cursor = connectDB()
        cursor.execute('INSERT INTO inventory(name, quantity, size, price) VALUES(%s, %s, %s, %s)', (name.get(), quantity.get(), size.get(), price.get()))
        conn.commit()
        cursor.close()
        conn.close()
        mb.showinfo('Success', 'Item added successfully')
        window.destroy()
        # refresh treeview
        tree.delete(*tree.get_children())

    window = tk.Toplevel()
    window.title('Add Item')
    window.geometry('400x400')
    window.resizable(False, False)
    # create label and entry for name
    nameLabel = tk.Label(window, text='Name')
    nameLabel.place(x=10, y=10)
    name = tk.Entry(window)
    name.place(x=10, y=30)
    # create label and entry for quantity
    quantityLabel = tk.Label(window, text='Quantity')
    quantityLabel.place(x=10, y=60)
    quantity = tk.Entry(window)
    quantity.place(x=10, y=80)
    # create label and entry for size
    sizeLabel = tk.Label(window, text='Size')
    sizeLabel.place(x=10, y=110)
    size = tk.Entry(window)
    size.place(x=10, y=130)
    # create label and entry for price
    priceLabel = tk.Label(window, text='Price')
    priceLabel.place(x=10, y=160)
    price = tk.Entry(window)
    price.place(x=10, y=180)

    # create button to insert data
    insertButton = tk.Button(window, text='Insert', command=insertData)
    insertButton.place(x=10, y=210)

    window.mainloop()

def deleteItem():
    if not tree.selection():
        mb.showwarning('Warning', 'Please select an item')
    else:
        result = mb.askquestion('Delete', 'Are you sure you want to delete this item?')
        if result == 'yes':
            conn, cursor = connectDB()
            cursor.execute('DELETE FROM inventory WHERE id=%s', (tree.set(tree.selection()[0], '#1'),))
            conn.commit()
            cursor.close()
            conn.close()
            mb.showinfo('Success', 'Item deleted successfully')
            # refresh treeview
            tree.delete(*tree.get_children())
            viewItems()

    # update item in database
def updateItem():
    if not tree.selection():
        mb.showwarning('Warning', 'Please select an item')
    else:
        def updateData():
            conn, cursor = connectDB()
            cursor.execute('UPDATE inventory SET name=%s, quantity=%s, size=%s, price=%s WHERE id=%s', (name.get(), quantity.get(), size.get(), price.get(), tree.set(tree.selection()[0], '#1')))
            conn.commit()
            cursor.close()
            conn.close()
            mb.showinfo('Success', 'Item updated successfully')
            window.destroy()
            # refresh treeview
            tree.delete(*tree.get_children())
            viewItems()

        window = tk.Toplevel()
        window.title('Update Item')
        window.geometry('400x400')
        window.resizable(False, False)
        # create label and entry for name
        nameLabel = tk.Label(window, text='Name')
        nameLabel.place(x=10, y=10)
        name = tk.Entry(window)
        name.place(x=10, y=30)
        # create label and entry for quantity
        quantityLabel = tk.Label(window, text='Quantity')
        quantityLabel.place(x=10, y=60)
        quantity = tk.Entry(window)
        quantity.place(x=10, y=80)
        # create label and entry for size
        sizeLabel = tk.Label(window, text='Size')
        sizeLabel.place(x=10, y=110)
        size = tk.Entry(window)
        size.place(x=10, y=130)
        # create label and entry for price
        priceLabel = tk.Label(window, text='Price')
        priceLabel.place(x=10, y=160)
        price = tk.Entry(window)
        price.place(x=10, y=180)

        # create button to insert data
        updateButton = tk.Button(window, text='Update', command=updateData)
        updateButton.place(x=10, y=210)

        window.mainloop()

def refresh():
    tree.delete(*tree.get_children())
    viewItems()


# create a window
window = tk.Tk()
window.title("CICT Inventory System")
# geomtry of window based on items in treeview
window.geometry('600x300')
window.resizable(False, False)

# create frame
frame = tk.Frame(window)
frame.place(x=0, y=0, width=600, height=300)


# create a menu
menu = tk.Menu(window)
window.config(menu=menu)

# create a submenu
submenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='Items', menu=submenu)
submenu.add_command(label='Add Item', command=addItem)
submenu.add_command(label='Update Item', command=updateItem)
submenu.add_command(label='Delete Item' , command=deleteItem)
submenu.add_separator()
submenu.add_command(label='Exit', command=window.quit)

# create title label and put on top of frame
titleLabel = tk.Label(frame, text='CICT Inventory System', font=('Arial', 20))
titleLabel.place(x=200, y=10)

#center items to treeview
def centerItems():
    tree.column('#0', width=0, stretch='no')
    tree.column('#1', width=100, anchor='center')
    tree.column('#2', width=100, anchor='center')
    tree.column('#3', width=100, anchor='center')
    tree.column('#4', width=100, anchor='center')
    tree.column('#5', width=100, anchor='center')

# create tree view for items on main window
tree = ttk.Treeview(frame, columns=('id', 'name', 'quantity', 'size', 'price'), show='headings')
tree.heading('id', text='ID')
tree.heading('name', text='Name')
tree.heading('quantity', text='Quantity')
tree.heading('size', text='Size')
tree.heading('price', text='Price')
tree.grid(row=0, column=0, sticky="nsew")
centerItems()
#view items in database to treeview
def viewItems():
    conn, cursor = connectDB()
    cursor.execute('SELECT * FROM inventory')
    rows = cursor.fetchall()
    for row in rows:
        tree.insert('', 'end', values=row)
    cursor.close()
    conn.close()

viewItems()

# create a scrollbar
scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
tree.configure(yscrollcommand=scrollbar.set)

# create button for refresh
refreshButton = tk.Button(frame, text='Refresh', command=refresh)
refreshButton.grid(row=1, column=0, sticky="nsew")

window.mainloop()
