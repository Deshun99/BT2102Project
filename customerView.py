from tkinter import font as tkfont
from tkinter import ttk
from tkinter import *

from numpy import empty

from customer import *
from utilities import *
from tkinter import messagebox
from userDetails import *
from oshes import *
#from PIL import ImageTk, Image
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option("display.max_rows", None)


class CustDash(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Dashboard", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # def getDetails():
        #     label1 = tk.Label(self, text= "Welcome Back" + username(), bg= controller.base, fg= controller.PriColor, font= controller.title_font)
        #     label1.pack()

        # getDetails()

        purchaseButton = tk.Button(self, text="Purchase An Item", font=controller.button_font, fg=controller.button_fontColor,
                                   command=lambda: controller.show_frame("ItemPurchase"), height="3", width="20")
        SearchButton = tk.Button(self, text="Search", font=controller.button_font, fg=controller.button_fontColor,
                                 command=lambda: controller.show_frame("SearchTypes"), height="3", width="20")
        RequestButton = tk.Button(self, text="Request", font=controller.button_font, fg=controller.button_fontColor,
                                  command=lambda: controller.show_frame("Request"), height="3", width="20")
        serviceButton = tk.Button(self, text="Service Payment", font=controller.button_font, fg=controller.button_fontColor,
                                  command=lambda: controller.show_frame("Service"), height="3", width="20")
        exitButton = tk.Button(self, text="Exit", font=controller.button_font, fg=controller.button_fontColor,
                               command=lambda: controller.show_frame("StartPage"), height="3", width="20")

        purchaseButton.pack(pady=10)
        SearchButton.pack(pady=10)
        RequestButton.pack(pady=10)
        serviceButton.pack(pady=10)
        exitButton.pack(pady=10)


class CustomerSignUpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Create Customer Account", bg=controller.priColor,
                         fg=controller.base, width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        tk.Label(self, text="Username", fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
            side="top", fill="x", pady=5)
        eUser = Entry(self, width=35)
        eUser.insert(0, "")
        eUser.pack()

        tk.Label(self, text="Name", fg=controller.priColor, bg=controller.base,
                 font=controller.header_font).pack(side="top", fill="x", pady=5)
        eName = Entry(self, width=35)
        eName.insert(0, "")
        eName.pack()

        tk.Label(self, text="Phone Number", fg=controller.priColor, bg=controller.base,
                 font=controller.header_font).pack(side="top", fill="x", pady=5)
        ePhone = Entry(self, width=35)
        ePhone.insert(0, "")
        ePhone.pack()

        tk.Label(self, text="Gender", fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
            side="top", fill="x", pady=5)
        genderList = ["-", "M", "F"]
        eGender = ttk.Combobox(self, values=genderList, height=3, width=35)
        eGender.set("-")
        eGender.pack()

        tk.Label(self, text="Email Address", fg=controller.priColor, bg=controller.base,
                 font=controller.header_font).pack(side="top", fill="x", pady=5)
        eEmail = Entry(self, width=35)
        eEmail.insert(0, "")
        eEmail.pack()

        tk.Label(self, text="Home Address", fg=controller.priColor, bg=controller.base,
                 font=controller.header_font).pack(side="top", fill="x", pady=5)
        eAdd = Entry(self, width=35)
        eAdd.insert(0, "")
        eAdd.pack()

        tk.Label(self, text="Password", fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
            side="top", fill="x", pady=5)
        ePW = Entry(self, width=35)
        ePW.insert(0, "")
        ePW.pack()

        tk.Label(self, text="Confirm Password", fg=controller.priColor, bg=controller.base,
                 font=controller.header_font).pack(side="top", fill="x", pady=5)
        eCPW = Entry(self, width=35)
        eCPW.insert(0, "")
        eCPW.pack()

        tk.Label(self, text=" ", bg=controller.base).pack()

        enterButton = tk.Button(self, text="Enter", font=controller.button_font, fg=controller.button_fontColor,
                                command=lambda: custSignUp(), height="3", width="20")
        enterButton.pack(pady=10)

        backButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("AdminCustomerSignUp"), height="2", width="10")
        backButton.pack(pady=10)
        backButton.place(x=10, y=50)

        def popWin(message, header, button):
            win = Toplevel()
            win.title(header)
            Label(win, text=message, fg="#243E36", bg="#7CA982").pack()
            win.configure(background="#f1f7ed")
            Button(win, text=button, command=win.destroy).pack()
            win.geometry("600x250")
            win.eval('tk::PlaceWindow . center')

        def custSignUp():
            notRegistered = "UserID Or Password Is Invalid"
            successRegistered = "Login Successfully As A Customer"
            username = eUser.get()
            name = eName.get()
            password = ePW.get()
            cPassword = eCPW.get()
            gender = eGender.get()
            email = eEmail.get()
            phone = ePhone.get()
            add = eAdd.get()

            if password == cPassword and password != empty:
                if registerCustomer(username, name, password, gender, email, add, phone):
                    print(successRegistered)
                    controller.show_frame("CustomerSignInPage")
                    #popWin("Registration Successful", "Result", "Okay")
                    messagebox.showinfo(
                        "Registration Successful", "Registration Successful!")
                else:
                    #popWin("Username has been taken", "Result", "Okay")
                    messagebox.showerror(
                        "Information", "Username has been taken")
            else:
                print(notRegistered)
                #popWin("Passwords do not match, please try again", "Result", "Okay")
                messagebox.showerror(
                    "Information", "Passwords do not match, please try again")


class CustomerSignInPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Sign In", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        tk.Label(self, text="Username ID", fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
            side="top", fill="x", pady=10)
        eUser = tk.Entry(self, width=35, cursor="xterm")
        eUser.pack()

        tk.Label(self, text="Password", fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
            side="top", fill="x", pady=10)
        ePW = tk.Entry(self, width=35, cursor="xterm")
        ePW.pack()

        tk.Label(self, text=" ", bg=controller.base).pack()

        enterButton = tk.Button(self, text="Enter", font=controller.button_font, fg=controller.button_fontColor,
                                command=lambda: signIn(), height="3", width="20")
        enterButton.pack(pady=10)
        backButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("AdminCustomerSignIn"), height="2", width="10")
        backButton.pack(pady=10)
        backButton.place(x=10, y=50)

        def signIn():
            notRegistered = "UserID Or Password Is Invalid"
            successRegistered = "Login Successfully As A Customer"
            global username
            username = eUser.get()
            password = ePW.get()

            UserDetails(username)

            if loginCustomer(username, password):
                print(successRegistered)
                tk.Label(self, text=successRegistered, fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
                    side="top", fill="x", pady=10)
                messagebox.showinfo("Information", "Login Successful!")
                controller.show_frame("CustDash")
            else:
                print(notRegistered)
                messagebox.showerror("Information", "Login failed")


class ItemPurchase(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Item Purchase", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        label1 = tk.Label(self, text="Input Item ID", fg=controller.priColor, bg=controller.base,
                          font=controller.header_font).pack(pady=10)
        eItemID = Entry(self, width=30)
        eItemID.insert(0, "")
        eItemID.pack(ipady=10)

        purchaseButton = tk.Button(self, text="Purchase", font=controller.button_font, fg=controller.button_fontColor, height="3", width="20",
                                   command=lambda: purchaseItem())
        purchaseButton.pack(pady=10)

        backButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("CustDash"), height="2", width="10")
        backButton.pack(pady=10)
        backButton.place(x=10, y=50)

        def purchaseItem():

            itemNotAvailable = "Item Is Not Available Or Already Sold!"
            successPurchaseItem = "You Have Successfully Purchased The Item"

            itemID = eItemID.get()

            if checkoutItem(username, itemID):

                messagebox.showinfo("Information", successPurchaseItem)
                controller.show_frame("ItemPurchase")
            else:
                messagebox.showerror("Information", itemNotAvailable)


