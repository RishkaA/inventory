from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import sys
print(sys.executable)
import os
import sqlite3

table = "shoe_data"

root = Tk()
root.title("Stock manageent system")
root.iconbitmap("images/icon.ico")
root.geometry("1100x550")
root.config(bg = "#8bbabb")
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=3)
root.grid_columnconfigure(0, weight=1)

#icons
view_all_img = PhotoImage(file = "images/view all.png")
view_value_img = PhotoImage(file = "images/view value.png")
view_sale_img = PhotoImage(file = "images/view sale.png")
add_item_img = PhotoImage(file = "images/add item.png")
restock_img = PhotoImage(file = "images/restock.png")
search_img = PhotoImage(file = "images/search.png")
back_home_img = PhotoImage(file = "images/back_home.png")
shoe_bullet = PhotoImage(file = "images/shoe_img.png")
go_back = PhotoImage(file = "images/go_back.png")

# Empty list to store a list of objects of shoes
shoe_list = []


class Shoe:
    """
    Shoe class provides details of the shoe
    param: country: takes in the country of the shoe
    para: code: takes the code of the shoe
    param: product: takes the type of product
    param: cost: takes the cost of the shoe
    param: quantity: takes the quantity of the type of shoe
    """
    def __init__(self, code, product, cost, country, quantity):
        self.code = code
        self.product = product
        self.cost = cost
        self.country = country
        self.quantity = quantity

    def get_product(self):
        """
        method returns the product name of the given object
        """
        return self.product

    def get_code(self):
        """
        method returns the code of the given object
        """
        return self.code

    def get_cost(self):
        """
        method returns the cost of the given object
        """
        return self.cost

    def get_quantity(self):
        """
        method returns the quantity of the given object
        """
        return self.quantity

    def __str__(self):
        """
        identifies how the object will be printed out
        """
        return f"Product: {self.product}. Item code: {self.code}. Cost of the product is: £{self.cost}. Country: {self.country}. Stock items: {self.quantity}"
    
    def add_object(self):
        """
        creates a tuple to add a new object to the database table
        """
        return(self.code, self.product, self.cost, self.country, self.quantity)


# Functions outside the class
def read_shoes_data(table):
    """
    Function creates objects from each inventory row and adds all of them to the shoe_list
    """

    # clearing the show list of any possible previous data
    shoe_list.clear()

    cursor.execute(f"SELECT * FROM {table}")
    stock = [item for item in cursor]

    for shoe in stock:
        # each piece of data in the file line gets storwd in the variable
        country = shoe[3]
        code = shoe[0]
        product = shoe[1]
        cost = shoe[2]
        quantity = shoe[4]
        # creating object using new variables
        new_object = Shoe(code, product, cost, country, quantity)
        shoe_list.append(new_object)


def view_all():
    """
    This function iterates over the shoes list and
    prints the details of the shoes returned from the __str__
    function. 
    param: file: takes the name of the table containing shoe data.
    """
    # top information frame 
    view_all_fr = Frame(root, bg = "#fdfdfd")
    view_all_fr.grid(row = 0, column = 0, padx = 0, pady = 0, rowspan = 2, sticky = NSEW)
    view_all_fr.grid_columnconfigure(0, weight=1)
    view_all_fr.grid_rowconfigure(0, weight=1)

    view_all_c = Canvas(view_all_fr, bg = "#fdfdfd")
    view_all_c.grid(row = 0, column = 0, sticky = NSEW)

    s = Scrollbar(view_all_fr, orient = "vertical", command = view_all_c.yview)
    s.grid(row = 0, column = 1, sticky = NSEW)

    # header
    view_all_c.create_text(600, 40, text = "List of all stock shoe items:",
                    font = ("Times New Roman", 16, "bold"), fill= "#141616", justify= CENTER)

    # list of all shoes
    read_shoes_data(table)

    #statring column number
    y = 80
    for line in shoe_list:
        view_all_c.create_text(1, y, text = f"\t\t\t●\t{line}",
                          font = ("Times New Roman", 12), fill = "#141616", anchor = W)
        y += 30


    back_to_main_btn = Button(view_all_c, image = back_home_img, command = lambda: view_all_fr.destroy(),
                              relief = FLAT, bg = "#fdfdfd")
    view_all_c.create_window(5, 32, anchor=W, window= back_to_main_btn)


