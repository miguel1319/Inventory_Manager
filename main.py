import tkinter.ttk

from Functions import *
from Connect import *

root = Tk()
root.iconbitmap('GameIcon.ico')
root.title("Game Manager")
root.geometry("960x750")

# Display Frame

Display_Frame = LabelFrame(root)
Display_Frame.place(x=230, y=27, width=702, height=495)

List_Scrollbar = Scrollbar(Display_Frame, orient=VERTICAL)

Display = tkinter.ttk.Treeview(Display_Frame, yscrollcommand=List_Scrollbar.set)
Display['columns'] = ("Count", "Game ID", "Title", "Console", "Price")
Display.column("#0", width=0, stretch=NO)
Display.column("Count", width=35, minwidth=35, stretch=NO)
Display.column("Game ID", width=60, anchor=CENTER, minwidth=60, stretch=NO)
Display.column("Title", width=190, anchor=W, minwidth=200)
Display.column("Console", width=125, anchor=CENTER, minwidth=125, stretch=NO)
Display.column("Price", width=80, anchor=E, minwidth=80, stretch=NO)

Display.heading("#0", text="", anchor=W)
Display.heading("Count", text="#", anchor=W)
Display.heading("Game ID", text="ID", anchor=W)
Display.heading("Title", text="Title", anchor=W)
Display.heading("Console", text="Console", anchor=W)
Display.heading("Price", text="Price", anchor=W)


Display.place(x=-2, y=-2, width=683, height=495)

List_Scrollbar.config(command=Display.yview)
List_Scrollbar.pack(side=RIGHT, fill=Y)


# Quick Access Menu
Quick_Access_Frame = LabelFrame(root, text="Quick Access Functions", pady=7)
Quick_Access_Frame.place(x=20, y=20, width=200, height=500)

Button(Quick_Access_Frame, text="Read All Games", width=22, command=lambda: read_all_games_to_display(conn, Display)).pack()
Button(Quick_Access_Frame, text="Count by Console", width=22, command=lambda: display_count_by_console(conn, Display)).pack(pady=10)
Button(Quick_Access_Frame, text="Total Price by Console", width=22, command=lambda: display_pricesum_by_console(conn, Display)).pack()
Button(Quick_Access_Frame, text="Total Count and Sum", width=22, command=lambda: display_total(conn, Display)).pack(pady=10)
Button(Quick_Access_Frame, text="Clear Display", width=22, command=lambda: clear_text(Display)).pack()


# Find Menu
Find_Frame = LabelFrame(root, text="Find ", pady=7)
Find_Frame.place(x=20, y=525, width=200, height=200)

Find_Entry = Entry(Find_Frame, width=22)
Find_Entry.pack()

Find_Clicked = StringVar()
Find_Clicked.set("Select a Field")
Find_Drop_Menu = OptionMenu(Find_Frame, Find_Clicked, "Title", "Price", "Console", "GameID")

Find_Drop_Menu.pack(pady=5)

Button(Find_Frame, text="Find", width=18, command=lambda: find_title(conn, Find_Clicked.get(), Find_Entry.get(), Display, Radio_Variable.get())).pack()


Radio_Variable = IntVar()
R1 = Radiobutton(Find_Frame, text="Equal To", state="disabled", value=1, variable=Radio_Variable)
R1.pack()
R2 = Radiobutton(Find_Frame, text="Less Than", state="disabled", value=2, variable=Radio_Variable)
R2.pack(side=LEFT)
R3 = Radiobutton(Find_Frame, text="Greater Than", state="disabled", value=3, variable=Radio_Variable)
R3.pack(side=LEFT)


def set_radio(*args):

    if Find_Clicked.get() == "Price":
        R1.config(state="normal")
        R2.config(state="normal")
        R3.config(state="normal")
    else:
        Radio_Variable.set(0)
        R1.config(state="disabled")
        R2.config(state="disabled")
        R3.config(state="disabled")


Find_Clicked.trace('w', set_radio)

# Delete Menu
Delete_Frame = LabelFrame(root, text="Delete ", pady=30, padx=5)
Delete_Frame.place(x=231, y=525, width=180, height=200)

Delete_Entry = Entry(Delete_Frame, width=22)
Delete_Entry.pack()
Label(Delete_Frame, text="ID of Game").pack(pady=5)

Button(Delete_Frame, width=18, text="Delete", command=lambda: delete_item(conn, Delete_Entry.get())).pack()


# Insert Menu
Insert_Frame = LabelFrame(root, text="Insert ", pady=7, padx=5)
Insert_Frame.place(x=422, y=525, width=250, height=200)

Insert_Title_Entry = Entry(Insert_Frame, width=35)
Insert_Title_Entry.pack()
Label(Insert_Frame, text="Title").pack(pady=4)

Insert_Price_Entry = Entry(Insert_Frame, width=35)
Insert_Price_Entry.pack()
Label(Insert_Frame, text="Price").pack(pady=4)


Insert_Clicked = StringVar()
Insert_Clicked.set("Select a Console")

Console_Options = ["Intellivision", "Atari", "PlayStation", "PlayStation 2", "PlayStation 3",
                   "PlayStation 4", "PlayStation Vita", "PSP", "Xbox", "Xbox 360",
                   "Xbox One", "NES", "SNES", "Nintendo 64", "GameCube", "Wii", "Wii U", "Nintendo Switch",
                   "GameBoy", "GameBoy Color", "GameBoy Advance", "Nintendo DS", "Nintendo 3DS"]

Insert_Drop_Menu = OptionMenu(Insert_Frame, Insert_Clicked, *Console_Options)
Insert_Drop_Menu.pack(pady=3)


Button(Insert_Frame, width=18, text="Insert", command=lambda: insert_item(conn,Insert_Title_Entry.get(), Insert_Price_Entry.get(), Insert_Clicked.get())).pack(pady=3)


# Update Menu
Update_Frame = LabelFrame(root, text="Update ", pady=7)
Update_Frame.place(x=683, y=525, width=250, height=200)

Update_ID_Entry = Entry(Update_Frame, width=35)
Update_ID_Entry.pack()
Label(Update_Frame, text="ID of Game").pack(pady=5)

Update_Value_Entry = Entry(Update_Frame, width=35)
Update_Value_Entry.pack()

Update_Clicked = StringVar()
Update_Clicked.set("Select a Field")
Update_Drop_Menu = OptionMenu(Update_Frame, Update_Clicked, "Title", "Price")
Update_Drop_Menu.pack(pady=5)


Button(Update_Frame, width=18, text="Update", command=lambda: update_item(conn, Update_ID_Entry.get(), Update_Value_Entry.get(), Update_Clicked.get())).pack()

root.mainloop()
