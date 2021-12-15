from tkinter import font as tkfont
from tkinter import ttk
from tkinter import *
from customer import *
from utilities import *
from tkinter import messagebox
from customerView import *
from administratorView import *


class Oshes(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(
            family='Helvetica', size=40, weight="bold")  # slant="italic"
        self.header_font = tkfont.Font(
            family='Helvetica', size=20, weight="bold")

        self.button_font = tkfont.Font(
            family='Helvetica', size=16, weight="bold")

        self.label_font = tkfont.Font(
            family='Helvetica', size=16, weight="bold")

        self.standard = tkfont.Font(
            family='Helvetica', size=8, weight="bold")

        self.button_fontColor = "#243E36"

        self.priColor = "#3d6358"
        self.secColor = "#7CA982"
        self.base = "#d6e7ca"

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for P in (StartPage, AdminCustomerSignUp, CustomerSignUpPage, AdminSignUpPage,
                  AdminCustomerSignIn, AdminSignInPage, CustomerSignInPage,
                  CustDash, ItemPurchase, CustomerProductSearch, AdminProductSearch,
                  Request, NewRequest, CheckRequest, CancelRequest,
                  Service, IndividualSearch, SearchTypes, AdminSearchTypes,
                  AdminDash, AdminItemIDSearch, ViewInventory,
                  ManageServices, AdminRequest, ServiceList, SelfServiceList, PendingServiceFee,
                  CheckSales):
            page_name = P.__name__
            frame = P(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")


    def show_frame(self, page_name):
        # show the page for each page
        frame = self.frames[page_name]
        frame.config(background=self.base)
        frame.tkraise()

    def popWin(message, header, button):
        win = Toplevel()
        win.title(header)
        Label(win, text=message, fg="#243E36", bg="#7CA982").pack()
        win.configure(background="#f1f7ed")
        Button(win, text=button, command=win.destroy).pack()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to OSHES System", bg=controller.priColor,
                         fg=controller.base, width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        signup = tk.Button(self, text="Sign Up", font=controller.button_font, fg=controller.button_fontColor,
                           command=lambda: controller.show_frame("AdminCustomerSignUp"), height="3", width="20")
        signin = tk.Button(self, text="Sign In", font=controller.button_font, fg=controller.button_fontColor,
                           command=lambda: controller.show_frame("AdminCustomerSignIn"), height="3", width="20")
        signup.pack(pady=10)
        signin.pack(pady=10)


class AdminCustomerSignUp(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="I am a", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        customerSignUpButton = tk.Button(self, text="Customer", font=controller.button_font, fg=controller.button_fontColor,
                                         command=lambda: controller.show_frame("CustomerSignUpPage"), height="3", width="20")
        adminSignUpButton = tk.Button(self, text="Admin", font=controller.button_font, fg=controller.button_fontColor,
                                      command=lambda: controller.show_frame("AdminSignUpPage"), height="3", width="20")
        backButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.button_fontColor,
                               command=lambda: controller.show_frame("StartPage"), height="3", width="20")
        customerSignUpButton.pack(pady=10)
        adminSignUpButton.pack(pady=10)
        backButton.pack(pady=10)


class AdminCustomerSignIn(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="I Am A", bg=controller.priColor, fg=controller.base,
                         width="300", height="3", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        customerSignUpButton = tk.Button(self, text="Customer", font=controller.button_font, fg=controller.button_fontColor,
                                         command=lambda: controller.show_frame("CustomerSignInPage"), height="3", width="20")
        adminSignUpButton = tk.Button(self, text="Admin", font=controller.button_font, fg=controller.button_fontColor,
                                      command=lambda: controller.show_frame("AdminSignInPage"), height="3", width="20")
        backButton = tk.Button(self, text="Back", font=controller.button_font, fg=controller.button_fontColor,
                               command=lambda: controller.show_frame("StartPage"), height="3", width="20")
        customerSignUpButton.pack(pady=10)
        adminSignUpButton.pack(pady=10)
        backButton.pack(pady=10)


if __name__ == "__main__":
    Oshes().mainloop()