def sumbit_new(*args, table = "shoe_data"):
    """function checks that all data is entered correctly, creates a new shoe object
    and adds it to database"""
    code = code_e.get()
    product = product_e.get()
    obj_cost = cost_e.get()
    country = country_e.get()
    obj_quantity = quantity_e.get()
    entry_list = [code_e, product_e, cost_e, country_e, quantity_e]

    if obj_cost.isdigit() and obj_quantity.isdigit():
        cost = int(obj_cost)
        quantity = int(obj_quantity)
    else:
        response = messagebox.showerror("Entry error", "Cost and quantity must be numbers.")
        for entry in entry_list:
            entry.delete(0, END)
        return

    new_shoe = Shoe(code, product, cost, country, quantity)

    cursor.execute(f"""INSERT into {table}
                        VALUES (?, ?, ?, ?, ?)""", new_shoe.add_object())
    con.commit()
    response = messagebox.showinfo("Success", "New item added successfully.")
    

def check_input(*args):
    """
    Checking whether the input in the code, cost and quntity fields are of the correct format, 
    and displaying error messages if they are not.
    """
    code_input = cd.get()
    first_three_chars = code_input[0:3]

    # checking product code entry
    if first_three_chars.lower() == "sku" and len(code_input) == 8:
        code_msg_lbl.grid_remove()
        submit_btn.config(state = NORMAL)
    else:
        code_msg_lbl.grid()
        submit_btn.config(state = DISABLED)


def add_item():
    """
    This function allows a user to capture data
    about a shoe item and use this data to create a shoe object
    and add this item to the DB table.
    """
    global cd
    global code_e
    global product_e
    global cost_e
    global country_e
    global quantity_e
    global submit_btn
    global code_msg_lbl

    # frame for adding new product
    add_new_fr = Frame(root, bg = "#fdfdfd")
    add_new_fr.grid(row = 0, column = 0, padx = 0, pady = 0, rowspan = 2, sticky = NSEW)

    header = Label(add_new_fr, text = "Add new item to the database:", 
                   bg = "#fdfdfd", fg = "#141616", font = ("Times New Roman", 16, "bold"), anchor= CENTER)
    header.grid(row = 0, column = 0, columnspan = 2, pady = 25, sticky = E)

    # input labels
    code_lbl = Label(add_new_fr, text = "New code", bg = "#fdfdfd", 
                     font = ("Verdana", 10), fg = "#141616")
    code_lbl.grid(row = 1, column = 0, padx = (350, 20), pady = 2, sticky = E)
    code_msg_lbl = Label(add_new_fr, text = "8 characters. Must start with SKU", bg = "#fdfdfd", 
                     font = ("Verdana", 6), fg = "#141616", anchor = N)
    code_msg_lbl.grid(row = 2, column = 1, padx = 5, pady = 1, sticky = NW)
    product_lbl = Label(add_new_fr, text = "New product name", bg = "#fdfdfd",
                        font = ("Verdana", 10), fg = "#141616")
    product_lbl.grid(row = 3, column = 0, padx = (350, 20), pady = 4, sticky = E)
    cost_lbl = Label(add_new_fr, text = "New product's cost", bg = "#fdfdfd",
                     font = ("Verdana", 10), fg = "#141616")
    cost_lbl.grid(row = 4, column = 0, padx = (350, 20), pady = 4, sticky = E)
    country_lbl = Label(add_new_fr, text = "New product's country", bg = "#fdfdfd",
                        font = ("Verdana", 10), fg = "#141616")
    country_lbl.grid(row = 5, column = 0, padx = (350, 20), pady = 4, sticky = E)
    quantity_lbl = Label(add_new_fr, text = "New product's quantity", bg = "#fdfdfd",
                         font = ("Verdana", 10), fg = "#141616")
    quantity_lbl.grid(row = 6, column = 0, padx = (350, 20), pady = 4, sticky = E)

    
    # input fields
    cd = StringVar(add_new_fr)
    code_e = Entry(add_new_fr, width =20, textvariable = cd,
                   bd = 1, bg = "#f7f7f6", font = ("Calibri", 11), relief= FLAT,
                    highlightthickness= 1, highlightcolor= "#020202", highlightbackground= "#a7afaf")
    code_e.grid(row = 1, column = 1, padx = 0, sticky = W)
    cd.trace("w", check_input)
    product_e = Entry(add_new_fr, width = 20,
                      bd = 1, bg = "#f7f7f6", font = ("Calibri", 11), relief= FLAT,
                    highlightthickness= 1, highlightcolor= "#020202", highlightbackground= "#a7afaf")
    product_e.grid(row = 3, column = 1, padx = 0, sticky = W)
    cost_e = Entry(add_new_fr, width = 20, 
                    bd = 1, bg = "#f7f7f6", font = ("Calibri", 11), relief= FLAT, 
                    highlightthickness= 1, highlightcolor= "#020202", highlightbackground= "#a7afaf")
    cost_e.grid(row = 4, column = 1, padx = 0, sticky = W)
    country_e = Entry(add_new_fr, width = 20, bd = 1, bg = "#f7f7f6", font = ("Calibri", 11), relief= FLAT,
                    highlightthickness= 1, highlightcolor= "#020202", highlightbackground= "#a7afaf")
    country_e.grid(row = 5, column = 1, padx = 0, sticky = W)
    quantity_e = Entry(add_new_fr, width = 20,
                    bd = 1, bg = "#f7f7f6", font = ("Calibri", 11), relief= FLAT,
                    highlightthickness= 1, highlightcolor= "#020202", highlightbackground= "#8bbabb")
    quantity_e.grid(row = 6, column = 1, padx = 0, sticky = W)

    # buttons
    submit_btn = Button(add_new_fr, text = "Add item", command = sumbit_new, state = DISABLED,
                      bg = "#8bbabb", fg = "#fafcfc", font = ("Calibri", 12, "bold"), 
                      activebackground = "#dbeaea", relief = RAISED, width = 15)
    submit_btn.grid(row = 7, column = 1, sticky = W, padx = 8, pady = 10)

    back_home_btn = Button(add_new_fr, image = back_home_img, command = lambda: add_new_fr.destroy(),
                           bg = "#fdfdfd", relief = FLAT)
    back_home_btn.grid(row = 0, column = 0, padx = 15, sticky = W)