class CustomerProductSearch(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Product Search", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        categoryList = ["-", "Lights", "Locks"]
        labelCategory = tk.Label(
            self, text="Select Category", fg=controller.priColor, bg=controller.base, font=controller.standard)
        categoryBox = ttk.Combobox(
            self, values=categoryList, height=3, width=25)
        categoryBox.set("-")

        labelOr = tk.Label(self, text="AND / OR", fg=controller.priColor,
                           bg=controller.base, font=controller.standard)

        labelModel = tk.Label(self, text="Select Model",
                              fg=controller.priColor, bg=controller.base, font=controller.standard)

        modelList = ["-", "Light1", "Light2",
                     "Safe1", "Safe2", "Safe3", "SmartHome1"]
        modelBox = ttk.Combobox(self, values=modelList, height=3, width=25)
        modelBox.set("-")

        labelAdd = tk.Label(self, text="Additional Filters",
                            fg=controller.priColor, bg=controller.base, font=controller.standard)

        labelPrice = tk.Label(self, text="Select Price",
                              fg=controller.priColor, bg=controller.base, font=controller.standard)

        priceList = ["-", "Below $100", "$100-$150", "$150-$200", "Above $200"]
        priceBox = ttk.Combobox(self, values=priceList, height=3, width=25)
        priceBox.set("-")

        labelWarranty = tk.Label(
            self, text="Select Warranty Length (Months)", fg=controller.priColor, bg=controller.base, font=controller.standard)

        warrantyList = ["-", 6, 8, 10, 12]
        warrantyBox = ttk.Combobox(
            self, values=warrantyList, height=3, width=25)
        warrantyBox.set("-")

        labelColour = tk.Label(self, text="Select Colour",
                               fg=controller.priColor, bg=controller.base, font=controller.standard)

        colourList = ["-", "White", "Blue", "Yellow", "Green", "Black"]
        colourBox = ttk.Combobox(self, values=colourList, height=3, width=25)
        colourBox.set("-")

        labelFactory = tk.Label(
            self, text="Select Factory", fg=controller.priColor, bg=controller.base, font=controller.standard)

        factoryList = ["-", "Malaysia", "China", "Philippines"]
        factoryBox = ttk.Combobox(self, values=factoryList, height=3, width=25)
        factoryBox.set("-")

        labelProduction = tk.Label(
            self, text="Select Production Year", fg=controller.priColor, bg=controller.base, font=controller.standard)

        yearList = ["-", "2014", "2015", "2016", "2017", "2019", "2020"]
        yearBox = ttk.Combobox(self, values=yearList, height=3, width=25)
        yearBox.set("-")

        submitButton = tk.Button(self, text="Submit", font=controller.button_font, fg=controller.button_fontColor, height="3", width="20",
                                 command=lambda: doSearchProduct())

        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("SearchTypes"), height="2", width="10")

        labelCategory.pack()
        categoryBox.pack()
        labelOr.pack()
        labelModel.pack()
        modelBox.pack()
        labelAdd.pack(padx=20, pady=20)
        labelPrice.pack()
        priceBox.pack()
        labelWarranty.pack()
        warrantyBox.pack()
        labelColour.pack()
        colourBox.pack()
        labelFactory.pack()
        factoryBox.pack()
        labelProduction.pack()
        yearBox.pack()

        submitButton.pack(pady=10)
        exitButton.pack()
        exitButton.place(x=10, y=50)

        def doSearchProduct():
            print(modelBox.get())
            # controller.show_frame("SearchResults")
            results = advancedSearch(username, categoryBox.get(), modelBox.get(
            ), priceBox.get(), warrantyBox.get(), colourBox.get(), "-", factoryBox.get(), yearBox.get())
            win = tk.Toplevel()
            win.wm_title("Search Results")
            print(results)

            if results is None:
                tk.Label(win, text="No Results Found", fg=controller.priColor,
                         bg=controller.base).pack(padx=200, pady=200)
            else:
                cols = list(results.columns)
                tree = ttk.Treeview(win)
                tree["columns"] = cols
                for i in cols:
                    tree.column(i, anchor="w")
                    tree.heading(i, text=i, anchor='w')
                for index, row in results.iterrows():
                    tree.insert("", "end", text=index+1, values=list(row))
                    tree.pack()


class SearchTypes(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Search Types", bg=controller.priColor, fg=controller.base,
                         width="10", height="2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        ProductSearchButton = tk.Button(self, text="Product Search", font=controller.button_font, fg=controller.button_fontColor,
                                        command=lambda: controller.show_frame("CustomerProductSearch"), height="3", width="20")
        ProductSearchButton.pack(pady=10)

        IndividualSearchButton = tk.Button(self, text="Individual Search", font=controller.button_font, fg=controller.button_fontColor,
                                           command=lambda: controller.show_frame("IndividualSearch"), height="3", width="20")
        IndividualSearchButton.pack(pady=10)

        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("CustDash"), height="2", width="10")
        exitButton.pack(pady=10)
        exitButton.place(x=10, y=50)


