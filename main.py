import customtkinter
from connection import check_connection, show_connection_error
import ai
import database

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

lightmode.place(relx=0.02, rely=0.95, anchor="sw")
txt_storylab.pack()
txt_howtouse.pack()
txt_tips.pack()
user_input.place(relx=0.5, rely=0.3, anchor="center")
btn_generate.place(relx=0.5, rely=0.5, anchor="center")
ai_response.place(relx=0.5, rely=0.72, anchor="center")
app.mainloop()