def quantity_data(table):
    """
    This function reads creates and returns a list of all shoe objects' quantities
    param: file: takes the name of the table containing the inventory data as an argument
    """
    read_shoes_data(table)

    # an empty list to store all object quantities
    quantities_list = []
    # looping over the shoe list and taking shoe quantitles and adding them to the quatities list
    for shoe in shoe_list:
        quantities_list.append(int(shoe.get_quantity()))

    return quantities_list


def view_sale():
    """
    This function determines the product with the highest quantity and prints this shoe as being for sale.
    """
    sale = Toplevel()
    sale.title("Sale item")
    sale.geometry("+{}+{}".format(700, 400))
    sale.iconbitmap("images/icon.ico")
    sale.config(bg = "#fdfdfd")
    sale.attributes("-toolwindow", True)
    sale.attributes("-topmost", True)

    header = Label(sale, text = "Item(s) on sale:", 
                   bg = "#fdfdfd", fg = "#305252", font = ("Times New Roman", 16, "bold"), anchor= CENTER)
    header.grid(row = 0, column = 0, columnspan = 2, pady = 20, padx = 30)

    # getting the item with the highest quantity
    quantities = quantity_data(table)
    highest = max(quantities)  

    cursor.execute(f"SELECT * FROM {table}")#
    # list variable storing each show object as a list 
    shoe_items = [list(item) for item in cursor]

        # reducing the highest quantity item's price by 30% and prinring the result on screen.
        # not updating DB to avoid duplicate price reduction
    for shoe_object in shoe_items:
        if shoe_object[4] == highest:
            shoe_object[2] = shoe_object[2] - (30 * shoe_object[2])/100
            sale_item_lbl = Label(sale, text = f"\nShoe item: {shoe_object[1]} Code {shoe_object[0]} is on sale at £{shoe_object[2]}",
                                  bg = "#eef5f5", fg = "#305252", font = ("Verdana", 12))
            sale_item_lbl.grid(row =  1, column = 0, sticky = NSEW)