class IndividualSearch(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Search An Individual Item", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        categoryList = ["-", "Lights", "Locks"]
        labelCategory = tk.Label(
            self, text="Select Category", fg=controller.priColor, bg=controller.base, font=controller.standard)
        categoryBox = ttk.Combobox(
            self, values=categoryList, height=3, width=25)
        categoryBox.set("-")

        labelOr = tk.Label(
            self, text="OR", fg=controller.priColor, bg=controller.base, font=controller.standard)

        labelModel = tk.Label(self, text="Select Model",
                              fg=controller.priColor, bg=controller.base, font=controller.standard)

        modelList = ["-", "Light1", "Light2",
                     "Safe1", "Safe2", "Safe3", "SmartHome1"]
        modelBox = ttk.Combobox(self, values=modelList, height=3, width=25)
        modelBox.set("-")

        labelColour = tk.Label(self, text="Select Colour",
                               fg=controller.priColor, bg=controller.base, font=controller.standard)

        colourList = ["-", "White", "Blue", "Yellow", "Green", "Black"]
        colourBox = ttk.Combobox(self, values=colourList, height=3, width=25)
        colourBox.set("-")

        labelWarranty = tk.Label(
            self, text="Select Warranty Length (Months)", fg=controller.priColor, bg=controller.base, font=controller.standard)

        warrantyList = ["-", 6, 8, 10, 12]
        warrantyBox = ttk.Combobox(
            self, values=warrantyList, height=3, width=25)
        warrantyBox.set("-")

        labelSupply = tk.Label(
            self, text="Select Power Supply", fg=controller.priColor, bg=controller.base, font=controller.standard)

        powerList = ["-", "Battery", "USB"]
        powerBox = ttk.Combobox(self, values=powerList, height=3, width=25)
        powerBox.set("-")

        labelFactory = tk.Label(
            self, text="Select Factory", fg=controller.priColor, bg=controller.base, font=controller.standard)

        factoryList = ["-", "Malaysia", "China", "Philippines"]
        factoryBox = ttk.Combobox(self, values=factoryList, height=3, width=25)
        factoryBox.set("-")

        labelProduction = tk.Label(
            self, text="Select Production Year", fg=controller.priColor, bg=controller.base, font=controller.standard)

        yearList = ["-", "2014", "2015", "2016", "2017", "2019", "2020"]
        yearBox = ttk.Combobox(self, values=yearList, height=3, width=25)
        yearBox.set("-")

        SubmitButton = tk.Button(self, text="Submit", font=controller.button_font, fg=controller.button_fontColor, height="3", width="20",
                                 command=lambda: doSearchItem())

        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("SearchTypes"), height="2", width="10")

        labelCategory.pack()
        categoryBox.pack()
        labelOr.pack()
        labelModel.pack()
        modelBox.pack()
        labelColour.pack()
        colourBox.pack()
        labelWarranty.pack()
        warrantyBox.pack()
        labelSupply.pack()
        powerBox.pack()
        labelFactory.pack()
        factoryBox.pack()
        labelProduction.pack()
        yearBox.pack()
        SubmitButton.pack(pady=10)
        exitButton.pack()
        exitButton.place(x=10, y=50)

        def doSearchItem():
            print(modelBox.get())
            # controller.show_frame("SearchResults")
            results = searchItem(categoryBox.get(), modelBox.get(
            ), colourBox.get(), warrantyBox.get(), powerBox.get(), factoryBox.get(), yearBox.get())
            win = tk.Toplevel()
            win.wm_title("Search Results")
            print(results)

            if results is None:
                tk.Label(win, text="No Results Found", fg=controller.priColor,
                         bg=controller.base).pack(padx=200, pady=200)
            else:
                cols = list(results.columns)
                tree = ttk.Treeview(win)
                tree["columns"] = cols
                for i in cols:
                    tree.column(i, anchor="w")
                    tree.heading(i, text=i, anchor='w')
                for index, row in results.iterrows():
                    tree.insert("", "end", values=list(row))
                    tree.pack()


