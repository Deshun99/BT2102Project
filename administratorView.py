from userDetails import UserDetails
from administrator import *
from tkinter import font as tkfont
from tkinter import ttk
from tkinter import *

from customer import *
from utilities import *
from oshes import *

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option("display.max_rows", None)


class AdminSearchTypes(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Search Types", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        ProductSearchButton = tk.Button(self, text="Search By Product or Model", font=controller.button_font, fg=controller.button_fontColor,
                                        command=lambda: controller.show_frame("AdminProductSearch"), height="3", width="30")
        ProductSearchButton.pack(pady=10)

        ItemIDSearchButton = tk.Button(self, text="Search by Item ID", font=controller.button_font, fg=controller.button_fontColor,
                                       command=lambda: controller.show_frame("AdminItemIDSearch"), height="3", width="30")
        ItemIDSearchButton.pack(pady=10)

        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("AdminDash"), height="2", width="10")
        exitButton.pack()
        exitButton.place(x=10, y=50)


class AdminDash(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Dashboard", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        productSearchButton = tk.Button(self, text="Search", font=controller.button_font, fg=controller.button_fontColor,
                                        command=lambda: controller.show_frame("AdminSearchTypes"), height="3", width="20")
        viewInventoryButton = tk.Button(self, text="View Inventory", font=controller.button_font, fg=controller.button_fontColor,
                                        command=lambda: controller.show_frame("ViewInventory"), height="3", width="20")
        manageServicesButton = tk.Button(self, text="Manage Services", font=controller.button_font, fg=controller.button_fontColor,
                                         command=lambda: controller.show_frame("ManageServices"), height="3", width="20")
        checkSalesButton = tk.Button(self, text="Check Sales", font=controller.button_font, fg=controller.button_fontColor,
                                     command=lambda: controller.show_frame("CheckSales"), height="3", width="20")
        exitButton = tk.Button(self, text="Exit", font=controller.button_font, fg=controller.button_fontColor,
                               command=lambda: controller.show_frame("StartPage"), height="3", width="20")

        productSearchButton.pack(pady=10)
        viewInventoryButton.pack(pady=10)
        manageServicesButton.pack(pady=10)
        checkSalesButton.pack(pady=10)
        exitButton.pack(pady=10)


class AdminSignUpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Create Admin Account", bg=controller.priColor,
                         fg=controller.base, width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        tk.Label(self, text="Username", fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
            side="top", fill="x", pady=10)
        eUser = Entry(self, width=35)
        eUser.insert(0, "")
        eUser.pack()

        tk.Label(self, text="Name", fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
            side="top", fill="x", pady=10)
        eName = Entry(self, width=35)
        eName.insert(0, "")
        eName.pack()

        tk.Label(self, text="Phone Number", fg=controller.priColor, bg=controller.base,
                 font=controller.header_font).pack(side="top", fill="x", pady=10)
        ePhone = Entry(self, width=35)
        ePhone.insert(0, "")
        ePhone.pack()

        tk.Label(self, text="Gender", fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
            side="top", fill="x", pady=10)
        # eGender = Entry(self, width=35)
        # eGender.insert(0, "")
        genderList = ["-", "M", "F"]
        eGender = ttk.Combobox(self, values=genderList, height=3, width=35)
        eGender.set("-")
        eGender.pack()

        tk.Label(self, text="Password", fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
            side="top", fill="x", pady=10)
        ePW = Entry(self, width=35)
        ePW.insert(0, "")
        ePW.pack()

        tk.Label(self, text="Confirm Password", fg=controller.priColor, bg=controller.base,
                 font=controller.header_font).pack(side="top", fill="x", pady=10)
        eCPW = Entry(self, width=35)
        eCPW.insert(0, "")
        eCPW.pack()

        tk.Label(self, text=" ", bg=controller.base).pack()

        enterButton = tk.Button(self, text="Enter", font=controller.button_font, fg=controller.button_fontColor,
                                command=lambda: adminSignUp(), height="3", width="20")
        enterButton.pack(pady=10)

        backButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("AdminCustomerSignUp"), height="2", width="10")
        backButton.pack(pady=10)
        backButton.place(x=10, y=50)

        def adminSignUp():
            userIDisUsed = "AdministratorID Is Already Taken Please Select A Different AdministratorID"
            successRegistered = "Successfully Registered As An Administrator"
            notRegistered = "UserID Or Password Is Invalid"

            username = eUser.get()
            name = eName.get()
            password = ePW.get()
            cPassword = eCPW.get()
            gender = eGender.get()
            phone = ePhone.get()

            if password == cPassword and password != empty:
                if registerAdministrator(username, name, password, gender, phone):
                    print(successRegistered)

                    controller.show_frame("AdminSignInPage")
                    messagebox.showinfo(
                        "Registration Successful", "Registration Successful!")
                else:
                    print(userIDisUsed)
                    messagebox.showerror(
                        "Information", "Username Has Been Taken")
            else:
                print(notRegistered)
                messagebox.showerror(
                    "Information", "Passwords Do Not Match, Please Try Again")


class AdminSignInPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Sign In", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        tk.Label(self, text="Username ID", fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
            side="top", fill="x", pady=10)
        eUser = Entry(self, width=35)
        eUser.insert(0, "")
        eUser.pack()

        tk.Label(self, text="Password", fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
            side="top", fill="x", pady=10)
        ePW = Entry(self, width=35)
        ePW.insert(0, "")
        ePW.pack()

        tk.Label(self, text=" ", fg=controller.priColor,
                 bg=controller.base).pack()

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
            successRegistered = "Login Successfully As An Admin"
            global username
            username = eUser.get()
            password = ePW.get()

            UserDetails(username)

            if loginAdministrator(username, password):
                print(successRegistered)
                tk.Label(self, text=successRegistered, fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
                    side="top", fill="x", pady=10)
                messagebox.showinfo("Information", "Login Successful!")
                controller.show_frame("AdminDash")
            else:
                print(notRegistered)
                messagebox.showerror("Information", "Login failed")


class AdminProductSearch(tk.Frame):

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

        labelOr = tk.Label(
            self, text="AND / OR", fg=controller.priColor, bg=controller.base, font=controller.standard)

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
                               command=lambda: controller.show_frame("AdminSearchTypes"), height="2", width="10")

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
                         bg=controller.base,).pack(padx=200, pady=200)
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


class AdminItemIDSearch(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Search by Item ID", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        tk.Label(self, text="Enter Item ID", fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
            side="top", fill="x", pady=10)
        eLabel = tk.Entry(self, width=45, cursor="xterm")
        eLabel.pack()

        goButton = tk.Button(self, text="Go", font=controller.button_font, fg=controller.button_fontColor, height="3", width="20",
                             command=lambda: doItemSearch())
        goButton.pack(pady=10)

        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("AdminSearchTypes"), height="2", width="10")
        exitButton.pack()
        exitButton.place(x=10, y=50)

        def doItemSearch():
            itemID = eLabel.get()
            results = itemSearch(username, itemID)
            win = tk.Toplevel()
            win.wm_title("Search Results")

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


class ViewInventory(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="View Inventory", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        inventoryButton = tk.Button(self, text="Get Inventory", font=controller.button_font, fg=controller.button_fontColor, height="3", width="20",
                                    command=lambda: getInventory())
        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("AdminDash"), height="2", width="10")
        inventoryButton.pack(pady=10)
        exitButton.pack()
        exitButton.place(x=10, y=50)

        def getInventory():

            #win = tk.Toplevel()
            #win.wm_title("Search Results")
            tuple_list = printProductInventory()

            results = pd.DataFrame(tuple_list, columns=[
                                   "IID", "Number of 'SOLD' items", "Number of 'UNSOLD' items"])

            cols = list(results.columns)
            tree = ttk.Treeview(self)

            tree["columns"] = cols
            for i in cols:
                tree.column(i, anchor="w")
                tree.heading(i, text=i, anchor='w')
            for index, row in results.iterrows():
                tree.insert("", 'end', values=list(row))
                tree.pack()