def add_stock_to_table(table):
    """
    updating stock number for a selected item in the database
    """
    qty_to_add = add_item_qty.get()

    selected_product = restock_choice.get()
    product_listed = selected_product.split(" ")
    p_code = product_listed[0]
  
    if qty_to_add.isdigit():
        for shoe_item in shoe_list:
            if shoe_item.get_code() == p_code:
                current_amount = shoe_item.get_quantity()
                to_add = int(qty_to_add)
                new_quantity = current_amount + to_add
    else:
        response = messagebox.showerror("Entry error", "Entry must be a numerical value")
        return

    cursor.execute(f"""UPDATE {table}
                   SET quantity  = ? WHERE code = ?""", (new_quantity, p_code))
    con.commit()
    response = messagebox.showinfo("Successful", f"Quantity for {selected_product} updated")


def get_more():
    """
    Function allows user to add quantity to the lowesr stock quantity items.
    """   
    global add_item_qty

    # user shoe selection 
    selected_product = restock_choice.get()

    if restock_choice.get() == "":
         response = messagebox.showerror("No selection", "No product was selected")
    else:
        # new frame for adding items to stock
        add_more_fr = Frame(restock_w, bg = "#eef4f5")
        add_more_fr.grid(row = 0, column = 0, padx = 0, pady = 0, rowspan = 100, sticky = NSEW)
        header = Label(add_more_fr, text = f"Add to item: {selected_product}",
                    bg = "#eef4f5", fg = "#305252", font = ("Times New Roman", 16, "bold"), anchor = CENTER)
        header.grid(row = 0, column = 1, pady = (30, 10), padx = 10)

        add_item_qty = Entry(add_more_fr, width = 10,
                        bd = 1, bg = "#fafbfc", font = ("Calibri", 11), relief= FLAT,
                        highlightthickness= 1, highlightcolor= "#020202", highlightbackground= "#8bbabb")
        add_item_qty.grid(row = 0, column = 2, padx = 5, pady = (30, 10), sticky = W)

        confirm_add_btn = Button(add_more_fr, text = "Add stock", command = lambda: add_stock_to_table(table),
                        bg = "#8bbabb", fg = "#fafcfc", font = ("Calibri", 12, "bold"), 
                        activebackground = "#dbeaea", relief = RAISED, width = 10)
        confirm_add_btn.grid(row = 1, column = 2, pady = 5, sticky = W)

        back_btn = Button(add_more_fr, image = go_back, command = lambda: add_more_fr.destroy(),
                          bg = "#eef4f5", relief = FLAT)
        back_btn.grid(row = 0, column = 0, padx = 5, pady = (30, 10))

    
def restock():
    """
    This function will find the shoe object with the lowest quantity,
    which is the shoe that needs to be re-stocked. Ask the user what 
    quantity of shoes they want to add.
    This quantity will be updated in the table for this shoe.
    param: table: takes the name of the table containing inventory details as an argument
    """
    global restock_w
    global restock_choice

    restock_w = Toplevel()
    restock_w.title("Sale items")
    restock_w.iconbitmap("images/icon.ico")
    restock_w.config(bg = "#fdfdfd")
    restock_w.attributes("-toolwindow", True)
    restock_w.attributes("-topmost", True)

    quantities = quantity_data(table)
    minimum = min(quantities)  

    header = Label(restock_w, text = "Product(s) with minimum stock quantity:",
                   bg = "#fdfdfd", fg = "#305252", font = ("Times New Roman", 16, "bold"), anchor= CENTER)
    header.grid(row = 0, column = 0, columnspan = 2, pady = 20, padx = 30)

    # getting and displaying lowest stock items
    restock_choice = StringVar()
    y = 1
    for shoe in shoe_list:
        if int(shoe.get_quantity()) == minimum:
            item_to_restock = shoe
            display_value = f"{item_to_restock.get_code()} {item_to_restock.get_product()}"
            lowest_stock = Radiobutton(restock_w, text = item_to_restock, compound = "left", image = shoe_bullet,
                                       variable = restock_choice, value = display_value, 
                                 bg = "#fdfdfd", fg = "#305252", font = ("Verdana", 12))
            lowest_stock.grid(row = y, column = 0, padx = 30, pady = 10, sticky = W)
            y += 1
        if shoe == shoe_list[-1]:
            restock_btn = Button(restock_w, text = "Restock", command = get_more,
                      bg = "#8bbabb", fg = "#fafcfc", font = ("Calibri", 12, "bold"), 
                      activebackground = "#dbeaea", relief = RAISED, width = 15)
            restock_btn.grid(row = y+1, column = 0, padx = 40, pady = 10)

    width = lowest_stock.winfo_width()
    height = lowest_stock.winfo_height()
    restock_w.geometry("+{}+{}".format(width, height))


