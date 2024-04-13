from tkinter import *
from tkinter import messagebox
from tkinter_widgets import TkinterWidgets
from pw_generator import pw_gen
import pyperclip
import json
BUTTON_FONT = ("Arial", 10, 'normal')
LABEL_FONT = ("Courier", 10, 'normal')
IMAGE_PATH = "logo.png"
DEFAULT_EMAIL_PATH = "default_email.txt"
OUTPUT_PATH = "passwords.json"


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
        self.load_default_email()

        # main loop
        self.window.mainloop()
    def create_canvas(self):
        # create canvas with logo image
        canvas = Canvas(width=200, height=200)
        canvas.create_image(100, 100, image=self.logo_image)
        canvas.grid(row=0, column=1)

        self.widgets.add_canvas("canvas", canvas)

    def create_labels(self):
        label_1 = Label(text="Website:", font=LABEL_FONT)
        label_2 = Label(text="Email/Username:", font=LABEL_FONT)
        label_3 = Label(text="Password:", font=LABEL_FONT)
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
        entry_1 = Entry(width=30)
        entry_1.focus()
        entry_2 = Entry(width=50)

        entry_3 = Entry(width=30)
        entry_1.grid(row=1, column=1)
        entry_2.grid(row=2, column=1, columnspan=2)
        entry_3.grid(row=3, column=1)

        entry_dict={
            "website": entry_1,
            "email": entry_2,
            "password": entry_3,
        }

        self.widgets.add_entry_dict(entry_dict)

    def create_buttons(self):

        button_1 = Button(text="Generate Password", width=14, font=BUTTON_FONT, command=self.password_generator)
        button_2 = Button(text="Add", width=37, font=BUTTON_FONT, command=self.save_password)
        button_3 = Button(text="Search", width = 14, font=BUTTON_FONT, command=self.search)

        button_1.grid(row=3, column=2)
        button_2.grid(row=4, column=1, columnspan=2)
        button_3.grid(row=1, column=2)

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

        data = {
            website_text: {
                "email": email_text,
                "password": password_text,
            },
        }

        if website_text == "" or password_text == "" or email_text == "":
            messagebox.showwarning(title="Empty Fields", message="Please don't leave any fields empty")

        else:
            is_okay = messagebox.askokcancel(title=website_text, message=f"The following are your details:\n"
                                         f"Email: {email_text}\nPassword: {password_text}\n\nDo you want to proceed?")

            if is_okay:
                try:
                    with open(OUTPUT_PATH, mode='r') as file:
                            json_data = json.load(file)
                            json_data.update(data)
                except json.decoder.JSONDecodeError:
                    json_data = data

                except FileNotFoundError:
                    messagebox.showinfo(title="Information!", message="Created json file.")
                    json_data = data

                with open(OUTPUT_PATH, mode='w') as file:
                    json.dump(json_data, file, indent=4)

                website_entry.delete(0, END)
                password_entry.delete(0, END)

    def password_generator(self):
        password = pw_gen()
        password_entry = self.widgets.get_entries("password")
        password_entry.delete(0, END)
        password_entry.insert(0, password)

        pyperclip.copy(password)
        messagebox.showinfo(title="Password Copied", message="Your password has been copied to your clipboard")

    def search(self):
        website = self.widgets.get_entries("website").get()

        try:
            with open(OUTPUT_PATH, mode="r") as json_file:
                json_data = json.load(json_file)

        except FileNotFoundError:
            messagebox.showwarning(title="Error",
                                   message="Sorry, we could not find the json file, please add some data to create one.")

        except json.decoder.JSONDecodeError:
            messagebox.showwarning(title="Error",
                                   message="Sorry, your data is empty, please add some data.")

        else:
            if website in json_data:
                email = json_data[website]["email"]
                password = json_data[website]["password"]
                messagebox.showinfo(title=f"{website} Data", message=f"Email: {email}\nPassword: {password}")
            else:
                messagebox.showwarning(title="Error",
                                       message=f"Sorry, we could not find data for {website}. Please check for spelling "
                                               "errors and try again.")

    def load_default_email(self):
        email_entry = self.widgets.get_entries("email")

        try:
            with open(DEFAULT_EMAIL_PATH, 'r') as file:
                email_entry.insert(0, file.read())

        except FileNotFoundError:
            with open(DEFAULT_EMAIL_PATH, mode='w') as file:
                file.write("example@gmail.com")

            with open(DEFAULT_EMAIL_PATH, 'r') as file:
                email_entry.insert(0, file.read())

            messagebox.showwarning(title="Warning",
                                   message="Default email is example@gmail.com by default. To change this, edit the "
                                           "default_email.txt file. You can also leave it blank.")
