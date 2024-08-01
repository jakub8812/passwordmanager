from tkinter import Tk, Label, Button, Entry, Frame, END, Toplevel
from tkinter import ttk
from db_operations import DbOperation
import pyperclip

class root_window:
    """
    Klasa root_window zapewnia GUI do zarządzania hasłami przy użyciu Tkinter.
    """

    def __init__(self, root, db):
        """
        Inicjalizuje główne okno aplikacji.

        :param root: Obiekt Tkintera
        :param db: Obiekt DbOperation
        """
        self.db = db
        self.db.register_observer(self)
        self.root = root
        self.root.title("Password Manager")

        head_title = Label(self.root, text="Menadżer haseł", bg="lightgray", font=("Ariel", 20), padx=10, pady=10)
        head_title.pack(fill="x")

        window_width = 900
        window_height = 600

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        self.crud_frame = ttk.Frame(self.root)
        self.crud_frame.pack()
        self.create_entry_labels()
        self.create_entry_boxes()
        self.create_crud_buttons()
        self.search_entry = Entry(self.crud_frame, width=30)
        self.search_entry.grid(row=self.row_no, column=self.col_no)
        self.col_no += 1
        Button(self.crud_frame, text="Wyszukaj", bg="yellow", font=("Ariel", 12), command=self.search_record).grid(row=self.row_no, column=self.col_no, padx=5, pady=5)
        self.create_records_tree()

        self.password_dict = {}

    def update(self):
        self.show_records()

    def show_records(self):
        self.clear_tree()
        records_list = self.db.show_records()
        for record in records_list:
            password_placeholder = '*' * len(record[5]) if record[5] else ''
            self.records_tree.insert('', END, values=(record[0], record[3], record[4], password_placeholder))
            self.password_dict[record[0]] = record[5]

    def clear_tree(self):
        for i in self.records_tree.get_children():
            self.records_tree.delete(i)

    def copy_password(self):
        ID = int(self.entry_boxes[0].get())
        if ID in self.password_dict:
            password = self.password_dict[ID]
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            message = "Skopiowano do schowka"
            title = "copy"
        else:
            message = "Schowek jest pusty"
            title = "Error"
        
        self.showmessage(title_box=title, message=message)

    def create_entry_labels(self):
        self.col_no, self.row_no = 0, 0
        labels_info = ("ID", "Tytul", "Nazwa uzytkownika", "Haslo")
        for label_info in labels_info:
            Label(self.crud_frame, text=label_info, bg="grey", fg="white", font=("Ariel", 12), padx=5, pady=2, width=20).grid(row=self.row_no, column=self.col_no, padx=5, pady=2)
            self.col_no+=1

    def create_crud_buttons(self):
        self.row_no += 1
        self.col_no = 0
        buttons_info = (("Zapisz", "darkgreen", self.save_record), ("Aktualizuj", "blue", self.update_record), ("Usun", "red", self.delete_record), ("Skopiuj haslo", "green", self.copy_password), ('Pokaz wszystkie dane', 'purple', self.show_records))
        for button_info in buttons_info:
            if button_info[0] == 'Pokaz wszystkie dane':
                self.row_no += 1
                self.col_no = 0
            Button(self.crud_frame, text=button_info[0], bg=button_info[1], fg="white", font=("Ariel", 12), padx=5, pady=2, width=20, command=button_info[2]).grid(row=self.row_no, column=self.col_no, padx=5, pady=2)
            self.col_no += 1

    def create_entry_boxes(self):
        self.row_no+=1
        self.entry_boxes = []
        self.col_no = 0
        for i in range(4):
            show = ""
            if i == 3:
                show = "*"
            entry_box = Entry(self.crud_frame, width=25, background="lightgreen", font=("Ariel", 10), show=show)
            entry_box.grid(row=self.row_no, column=self.col_no, padx=5, pady=2)
            self.col_no+=1
            self.entry_boxes.append(entry_box)

    def save_record(self):
        title = self.entry_boxes[1].get()
        username = self.entry_boxes[2].get()
        password = self.entry_boxes[3].get()
        data = { 'title' : title, 'username' : username, 'password' : password}
        self.db.create_record(data)
        self.clear_tree()
        self.show_records()

    def delete_record(self):
        record_id = int(self.entry_boxes[0].get())  # Convert to int
        self.db.delete_record(record_id)
        self.clear_tree()
        self.show_records()

    def update_record(self):
        record_id = int(self.entry_boxes[0].get())
        updated_data = {
            'ID': record_id,
            'title': self.entry_boxes[1].get(),
            'username': self.entry_boxes[2].get(),
            'password': self.entry_boxes[3].get()
        }
        self.db.update_record(updated_data)
        self.clear_tree()
        self.show_records()

    def search_record(self):
        title = self.search_entry.get()
        self.clear_tree()
        records_list = self.db.search_records(title)
        for record in records_list:
            password_placeholder = '*' * len(record[5]) if record[5] else ''
            self.records_tree.insert('', END, values=(record[0], record[3], record[4], password_placeholder))
            self.password_dict[record[0]] = record[5]

    def create_records_tree(self):
        self.records_tree_frame = Frame(self.root)
        self.records_tree_frame.pack()  # Używamy pack zamiast grid
        columns = ('ID', 'Tytul', 'Nazwa uzytkownika', 'Haslo')
        self.records_tree = ttk.Treeview(self.records_tree_frame, columns=columns, show='headings')
        self.records_tree.heading('ID', text='ID')
        self.records_tree.heading('Tytul', text='Tytul')
        self.records_tree.heading('Nazwa uzytkownika', text='Nazwa uzytkownika')
        self.records_tree.heading('Haslo', text='Haslo')

        self.records_tree['displaycolumns'] = ('ID', 'Tytul', 'Nazwa uzytkownika', 'Haslo')

        def item_selected(event):
            for selected_item in self.records_tree.selection():
                item = self.records_tree.item(selected_item)
                record = item['values']
                for entry_box, item in zip(self.entry_boxes, record):
                    entry_box.delete(0, END)
                    entry_box.insert(0, item)

        self.records_tree.bind('<<TreeviewSelect>>', item_selected)

        self.records_tree.grid()

    def showmessage(self, title_box:str=None, message:str=None):
        TIME_TO_WAIT = 900
        root = Toplevel(self.root)
        background='green'
        if title_box == 'Error':
            background = "red"
        root.geometry('200x30+600+200')
        root.title(title_box)
        Label(root, text=message, background=background, font=('Ariel', 15), fg='white').pack(padx=4, pady=2)
        try:
            root.after(TIME_TO_WAIT, root.destroy)
        except Exception as e:
            print("Blad", e)

if __name__ == "__main__":
    db_class = DbOperation()
    db_class.create_table()
    
    root = Tk()
    root_class = root_window(root, db_class)
    root.mainloop()