def go_back_comm():
    """
    functions allows user to go back from a window displaying seleted item's value
     to the list of all item's values
    """
    values_fr.destroy()

    item_values()


def update_values_frame(*args):
    """
    updates display values frame so that only the selected product's value os shown
    """
    # removing all canvas data
    # all_values_c.destroy()
    # s.destroy()
    for child in values_fr.winfo_children():
        child.destroy()

    # unconfiguring rfame row weight
    values_fr.grid_columnconfigure(0, weight=0)
    values_fr.grid_rowconfigure(0, weight=0)
    
    # getting the selected shoe data
    selected_value = sel_option.get()
    selected_list = selected_value.split(" ")

    header = Label(values_fr, text = "List of stock items' values:",
                   font = ("Times New Roman", 16, "bold"), bg= "#fdfdfd", fg = "black")
    header.grid(row = 0, column = 1, padx = 250, pady = 1)

    for shoe_item in shoe_list:
        if shoe_item.get_code() == selected_list[0]:
            value = shoe_item.get_cost() * shoe_item.get_quantity()
            sel_shoe_val = Label(values_fr, text = f"●  {shoe_item}\nTotal value: £{value}",
                                 bg = "#fdfdfd", fg = "black", font = ("Times New Roman", 12))
            sel_shoe_val.grid(row = 1, column = 1, padx = 16, pady = 35)

    back_btn = Button(values_fr, image = go_back, command = go_back_comm,
                          bg = "#fdfdfd", relief = FLAT)
    back_btn.grid(row = 0, column = 0, padx = (5, 104), pady = 1)


def item_values():
    """
    This function will calculate the total value for each item and print this information all shoes.
    """
    global all_values_c
    global values_fr
    global sel_option
    global option_list
    global s
    global dropdown_fr
    
    # top information frame 
    values_fr = Frame(root, bg = "#fdfdfd")
    values_fr.grid(row = 0, column = 0, padx = 0, pady = 0, rowspan = 2, sticky = NSEW)
    values_fr.grid_columnconfigure(0, weight=1)
    values_fr.grid_rowconfigure(0, weight=1)

    all_values_c = Canvas(values_fr, bg = "#fdfdfd")
    all_values_c.grid(row = 0, column = 0, sticky = NSEW)

    s = Scrollbar(values_fr, orient = "vertical", command = all_values_c.yview)
    s.grid(row = 0, column = 1, sticky = NSEW)

    # header
    all_values_c.create_text(550, 30, text = "List of stock items' values:",
                    font = ("Times New Roman", 16, "bold"), fill= "#141616", justify= CENTER)

    # list of all shoes
    read_shoes_data(table)

    # CREATING A DROPDOWN MENU
    # dropdown frame
    dropdown_fr = Frame(all_values_c)

    # dropdown options
    option_list = []
    for shoe_item in shoe_list:
        display_option = f"{shoe_item.get_code()} {shoe_item.get_product()}"
        option_list.append(display_option)

    sel_option = StringVar()
    sel_option.set("Choose product")
    sel_option.trace("w", update_values_frame)

    dropdown = OptionMenu(dropdown_fr, sel_option, *option_list)
    dropdown.config(background = "#f1f9fd", highlightbackground = "#f1f9fd")
    dropdown.pack()
    
    all_values_c.create_window(550, 70, window = dropdown_fr)

    # creating and displaying a list of all shoe values
    y = 130
    for shoe_item in shoe_list:
        # calculating total value of each item
        value = shoe_item.get_cost() * shoe_item.get_quantity()
        all_values_c.create_text(200, y, text = f"●  {shoe_item}\n    Total value: £{value}",
                          font = ("Times New Roman", 12), fill = "#141616", anchor = W)
        y += 70

    # placing a back to main menu button onto the screen
    back_home_btn = Button(all_values_c, image = back_home_img, command = lambda: values_fr.destroy(),
                           bg = "#fdfdfd", relief = FLAT)

    all_values_c.create_window(5, 32, anchor=W, window= back_home_btn)


