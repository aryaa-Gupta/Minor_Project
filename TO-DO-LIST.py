from tkinter import *
from tkinter import messagebox
import sqlite3 as sql


def add_works():
    work_string = work_field.get()
    if len(work_string) == 0:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        works.append(work_string)
        the_cursor.execute('insert into works values (?)', (work_string,))
        list_update()
        work_field.delete(0, 'end')


def list_update():
    clear_list()
    for work in works:
        work_listbox.insert('end', work)


def delete_work():
    try:
        the_value = work_listbox.get(work_listbox.curselection())
        if the_value in works:
            works.remove(the_value)
            list_update()
            the_cursor.execute('delete from works where title = ?', (the_value,))
    except:
        messagebox.showinfo('Error', 'Select A Task To Delete.')


def delete_all_works():
    message_box = messagebox.askyesno('Clear All', 'Confirm ?')
    if message_box == True:
        while (len(works) != 0):
            works.pop()
        the_cursor.execute('delete from works')
        list_update()


def clear_list():
    work_listbox.delete(0, 'end')


def close():
    print(works)
    guiWindow.destroy()


def retrieve_database():
    while (len(works) != 0):
        works.pop()
    for row in the_cursor.execute('select title from works'):
        works.append(row[0])


if __name__ == "__main__":
    guiWindow = Tk()
    guiWindow.title("To-Do List ")
    guiWindow.geometry("665x400+550+250")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#B5E5CF")

    the_connection = sql.connect('listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('create table if not exists works (title text)')

    works = []

    functions_frame = Frame(guiWindow, bg="#8EE5EE")

    functions_frame.pack(side="top", expand=True, fill="both")

    work_label = Label(functions_frame, text="TO-DO-LIST \n Enter the Task Title:",
                       font=("arial", "12", "bold"),
                       background="#8EE5EE",
                       foreground="#FF6103"
                       )
    work_label.place(x=20, y=10)

    work_field = Entry(
        functions_frame,
        font=("Arial", "12"),
        width=42,
        foreground="green",
        background="pink",
    )
    work_field.place(x=180, y=30)

    add_button = Button(
        functions_frame,
        text="Add",
        width=15,
        bg='#D4AC0D', font=("arial", "14", "bold"),
        command=add_works,

    )
    del_button = Button(
        functions_frame,
        text="Remove",
        width=15,
        bg='#D4AC0D', font=("arial", "14", "bold"),
        command=delete_work,
    )
    del_all_button = Button(
        functions_frame,
        text="Delete All",
        width=15,
        font=("arial", "14", "bold"),
        bg='#D4AC0D',
        command=delete_all_works
    )

    exit_button = Button(
        functions_frame,
        text="Exit / Close",
        width=52,
        bg='#D4AC0D', font=("blue", "14", "bold"),
        command=close
    )
    add_button.place(x=18, y=80, )
    del_button.place(x=240, y=80)
    del_all_button.place(x=460, y=80)
    exit_button.place(x=17, y=330)

    work_listbox = Listbox(
        functions_frame,
        width=70,
        height=10,
        font="bold",
        selectmode='SINGLE',
        background="PINK",
        foreground="BLACK",
        selectbackground="#FF8C00",
        selectforeground="BLACK"
    )
    work_listbox.place(x=7, y=140)

    retrieve_database()
    list_update()
    guiWindow.mainloop()
    the_connection.commit()
    the_cursor.close()