class ManageServices(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Manage Services", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        viewRequestButton = tk.Button(self, text="View/Approve requests", font=controller.button_font, fg=controller.button_fontColor,
                                      command=lambda: controller.show_frame("AdminRequest"), height="3", width="20")
        viewServiceStatusButton = tk.Button(self, text="View All Items Under Service", font=controller.button_font, fg=controller.button_fontColor,
                                            command=lambda: controller.show_frame("ServiceList"), height="3", width="25")
        viewServiceSelfButton = tk.Button(self, text="View Items Serviced By Me", font=controller.button_font, fg=controller.button_fontColor,
                                          command=lambda: controller.show_frame("SelfServiceList"), height="3", width="25")
        pendingServiceFeeButton = tk.Button(self, text="Pending Service fee", font=controller.button_font, fg=controller.button_fontColor,
                                            command=lambda: controller.show_frame("PendingServiceFee"), height="3", width="25")
        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("AdminDash"), height="2", width="10")
        viewRequestButton.pack(pady=10)
        viewServiceStatusButton.pack(pady=10)
        viewServiceSelfButton.pack(pady=10)
        pendingServiceFeeButton.pack(pady=10)
        exitButton.pack()
        exitButton.place(x=10, y=50)


class AdminRequest(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="View/ Approve Request", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        tk.Label(self, text="Enter Request ID", fg=controller.priColor, bg=controller.base, font=controller.header_font).pack(
            side="top", fill="x", pady=10)
        eRequest = tk.Entry(self, width=45, cursor="xterm")
        eRequest.pack()

        requestButton = tk.Button(self, text="View Pending Requests",  command=lambda: checkForRequest(),
                                  font=controller.button_font, fg=controller.button_fontColor, height="3", width="20")
        requestButton.pack(pady=10)

        def checkForRequest():
            tuple_list = printPendingRequest()

            if tuple_list == []:
                label = tk.Label(self, text="There Are No Requests Submitted", font=controller.label_font,
                                 fg=controller.priColor, bg=controller.base)
                label.pack(side="top", fill="x", pady=10)

            else:
                results = pd.DataFrame(tuple_list, columns=[
                    "Request ID", "Request Status", "Item ID", "Customer ID"])
                cols = list(results.columns)
                tree = ttk.Treeview(self)

                tree["columns"] = cols
                for i in cols:
                    tree.column(i, anchor="w")
                    tree.heading(i, text=i, anchor='w')
                for index, row in results.iterrows():
                    tree.insert("", "end", text=index+1, values=list(row))
                    tree.pack()

        def approveNewRequest(requestID):

            if approveRequest(username, requestID):
                label = tk.Label(
                    self, text="Request Successfully Approved", fg=controller.priColor, bg=controller.base, font=controller.label_font)
                label.pack(side="top", fill="x", pady=10)

            else:
                label = tk.Label(self, text="Invalid Request Or Request Already Approved",
                                 fg=controller.priColor, bg=controller.base, font=controller.label_font)
                label.pack(side="top", fill="x", pady=10)

        def tryApproveRequest():
            requestID = eRequest.get()
            approveNewRequest(requestID)

        submitButton = tk.Button(self, text="Approve Request", font=controller.button_font, fg=controller.button_fontColor, height="3", width="20",
                                 command=lambda: tryApproveRequest())
        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("ManageServices"), height="2", width="10")
        submitButton.pack(pady=10)
        exitButton.pack()
        exitButton.place(x=10, y=50)