def back_to_search():
    """
    function closes the current window with shoe_item display and
    takes the user back to the search item window
    """
    search_w.destroy()

    item_search()


def lookup():
    """
    fundtion looks for the code entered in the search box in the database
    error message is displayed if code not found
    and product is dicplayed if the code matches
    """
    read_shoes_data(table)

    search_code = code_entry.get()
    
    # storing all item codes in a list
    codes = []
    # looping over the shoe list and printing out the details of the object with the matching code
    for shoe_item in shoe_list:
        codes.append(shoe_item.get_code())
        if shoe_item.get_code() == search_code.upper():
           # clearing all widgets and creating new ones to display
           for child in search_w.winfo_children():
               child.destroy()
           found_shoe = Label(search_w, text = shoe_item, 
                              font = ("Verdana", 14, "bold"), bg= "#f3f3f3", fg = "#141616")
           found_shoe.grid(row = 0, column = 1, padx = 20, pady = 30)
           back_btn = Button(search_w, image = go_back, command = back_to_search,
                             relief = FLAT, bg = "#f3f3f3")
           back_btn.grid(row = 0, column = 0)
    
    if search_code.upper() not in codes:
        response = messagebox.showerror("Error", "Code not found")


def item_search():
    """
    allows user to search the database for a specific shoe object using item code
    """
    global code_entry
    global search_w

    search_w = Toplevel()
    search_w.title("Search item")
    search_w.geometry("+{}+{}".format(450, 300))
    search_w.iconbitmap("images/icon.ico")
    search_w.config(bg = "#f3f3f3")
    search_w.attributes("-toolwindow", True)
    search_w.attributes("-topmost", True)

    header = Label(search_w, text = "Enter item code:", 
                   font = ("Times New Roman", 14, "bold"), bg = "#f3f3f3", fg = "#141616")
    header.grid(row = 0, column = 0, padx = 75, pady = (30, 10), sticky = NSEW)

    code_entry = Entry(search_w, width = 20, bd = 1, bg = "#f7f7f6", font = ("Calibri", 13), relief= FLAT, 
                    highlightthickness= 1, highlightcolor= "#020202", highlightbackground= "#a7afaf")
    code_entry.grid(row = 1, column = 0, padx = 75, pady = 10, sticky = NSEW)

    submit_search_btn = Button(search_w, text = "Search", command = lookup,
                        bg = "#8bbabb", fg = "#fafcfc", font = ("Calibri", 12, "bold"), width=15)
    submit_search_btn.grid(row = 2, column = 0, padx = 90, pady = 10)
 

