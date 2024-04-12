from tkinter import *
from tkinter import messagebox
from tkinter_widgets import TkinterWidgets
from pw_generator import pw_gen
import pyperclip
IMAGE_PATH = "logo.png"
DEFAULT_EMAIL_PATH = "default_email.txt"
OUTPUT_PATH = "passwords.txt"


class PasswordManager:
    def __init__(self):
        # create window and images
        self.window = Tk()
        self.window.title("Password Manager")
        self.window.config(padx=50, pady=50)
        self.logo_image = PhotoImage(file=IMAGE_PATH)

        # create widgets
        self.widgets = TkinterWidgets()
        self.create_canvas()
        self.create_labels()
        self.create_entries()
        self.create_buttons()

        # main loop
        self.window.mainloop()
    def create_canvas(self):
        # create canvas with logo image
        canvas = Canvas(width=200, height=200)
        canvas.create_image(100, 100, image=self.logo_image)
        canvas.grid(row=0, column=1)

        self.widgets.add_canvas("canvas", canvas)

    def create_labels(self):
        label_1 = Label(text="Website:", font=("Courier", 10, 'normal'))
        label_2 = Label(text="Email/Username:", font=("Courier", 10, 'normal'))
        label_3 = Label(text="Password:", font=("Courier", 10, 'normal'))
        label_1.grid(row=1, column=0)
        label_2.grid(row=2, column=0)
        label_3.grid(row=3, column=0)

        label_dict = {
            "website prompt: ": label_1,
            "email prompt": label_2,
            "password prompt": label_3,
        }

        self.widgets.add_label_dict(label_dict)

    def create_entries(self):
        entry_1 = Entry(width=50)
        entry_1.focus()
        entry_2 = Entry(width=50)
        with open(DEFAULT_EMAIL_PATH, 'r') as file:
            entry_2.insert(0, file.read())

        entry_3 = Entry(width=30)
        entry_1.grid(row=1, column=1, columnspan=2)
        entry_2.grid(row=2, column=1, columnspan=2)
        entry_3.grid(row=3, column=1)

        entry_dict={
            "website": entry_1,
            "email": entry_2,
            "password": entry_3,
        }

        self.widgets.add_entry_dict(entry_dict)

    def create_buttons(self):
        button_1 = Button(text="Generate Password", width=14, font=("Arial", 10, 'normal'), command=self.password_generator)
        button_2 = Button(text="Add", width=37, font=("Arial", 10, 'normal'), command=self.save_password)

        button_1.grid(row=3, column=2)
        button_2.grid(row=4, column=1, columnspan=2)

        button_dict = {
            "generate": button_1,
            "add": button_2,
        }

        self.widgets.add_button_dict(button_dict)

    def save_password(self):
        entry_dict = self.widgets.get_entries()

        website_entry = entry_dict["website"]
        email_entry = entry_dict["email"]
        password_entry = entry_dict["password"]

        website_text = website_entry.get()
        email_text = email_entry.get()
        password_text = password_entry.get()

        if website_text == "" or password_text == "" or email_text == "":
            messagebox.showwarning(title="Empty Fields", message="Please don't leave any fields empty")

        else:
            is_okay = messagebox.askokcancel(title=website_text, message=f"The following are your details:\n"
                                         f"Email: {email_text}\nPassword: {password_text}\n\nDo you want to proceed?")

            if is_okay:
                with open(OUTPUT_PATH, mode='a') as file:
                    file.write(f"==== {website_text} ====\nEmail: {email_text}\nPassword: {password_text}\n\n")

                website_entry.delete(0, END)
                password_entry.delete(0, END)

    def password_generator(self):
        password = pw_gen()
        password_entry = self.widgets.get_entries("password")
        password_entry.delete(0, END)
        password_entry.insert(0, password)

        pyperclip.copy(password)
        messagebox.showinfo(title="Password Copied", message="Your password has been copied to your clipboard")