class Request(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Request", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        newRequestButton = tk.Button(self, text="Submit New Request", font=controller.button_font, fg=controller.button_fontColor,
                                     command=lambda: controller.show_frame("NewRequest"), height="3", width="20")
        checkRequestButton = tk.Button(self, text="Check Request Status", font=controller.button_font, fg=controller.button_fontColor,
                                       command=lambda: controller.show_frame("CheckRequest"), height="3", width="20")
        cancelRequestButton = tk.Button(self, text="Cancel Request", font=controller.button_font, fg=controller.button_fontColor,
                                        command=lambda: controller.show_frame("CancelRequest"), height="3", width="20")
        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("CustDash"), height="2", width="10")
        checkRequestButton.pack(pady=10)
        newRequestButton.pack(pady=10)
        cancelRequestButton.pack(pady=10)
        exitButton.pack()
        exitButton.place(x=10, y=50)


class NewRequest(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Submit New Request", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        tk.Label(self, text="Enter Item ID", fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
            side="top", fill="x", pady=10)
        eItem = tk.Entry(self, width=45, cursor="xterm")
        eItem.pack()

        requestButton = tk.Button(self, text="View Items Purchased", font=controller.button_font, fg=controller.button_fontColor,
                                  command=lambda: checkForItems(), height="3", width="20")
        requestButton.pack(pady=10)

        def checkForItems():

            tuple_list = getPurchasedItems(username)

            if tuple_list == []:
                label = tk.Label(self, text="No Items Have Been Purchased", font=controller.label_font,
                                 fg=controller.priColor, bg=controller.base)
                label.pack(side="top", fill="x", pady=10)

            else:
                results = pd.DataFrame(tuple_list, columns=["Item ID"])

                cols = list(results.columns)
                tree = ttk.Treeview(self)

                tree["columns"] = cols
                for i in cols:
                    tree.column(i, anchor="w")
                    tree.heading(i, text=i, anchor='w')
                for index, row in results.iterrows():
                    tree.insert("", "end", text=index+1, values=list(row))
                    tree.pack()

        def submitNewService(itemID):

            if requestForService(username, str(itemID)):
                label = tk.Label(
                    self, text="Request Successfully Submitted For Item " + itemID, fg=controller.priColor, bg=controller.base,
                    font=controller.label_font)
                label.pack(side="top", fill="x", pady=10)

            else:
                label = tk.Label(self, text="Invalid Request OR Request Has Already Been Submitted",
                                 fg=controller.priColor, bg=controller.base, font=controller.label_font)
                label.pack(side="top", fill="x", pady=10)

        def callSubmitNewService():
            itemID = eItem.get()
            submitNewService(itemID)

        submitButton = tk.Button(self, text="Submit Request", font=controller.button_font, fg=controller.button_fontColor,
                                 command=lambda: callSubmitNewService(), height="3", width="20")
        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("Request"), height="2", width="10")
        submitButton.pack(pady=10)
        exitButton.pack()
        exitButton.place(x=10, y=50)


class CheckRequest(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Check Request Status", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        newRequestButton = tk.Button(self, text="Get Requests", font=controller.button_font, fg=controller.button_fontColor, height="3", width="20",
                                     command=lambda: getRequests())
        newRequestButton.pack(pady=10)

        def getRequests():
            tuple_list = printItemServicingList(username)

            if tuple_list == []:
                label = tk.Label(self, text="There Are No Requests Submitted", font=controller.label_font,
                                 fg=controller.priColor, bg=controller.base)
                label.pack(side="top", fill="x", pady=10)

            else:
                results = pd.DataFrame(tuple_list, columns=[
                    "Item ID", "Request Status"])
                cols = list(results.columns)
                tree = ttk.Treeview(self)

                tree["columns"] = cols
                for i in cols:
                    tree.column(i, anchor="w")
                    tree.heading(i, text=i, anchor='w')
                for index, row in results.iterrows():
                    tree.insert("", "end", text=index+1, values=list(row))
                    tree.pack()

        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("Request"), height="2", width="10")
        exitButton.pack()
        exitButton.place(x=10, y=50)

        def sequence(*functions):
            def func(*args, **kwargs):
                return_value = None
                for function in functions:
                    return_value = function(*args, **kwargs)
                return return_value
            return func