def main_page(table):
    """
    main page that displays has all the main menu options
    """
    # top information frame 
    general_info = Frame(root, bg = "#fdfdfd")
    general_info.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = NSEW)
    general_info.columnconfigure(0, weight=1)
    general_info.columnconfigure(1, weight=1)
    general_info.columnconfigure(2, weight=1)

    # main menu frame
    main = Frame(root, bg = "#fdfdfd")
    main.grid(row = 1, column = 0, padx = 0, pady = 0, sticky = NSEW, ipady = 10)
    main.columnconfigure(0, weight=1)
    main.columnconfigure(1, weight=3)
    main.columnconfigure(2, weight=1)
    main.columnconfigure(3, weight=3)

    cursor.execute(f"SELECT * FROM {table}")
    total_items = [list(item) for item in cursor]

    # caculating total value of all stock
    values_per_item = []
    for shoe_item in total_items:
        value = shoe_item[2]*shoe_item[4]
        values_per_item.append(value)
    stock_value = sum(values_per_item)

    # establishing if there's item with 0 stock
    zero_items = []
    for shoe_item in total_items:
        if shoe_item[4] == 0:
            to_display = f"{shoe_item[0]} {shoe_item[1]}"
            zero_items.append(to_display)
        
    if len(zero_items) > 0:
        final_result = zero_items
    else: 
        final_result = "None"

    # creating top information labels
    total_stock = Label(general_info, text = f"\n  Total of stock items:  \n\n{len(total_items)}\n", justify = CENTER, height = 8,
                        bg = "#fccbb7", fg = "#9a9a9a", font = ("Verdana", 11, "bold"))
    total_stock.grid(row = 0, column = 0, padx = (50, 10), pady = 30, sticky = EW)

    total_value = Label(general_info, text = f"\n  Total stock value:  \n\n£{stock_value}\n", justify = CENTER, height = 8,
                        bg = "#dff5fe", fg = "#9a9a9a", font = ("Verdana", 11, "bold"))
    total_value.grid(row = 0, column = 1, padx = 10, pady = 30, sticky = EW)

    zero = Label(general_info, text = f"\n  Items of 0 stock:  \n\n{final_result}\n", justify = CENTER, height = 8,
                        bg = "#defeed", fg = "#9a9a9a", font = ("Verdana", 11, "bold"))
    zero.grid(row = 0, column = 2, padx = (10, 50), pady = 30, sticky = EW)

    # menu image labels
    view_all_lbl = Label(main, image = view_all_img, bg = "#fdfdfd")
    view_all_lbl.grid(row = 1, column = 0, sticky = E)
    view_sale_lbl = Label(main, image = view_sale_img, bg = "#fdfdfd")
    view_sale_lbl.grid(row = 2, column = 0, sticky = E)
    item_values_lbl = Label(main, image = view_value_img, bg = "#fdfdfd")
    item_values_lbl.grid(row = 3, column = 0, sticky = E)
    add_item_lbl = Label(main, image = add_item_img, bg = "#fdfdfd")
    add_item_lbl.grid(row = 1, column = 2, sticky = E)
    restock_lbl = Label(main, image = restock_img, bg = "#fdfdfd")
    restock_lbl.grid(row = 2, column = 2, sticky = E)
    item_search_lbl = Label(main, image = search_img, bg = "#fdfdfd")
    item_search_lbl.grid(row = 3, column = 2, sticky = E)

    # menu option buttons
    # left column
    view_all_btn = Button(main, text = "View all items", command = view_all,
                      bg = "#8bbabb", fg = "#fafcfc", font = ("Calibri", 12, "bold"), 
                      bd = 0, activebackground = "#dbeaea")
    view_all_btn.grid(row = 1, column = 1, padx = (0, 70), pady = 10, sticky =EW)
    view_sale_btn = Button(main, text = "View sale", command = view_sale,
                      bg = "#8bbabb", fg = "#fafcfc", font = ("Calibri", 12, "bold"), 
                      bd = 0, activebackground = "#dbeaea")
    view_sale_btn.grid(row = 2, column = 1, padx = (0, 70), pady = 10, sticky = EW)
    item_values_btn = Button(main, text = "View item values", command = item_values,
                      bg = "#8bbabb", fg = "#fafcfc", font = ("Calibri", 12, "bold"), 
                      bd = 0, activebackground = "#dbeaea")
    item_values_btn.grid(row = 3, column = 1, padx = (0, 70), pady = 10, sticky =EW)

    # right column
    add_item_btn = Button(main, text = "Add new item", command = add_item,
                      bg = "#8bbabb", fg = "#fafcfc", font = ("Calibri", 12, "bold"), 
                      bd = 0, activebackground = "#dbeaea")
    add_item_btn.grid(row = 1, column = 3, padx = (0, 50), pady = 10, sticky = EW)
    restock_btn = Button(main, text = "Restock item", command = restock,
                      bg = "#8bbabb", fg = "#fafcfc", font = ("Calibri", 12, "bold"), 
                      bd = 0, activebackground = "#dbeaea")
    restock_btn.grid(row = 2, column = 3, padx = (0, 50), pady = 10, sticky = EW)
    item_search_btn = Button(main, text = "Look up item", command = item_search,
                      bg = "#8bbabb", fg = "#fafcfc", font = ("Calibri", 12, "bold"), 
                      bd = 0, activebackground = "#dbeaea")
    item_search_btn.grid(row = 3, column = 3, padx = (0, 50), pady = 10, sticky = EW)