class ServiceList(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="View All Items Under Service", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        itemsButton = tk.Button(self, text="Items Under Service",  command=lambda: getItems(),
                                font=controller.button_font, fg=controller.button_fontColor, height="3", width="20")
        itemsButton.pack(pady=10)
        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("ManageServices"), height="2", width="10")
        exitButton.pack()
        exitButton.place(x=10, y=50)

        def getItems():

            tuple_list = printItemsUnderService()
            if tuple_list == False:
                label = tk.Label(self, text="There Are No Items Under Servicing",
                                 fg=controller.priColor, bg=controller.base, font=controller.label_font)
                label.pack(side="top", fill="x", pady=10)

            else:
                results = pd.DataFrame(tuple_list, columns=[
                    "Item ID", "Service Status"])
                cols = list(results.columns)
                tree = ttk.Treeview(self)

                tree["columns"] = cols
                for i in cols:
                    tree.column(i, anchor="w")
                    tree.heading(i, text=i, anchor='w')
                for index, row in results.iterrows():
                    tree.insert("", "end", text=index+1, values=list(row))
                    tree.pack()


class SelfServiceList(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="View Items Serviced By Me", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        itemsButton = tk.Button(self, text="Items Serviced By Me",  command=lambda: getServicedItems(),
                                font=controller.button_font, fg=controller.button_fontColor, height="3", width="20")
        itemsButton.pack(pady=10)
        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("ManageServices"), height="2", width="10")
        exitButton.pack()
        exitButton.place(x=10, y=50)

        def getServicedItems():

            tuple_list = printServicedItem(username)
            if tuple_list == []:

                label = tk.Label(self, text="No Items Serviced By Me",
                                 fg=controller.priColor, bg=controller.base, font=controller.label_font)
                label.pack(side="top", fill="x", pady=10)

            else:

                results = pd.DataFrame(tuple_list, columns=[
                                       "RequestID", "ItemID"])
                cols = list(results.columns)
                tree = ttk.Treeview(self)

                tree["columns"] = cols
                for i in cols:
                    tree.column(i, anchor="w")
                    tree.heading(i, text=i, anchor='w')
                for index, row in results.iterrows():
                    tree.insert("", "end", text=index+1, values=list(row))
                    tree.pack()


class PendingServiceFee(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Pending Service Fee", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        salesButton = tk.Button(self, text="Retrieve Customer List", font=controller.button_font, fg=controller.button_fontColor, height="3", width="20",
                                command=lambda: getCustomers())
        salesButton.pack(pady=10)
        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("ManageServices"), height="2", width="10")
        exitButton.pack()
        exitButton.place(x=10, y=50)

        def getCustomers():

            tuple_list = printCustomerUnpaidServiceFee()
            if tuple_list == []:

                label = tk.Label(self, text="There Are No Customers Pending Service Fee",
                                 fg=controller.priColor, bg=controller.base, font=controller.label_font)
                label.pack(side="top", fill="x", pady=10)

            else:

                results = pd.DataFrame(tuple_list, columns=[
                    "Customer ID", "Request ID"])
                cols = list(results.columns)
                tree = ttk.Treeview(self)

                tree["columns"] = cols
                for i in cols:
                    tree.column(i, anchor="w")
                    tree.heading(i, text=i, anchor='w')
                for index, row in results.iterrows():
                    tree.insert("", "end", text=index+1, values=list(row))
                    tree.pack()


class CheckSales(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Check Sales", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        salesButton = tk.Button(self, text="View Sold Items", font=controller.button_font, fg=controller.button_fontColor, height="3", width="20",
                                command=lambda: getSoldItems())
        salesButton.pack(pady=10)
        exitButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.base,
                               bg=controller.secColor,
                               command=lambda: controller.show_frame("AdminDash"), height="2", width="10")
        exitButton.pack()
        exitButton.place(x=10, y=50)

        def getSoldItems():

            tuple_list = printSoldProduct()
            results = pd.DataFrame(tuple_list, columns=[
                                   "Product ID", "Category", "Model", "Count(SOLD)"])
            cols = list(results.columns)
            tree = ttk.Treeview(self)

            tree["columns"] = cols
            for i in cols:
                tree.column(i, anchor="w")
                tree.heading(i, text=i, anchor='w')
            for index, row in results.iterrows():
                tree.insert("", "end", values=list(row))
                tree.pack()
