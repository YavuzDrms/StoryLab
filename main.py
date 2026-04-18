import customtkinter
from connection import check_connection, show_connection_error
import ai
import database
from CTkTable import *
import sqlite3

connection = check_connection()
if connection:
    pass
else:
    print("Connection error. please try again")
    show_connection_error()

tips = "Use [] for telling the emotion. Example: [Sad] -> AI will generate a sad story. \nUse {} for telling the final. Example: {Some final...} -> AI will generate a story that end like this."

app = customtkinter.CTk()
customtkinter.set_appearance_mode("dark")
app.title("Story Lab")
app.geometry("800x1000")
app.resizable(False, False)

def switch_lightmode():
    print(lightmode_var.get())
    if lightmode_var.get() == "on":
        customtkinter.set_appearance_mode("dark")
    elif lightmode_var.get() == "off":
        customtkinter.set_appearance_mode("light")
lightmode_var = customtkinter.StringVar(value="on")
lightmode = customtkinter.CTkSwitch(app, text="DarkMode", command=switch_lightmode,
                                    variable=lightmode_var, onvalue="on", offvalue="off")

def generate_story():
    usr_input = user_input.get("0.0", "end")
    user_input.delete("0.0", "end")
    
    ai_response.configure(state="normal")
    ai_response.delete("0.0", "end")
    
    ai_prompt = ai.generate_prompt(usr_input)
    ai_res= ai.get_ai_response(ai_prompt, usr_input)
    
    d_t = database.get_date()
    data_model = database.DataModel(usr_input, d_t, ai_res)
    database.log_data(data_model)
    
    if ai_res:
        print(ai_res)
        ai_response.delete("0.0", "end")
        ai_response.insert("0.0", ai_res)
    else:
        print("Error")
        ai_response.delete("0.0", "end")
        ai_response.insert("0.0", "Error.")
    ai_response.configure(state="disabled")

def copy_to_clipboard(data):
    selected_text = data["value"]

    app.clipboard_clear() 
    app.clipboard_append(selected_text)
    app.update() 
    
    print(f"Copied: {selected_text}")

def show_database():
    db_window = customtkinter.CTkToplevel(app)
    db_window.geometry("900x600")
    db_window.title("Past Chats")

    db_window.attributes("-topmost", True)

    scroll_frame = customtkinter.CTkScrollableFrame(db_window, width=850, height=550)
    scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, prompt, response, date_time FROM messages")
        rows = cursor.fetchall()
        conn.close()
        
        table_data = [["ID", "Prompt", "Response", "Date"]]
        
        if rows:
            for row in rows:
                table_data.append([str(row[0]), str(row[1]), str(row[2]), str(row[3])])
        else:
            table_data.append(["-", "Cant find data", "-", "-"])

    except Exception as e:
        table_data = [["ERROR"]], [[f"Connection error: {e}"]]

    table = CTkTable(
        master=scroll_frame, 
        row=len(table_data), 
        column=4, 
        values=table_data,
        colors=["#2b2b2b", "#333333"],
        header_color="#1f538d",
        hover_color="#14375e",
        width=200,
        anchor="w",
        command=copy_to_clipboard
    )
    
    table.pack(expand=True, fill="both")

txt_storylab = customtkinter.CTkLabel(app, text="Story Lab", fg_color="transparent",
                                      font=("Arial", 48, "bold"))
txt_howtouse = customtkinter.CTkLabel(app, text="How to use?", fg_color="transparent",
                                      font=("Arial", 24, "bold"))
txt_tips = customtkinter.CTkLabel(app, text=tips, fg_color="transparent",
                                      font=("Arial", 14, "bold"))
user_input = customtkinter.CTkTextbox(app, width=600, height=350)
btn_generate = customtkinter.CTkButton(app, text="Generate Story", command=generate_story, width=200, height=45, corner_radius=15,
                                       font=("Inter", 16, "bold"))
ai_response = customtkinter.CTkTextbox(app, width=600, height=380)
ai_response.insert("0.0", "AI's response")
ai_response.configure(state="disabled")
btn_showschats = customtkinter.CTkButton(app, text="Show past chats", command=show_database, width=100, height=45, corner_radius=15,
                                         font=("Inter", 16, "bold"))
btn_cleardatabase = customtkinter.CTkButton(app, text="Clear past chats", command=database.clear_database, width=100, height=45, corner_radius=15,
                                            font=("Inter", 16, "bold"))

lightmode.place(relx=0.02, rely=0.95, anchor="sw")
txt_storylab.pack()
txt_howtouse.pack()
txt_tips.pack()
user_input.place(relx=0.5, rely=0.3, anchor="center")
btn_generate.place(relx=0.5, rely=0.5, anchor="center")
ai_response.place(relx=0.5, rely=0.72, anchor="center")
btn_showschats.place(relx=0.4, rely=1, anchor="sw")
btn_cleardatabase.place(relx=0.6, rely=1, anchor="sw")
app.mainloop()