class CancelRequest(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Cancel Request", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        tk.Label(self, text="Enter Request ID", fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
            side="top", fill="x", pady=10)
        eRequest = tk.Entry(self, width=45, cursor="xterm")
        eRequest.pack()

        viewRequestButton = tk.Button(self, text="View Requests", font=controller.button_font, fg=controller.button_fontColor, height="3", width="20",
                                      command=lambda: getRequests())
        viewRequestButton.pack(pady=10)

        def getRequests():
            tuple_list = printItemIDServicingList(username)

            if tuple_list == []:
                label = tk.Label(self, text="There Are No Requests Submitted", font=controller.label_font,
                                 fg=controller.priColor, bg=controller.base)
                label.pack(side="top", fill="x", pady=10)

            else:
                results = pd.DataFrame(tuple_list, columns=[
                    "Request ID", "Request Status", "Item ID"])
                cols = list(results.columns)
                tree = ttk.Treeview(self)

                tree["columns"] = cols
                for i in cols:
                    tree.column(i, anchor="w")
                    tree.heading(i, text=i, anchor='w')
                for index, row in results.iterrows():
                    tree.insert("", "end", text=index+1, values=list(row))
                    tree.pack()

        def cancelExistRequest(RequestID):

            if cancelRequest(username, RequestID):
                label = tk.Label(
                    self, text="Request " + RequestID + " Successfully Cancelled", bg=controller.base, fg=controller.priColor, font=controller.label_font)
                label.pack(side="top", fill="x", pady=10)

            else:
                label = tk.Label(
                    self, text="Currently No Pending Requests For Item", bg=controller.base, fg=controller.priColor, font=controller.label_font)
                label.pack(side="top", fill="x", pady=10)

        def callCancelRequest():
            RequestID = eRequest.get()
            cancelExistRequest(RequestID)

        submitButton = tk.Button(self, text="Cancel Request", font=controller.button_font, fg=controller.button_fontColor, height="3", width="20",
                                 command=lambda: callCancelRequest())
        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("Request"), height="2", width="10")
        submitButton.pack(pady=10)
        exitButton.pack()
        exitButton.place(x=10, y=50)


class Service(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Service Payment", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        tk.Label(self, text="Enter Request ID", fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
            side="top", fill="x", pady=10)
        eRequest = tk.Entry(self, width=45, cursor="xterm")
        eRequest.pack()

        serviceButton = tk.Button(self, text="View Items Under Service", command=lambda: checkForService(),
                                  font=controller.button_font, fg=controller.button_fontColor, height="3", width="30")
        serviceButton.pack(pady=10)

        def checkForService():

            tuple_list = printServicePayment(username)
            if tuple_list == []:
                label = tk.Label(self, text="There Are No Requests Pending Payment", font=controller.label_font,
                                 fg=controller.priColor, bg=controller.base)
                label.pack(side="top", fill="x", pady=10)

            else:
                results = pd.DataFrame(tuple_list, columns=[
                    "Request ID", "Due Date", "Service Fee Amount"])

                cols = list(results.columns)
                tree = ttk.Treeview(self)
                tree["columns"] = cols
                for i in cols:
                    tree.column(i, anchor="w")
                    tree.heading(i, text=i, anchor='w')
                for index, row in results.iterrows():
                    tree.insert("", "end", text=index+1, values=list(row))
                    tree.pack()

        def submitNewService(requestID):

            if payingServicePayment(username, requestID):
                label = tk.Label(
                    self, text="Service Fee Payment Success", fg=controller.priColor, bg=controller.base, font=controller.label_font)
                label.pack(side="top", fill="x", pady=10)

            else:
                label = tk.Label(self, text="Invalid Service Request",
                                 fg=controller.priColor, bg=controller.base, font=controller.label_font)
                label.pack(side="top", fill="x", pady=10)

        def callSubmitNewService():
            requestID = eRequest.get()
            submitNewService(requestID)

        submitButton = tk.Button(self, text="Submit Payment", font=controller.button_font, fg=controller.button_fontColor, height="3", width="20",
                                 command=lambda: callSubmitNewService())
        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("CustDash"), height="2", width="10")
        submitButton.pack(pady=10)
        exitButton.pack()
        exitButton.place(x=10, y=50)