def connect():
    """
    checks whether database entered by user exists.
    Connects if it does and displays the error message if it doesn't.
    """
    global cursor
    global con

    given_name = db_name.get()
    
    # if atabase exists, connect to it and perform operations as needed
    if os.path.isfile(given_name):
        con = sqlite3.connect(given_name)
        response = messagebox.showinfo("Success", "Connected", parent = start)
        start.destroy()
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS shoe_data ( 
                    code TEXT PRIMARY KEY,
                    product TEXT,
                    cost INTEGER,
                    country TEXT,  
                    quantity INTEGER 
                    )
        """)
        main_page(table)
    else:
        response = messagebox.showerror("Error", "Database does not exist", parent = start)


def db_connection():
    """
    asking a user to enter a database name until the user enters a valid DB name
    """

    global start
    global db_name

    start = Toplevel()
    start.title("Connect to database")
    start.geometry("+{}+{}".format(700, 400))
    start.iconbitmap("images/icon.ico")
    start.config(bg = "#f3f3f3")
    start.attributes("-toolwindow", True)
    start.attributes("-topmost", True)

    header = Label(start, text = "Enter the database name:", 
                   font = ("Times New Roman", 14, "bold"), bg = "#f3f3f3", fg = "#141616")
    header.grid(row = 0, column = 0, padx = 75, pady = (30, 10), sticky = NSEW)

    db_name = Entry(start, width = 20, bd = 1, bg = "#f7f7f6", font = ("Calibri", 13), relief= FLAT, 
                    highlightthickness= 1, highlightcolor= "#020202", highlightbackground= "#a7afaf")
    db_name.grid(row = 1, column = 0, padx = 75, pady = 10, sticky = NSEW)

    submit_btn = Button(start, text = "Connect", command = connect,
                        bg = "#8bbabb", fg = "#fafcfc", font = ("Calibri", 12, "bold"), width=15)
    submit_btn.grid(row = 2, column = 0, padx = 90, pady = 10)


################################## #############################################
################################## #############################################
############################## MAIN MENU #######################################
################################## #############################################
################################## #############################################




def seach_shoe(table):
    """
    This function searches for a shoe from the list
    using the shoe code and returns this object so that it is printed.
    param: table: takes the name of the file holding inventory data as an ardument
    """
    read_shoes_data(table)

    # list variable to store all the object codes in the inventory
    codes = []
    for Shoe in shoe_list:
        codes.append(Shoe.get_code())

    # getting a code from user while checking code exists and all conditions are met
    while True:
        code = input("Enter the prodct code: ")
        if code[0:3].lower() != "sku":
            print("Please check the code. Must start with SKU.")
            continue
        elif len(code) != 8:
            print("Please check the code. 8 characters expected.")
            continue
        elif code not in codes:
            print("Code not found. Try again")
            continue
        else:
            break
    
    # looping over the shoe list and printing out the details of the object with the matching code
    for Shoe in shoe_list:
        if Shoe.get_code() == code:
            print(Shoe)
 
    

db_connection()

# # #==========Main Menu=============
# while True:
#     menu = input(f'''\n╔═══════ Select Menu Option: ═══════╗
#  'va' - to view all items
#  'nd' - to add new item to the file
#  'r'  - to restock an item
#  's'  - to search for a shoe
#  'v'  - to view value for each item
#  'sa' - to view sale item(s)
#  'e'  - to exit
#  : ''')

#     if menu.lower() == "va":
#         view_all(table)
        
#     elif menu.lower() == "nd":
#         read_shoes_data(table)
        
#         capture_shoes()
#         print(f"\nThe item was added to the list")

#     elif menu.lower() == "r":
#         re_stock(table)
#         print(f"\nStock has been updated.\n")
                
#     elif menu.lower() == "s":
#         seach_shoe(table)
                
#     elif menu.lower() == "v":
#         value_per_item(table)

#     elif menu.lower() == "sa":
#         highest_qty(table)
    
#     elif menu.lower() == "e":
#         print(f"\nGoodbye!\n")
#         con.close()
#         break

root.mainloop()