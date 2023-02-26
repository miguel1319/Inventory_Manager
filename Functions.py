from tkinter import *


def clear_text(display):
    try:
        for i in display.get_children():
            display.delete(i)
    except:
        print("Clear function returned error")
    pass


def read_all_games_to_display(conn, display):
    clear_text(display)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT V.Game_ID, Title, Console_Name, V.Price
        FROM Video_Games V
        join Game_Console I
        ON V.Game_ID = I.Game_ID
        join Consoles C
        ON C.Console_ID = I.Console_ID
        ORDER by Console_Name, Title asc
        """
    )

    for i, row in enumerate(cursor, 1):
        display.insert(parent='', index='end', iid=i, text='', values=(str(i), str(row[0]), row[1], row[2], "$" + str(row[3])))


def display_count_by_console(conn, display):
    clear_text(display)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT count(V.Game_ID), Console_Name
        FROM Video_Games V
        join Game_Console I
        ON V.Game_ID = I.Game_ID
        join Consoles C
        ON C.Console_ID = I.Console_ID
        GROUP by Console_Name
        """
    )

    for i, row in enumerate(cursor, 1):
        display.insert(parent='', index='end', iid=i, text='',
                       values=(str(row[0]), "", "", row[1], ""))


def display_pricesum_by_console(conn, display):
    clear_text(display)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT sum(V.Price), C.Console_Name
        FROM Video_Games V
        join Game_Console I
        ON V.Game_ID = I.Game_ID
        join Consoles C
        ON C.Console_ID = I.Console_ID
        GROUP by Console_Name
        """
    )

    for i, row in enumerate(cursor, 1):
        display.insert(parent='', index='end', iid=i, text='',
                       values=("", "", "", row[1], str(row[0])))


def print_to_screen(cursor, display):
    clear_text(display)
    for count, row in enumerate(cursor, 1):
        display.insert(parent='', index='end', iid=count, text='',
                       values=(str(count), str(row[0]), row[1], row[2], "$" + str(row[3])))


def find_title(conn, optionstr, val, display, radio):
    if optionstr == "Select a Field":
        return
    cursor = conn.cursor()

    if optionstr == "Title":
        cursor.execute(f"""SELECT V.Game_ID, Title, Console_Name, V.Price
            FROM Video_Games V
            join Game_Console I
            ON V.Game_ID = I.Game_ID
            join Consoles C
            ON C.Console_ID = I.Console_ID
            where Title LIKE '%{val}%'
            ORDER by Console_Name, Title asc""")
        print_to_screen(cursor, display)

    if optionstr == "Price":
        if radio == 0:  # nothing
            return
        if radio == 1:  # equal to
            cursor.execute(f"""SELECT V.Game_ID, Title, Console_Name, V.Price
                            FROM Video_Games V
                            join Game_Console I
                            ON V.Game_ID = I.Game_ID
                            join Consoles C
                            ON C.Console_ID = I.Console_ID
                            where V.price = {val}
                            ORDER by Console_Name, Title asc""")
            print_to_screen(cursor, display)
        if radio == 2:  # less than
            cursor.execute(f"""SELECT V.Game_ID, Title, Console_Name, V.Price
                                        FROM Video_Games V
                                        join Game_Console I
                                        ON V.Game_ID = I.Game_ID
                                        join Consoles C
                                        ON C.Console_ID = I.Console_ID
                                        where V.price <= {val}
                                        ORDER by Console_Name, Title asc""")
            print_to_screen(cursor, display)
        if radio == 3:  # greater than
            cursor.execute(f"""SELECT V.Game_ID, Title, Console_Name, V.Price
                                        FROM Video_Games V
                                        join Game_Console I
                                        ON V.Game_ID = I.Game_ID
                                        join Consoles C
                                        ON C.Console_ID = I.Console_ID
                                        where V.price >= {val}
                                        ORDER by Console_Name, Title asc""")
            print_to_screen(cursor, display)

    if optionstr == "Console":
        cursor.execute(f"""SELECT V.Game_ID, Title, Console_Name, V.Price
                    FROM Video_Games V
                    join Game_Console I
                    ON V.Game_ID = I.Game_ID
                    join Consoles C
                    ON C.Console_ID = I.Console_ID
                    where C.Console_Name LIKE '{val}'
                    ORDER by Console_Name, Title asc""")
        print_to_screen(cursor, display)

    if optionstr == "GameID":
        cursor.execute(f"""SELECT V.Game_ID, Title, Console_Name, V.Price
                    FROM Video_Games V
                    join Game_Console I
                    ON V.Game_ID = I.Game_ID
                    join Consoles C
                    ON C.Console_ID = I.Console_ID
                    where V.Game_ID = '{val}'
                    ORDER by Console_Name, Title asc""")
        print_to_screen(cursor, display)


def display_total(conn, display):
    clear_text(display)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT sum(V.Price), count(V.Title)
        FROM Video_Games V
        join Game_Console I
        ON V.Game_ID = I.Game_ID
        join Consoles C
        ON C.Console_ID = I.Console_ID
        """
    )

    for i, row in enumerate(cursor, 1):
        display.insert(parent='', index='end', iid=i, text='',
                       values=(row[1], "", "", "", str(row[0])))


def delete_item(conn, val):
    cursor = conn.cursor()

    cursor.execute(
        'DELETE FROM Video_Games WHERE Game_ID = ?;',
        val
    )

    cursor.execute(
        'DELETE FROM Game_Console WHERE Game_ID = ?;',
        val
    )

    cursor.execute(
        'DELETE FROM Game_Info WHERE Game_ID = ?;',
        val
    )
    conn.commit()


def insert_item(conn, insert_title_entry, insert_price_entry, insert_clicked):
    if insert_clicked == "Select a Console":
        return
    cursor = conn.cursor()

    # Must be the same order as the database
    value = ["Atari", "Intellivision", "PlayStation", "PlayStation 2", "PlayStation 3",
     "PlayStation 4", "PlayStation Vita", "PSP", "Xbox", "Xbox 360",
     "Xbox One", "NES", "SNES", "Nintendo 64", "GameCube", "Wii", "Wii U", "Nintendo Switch",
     "GameBoy", "GameBoy Color", "GameBoy Advance", "Nintendo DS", "Nintendo 3DS"]

    cursor.execute('INSERT INTO Video_Games(Title,Price) VALUES(?,?);',
                   (insert_title_entry, int(insert_price_entry)))

    cursor.execute("""select top(1) Game_ID from Video_Games order by Game_ID desc""")
    id = 0
    for i in cursor:
        id = int(i[0])

    cursor.execute('INSERT INTO Game_Console(Game_ID, Console_ID) Values(?,?)', (id, value.index(insert_clicked) + 1))
    conn.commit()


def update_item(conn, update_id_entry, update_value_entry, update_clicked):
    if update_clicked == "Select a Field":
        return
    cursor = conn.cursor()
    try:
        if update_clicked == "Title":
            cursor.execute('UPDATE Video_Games SET Title = ? WHERE Game_ID = ?;',
                           (update_value_entry, update_id_entry))
            conn.commit()

        if update_clicked == "Price":
            cursor.execute('UPDATE Video_Games SET Price = ? WHERE Game_ID = ?;',
                           (update_value_entry, update_id_entry))
            conn.commit()
    except:
        print("Wrong")
