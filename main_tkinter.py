from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ct
from PIL import ImageTk, Image
import functions.sql_data as sql_data
import functions.api_weather as api_weather
import functions.sync_values as sync_values
import functions.graphs as graphs

root = ct.CTk()

ct.set_appearance_mode("light")
root.title('PyFlora Posude')
root.geometry('900x625')
root.resizable(width=False, height=False)
style = ttk.Style()
style.configure('Treeview.Heading', font=('Helvetica', 9, 'bold'))


frm_color = '#ECFEFA'
btn_color = '#DFDFDF'

frame_1 = ct.CTkFrame(master=root, width=899, height=624, corner_radius=10, border_width=2, border_color='grey', fg_color='#E9FFDB')
frame_2 = ct.CTkFrame(master=root, width=899, height=624, corner_radius=10, border_width=2, border_color='grey', fg_color='#E9FFDB')

frame_1.rowconfigure(0, weight=1)
frame_1.rowconfigure(1, weight=6)
frame_1.columnconfigure(0, weight=1)

frame_2.rowconfigure(0, weight=1)
frame_2.rowconfigure(1, weight=11)
frame_2.columnconfigure(0, weight=1)

for frame in (frame_1, frame_2):
    frame.grid(row=0, column=0, sticky='nsew')

def show_frame(frame):
    frame.tkraise()

# nakon login-a
def welcome_page():
    show_frame(frame_2)

    flora_label = ct.CTkLabel(frame_2, text='PyFlora', text_font=("Helvetica", 10, 'bold'))
    welcome_label = ct.CTkLabel(frame_2, text=f'Welcome {welcome_username}!', text_font=("Helvetica", 10, 'bold'))
    profil_button = ct.CTkButton(frame_2, text='My Profile', text_font=("Helvetica", 10),fg_color=btn_color, command=my_profile)
    log_out_button = ct.CTkButton(frame_2, text='Log Out', text_font=("Helvetica", 10), fg_color='red', command=log_in)

    flora_label.place(x=20, y=25)
    welcome_label.place(x=180, y=25)
    profil_button.place(x=500, y=25)
    log_out_button.place(x=650, y=25)

    pots_page()
    
#####  PLANTS PAGE  #####
def plants_page():

    frame_2b = ct.CTkFrame(frame_2, border_width=1, border_color='green', width=870, height=535, fg_color='#ECFEFA')
    frame_2b.place(x=15, y=75)

    # POPIS BILJAKA

    scrollbar_y = Scrollbar(frame_2b, orient=VERTICAL)
    
    plants_tree = ttk.Treeview(frame_2b)
    plants_tree.place(relx=0.01, rely=0.03, width=840, height=460)
    
    plants_tree.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.configure(command=plants_tree.yview)
    scrollbar_y.place(relx=0.98, rely=0.1, width=15, height=430)
    
    plants_tree.configure(selectmode='extended')

    plants_tree.configure(
        columns=(
            'ID',
            'Name',
            'Info'
        )
    )
    # plants_tree.heading('#0', text='ID', anchor=CENTER)
    plants_tree.heading('ID', text='ID', anchor=CENTER)
    plants_tree.heading('Name', text='Name of Plant', anchor=W)
    plants_tree.heading('Info', text='Information', anchor=W)

    plants_tree.column('#0', stretch=NO, width=0)
    plants_tree.column('#1', stretch=NO, width=80, anchor=CENTER)
    plants_tree.column('#2', stretch=NO, minwidth=125, width=200)
    plants_tree.column('#3', stretch=YES, minwidth=100, width=300)


    def insert_plants(id, name, info):
        # ovdje je iid=name jer ce po tome raspoznati biljke i radit query - edit ili delete button
        plants_tree.insert(parent='', index='end', text=id, iid=id , values=(id, name, info[:]))  # iid=0..
    
    plants_list = sql_data.load_plants()   # list of tuples
    
    for plant in plants_list:
        insert_plants(plant[0], plant[1], plant[2])

    
    # Button COMMANDS - ADD, EDIT, DELETE

    def add_plant():
        frame_2_add = ct.CTkFrame(frame_2, border_width=1, border_color='green', width=870, height=535, fg_color='#ECFEFA')
        frame_2_add.place(x=15, y=75)

        info_label = ct.CTkLabel(frame_2_add, text='More Information about the plant [Maintenance]')
        title_label = ct.CTkLabel(frame_2_add, text='ADD NEW PLANT', text_font='bold')
        id_label = ct.CTkLabel(frame_2_add, text='ID [Unique number]')
        name_label = ct.CTkLabel(frame_2_add, text='Name Of Plant')
        new_plant_id_entry = ct.CTkEntry(frame_2_add, width=90, height=8, borderwidth=3, relief='flat')
        new_plant_name_entry = ct.CTkEntry(frame_2_add, width=185, height=8, borderwidth=3, relief='flat')

        new_plant_info = Text(frame_2_add, width=68, height=23, padx=10, pady=10, spacing1=1, wrap=WORD)
        
        info_label.place(relx=0.3, rely=0.05)
        title_label.place(relx=0.03, rely=0.05) 
        id_label.place(relx=0.02, rely=0.15)
        new_plant_id_entry.place(relx=0.04, rely=0.2)
        name_label.place(relx=0.015, rely=0.28)
        new_plant_name_entry.place(relx=0.04, rely=0.33)
        
        new_plant_info.place(relx=0.3, rely=0.12)

        def upload_photo():
            global new_image_path, path_label
            new_image_path = filedialog.askopenfilename(title='Select image', filetypes=(('Allfile', '*'),('png', '*.png'), ('jpg', '*.jpg')))
            path_label = ct.CTkLabel(frame_2_add, text=new_image_path, wraplength=170, justify=LEFT)
            path_label.place(relx=0.04, rely=0.5)
            

        def save_plant():
            img_binary = sql_data.to_binary(new_image_path)
            new_id = new_plant_id_entry.get()
            new_name = new_plant_name_entry.get()
            new_info = new_plant_info.get('0.0', END)

            isert_is_ok = sql_data.insert_plant(new_id, img_binary, new_name, new_info)
            if isert_is_ok != -1:
                messagebox.showinfo('New Plant', 'Successfully Added! :)')
                new_plant_id_entry.delete(0, END)
                new_plant_name_entry.delete(0, END)
                new_plant_info.delete('0.0', END)
                path_label.place_forget()
            else:
                messagebox.showerror('New Plant', 'ID Already exists. Try Again')


        add_img_btn = ct.CTkButton(frame_2_add, text='Add a Photo', command=upload_photo, width=35, height=25, fg_color=btn_color)
        save_new_plant_btn = ct.CTkButton(frame_2_add, text='Save New Plant', command=save_plant, width=35, height=25, fg_color='#72FF6B')
        back_btn = ct.CTkButton(frame_2_add, text='Back',width=35, height=25, fg_color=btn_color, command=lambda: plants_page())

        save_new_plant_btn.place(relx=0.8, rely=0.92)
        add_img_btn.place(relx=0.04, rely=0.42)
        back_btn.place(relx=0.1, rely=0.92)

    def delete_plant():
        
        try:
            plant_id = plants_tree.selection()[0]
            sql_data.delete_plant(plant_id)
            plants_page()
        except IndexError:
            messagebox.showerror("Delete notification", "Choose a plant first !")

    def edit_plant():
        try:
            plant_id = plants_tree.selection()[0]                                   # uzima onaj iid iz ttk-a, broj - index sutpca
            print(plant_id)
        except IndexError:
            messagebox.showerror("Edit notification", "Choose a plant first !")
            return
        
        # novi frame preko popisa biljki
        frame_2c_edit = ct.CTkFrame(frame_2, border_width=1, border_color='green', width=870, height=535, fg_color='#ECFEFA')
        frame_2c_edit.place(x=15, y=75)

        # PRIKAZ SLIKE i ostalih info    
        plant_name, plant_info = sql_data.load_photo(plant_id)   # odabran naziv biljke iz tkk, po tome se radi query i moze se ucitat stvoreni .png
        
        img_old = Image.open('./photos/plant_from_bin.png')
        img_new = img_old.resize((200,250))
        my_img=ImageTk.PhotoImage(img_new)
        plant_pic = Label(frame_2c_edit, image=my_img)
        plant_pic.image = my_img                   
        plant_pic.place(relx=0.03, rely=0.13)

        name_lbl = ct.CTkLabel(frame_2c_edit, text=plant_name, width=100, height=30, text_font=("Helvetica", 13, 'bold'))
        info_txt = Text(frame_2c_edit, width=68, height=22, padx=10, pady=10, spacing1=1, wrap=WORD)
        
        info_txt.insert('0.0', plant_info)

        name_lbl.place(relx=0.55, rely=0.04)
        info_txt.place(relx=0.3, rely=0.13)
        

        def save_changes_btn():
            new_text = info_txt.get('0.0', END)
            info_txt.delete('0.0', END)
            sql_data.update_plant(plant_id, new_text)
            messagebox.showinfo('Update!', 'Successfully updated! :)')
            info_txt.insert('0.0', new_text)

        def update_img():
            global image_path
            image_path = filedialog.askopenfilename(title='Select image', filetypes=(('png', '*.png'), ('jpg', '*.jpg'), ('Allfile', '*')))
            try:
                img_binary = sql_data.to_binary(image_path)   # sada je binarni file
                sql_data.update_plant_image(plant_id, img_binary)
            except FileNotFoundError:
                return
            edit_plant() 


        back_btn = ct.CTkButton(frame_2c_edit, text='Back',width=35, height=25, fg_color=btn_color, command=lambda: plants_page())
        change_photo = ct.CTkButton(frame_2c_edit, text='Update Photo',width=35, height=25, fg_color=btn_color, command=update_img )
        save_btn = ct.CTkButton(frame_2c_edit, text='Save Changes', fg_color='#72FF6B', command=save_changes_btn)
        
        back_btn.place(relx=0.11, rely=0.92)
        change_photo.place(relx=0.08, rely=0.7)
        save_btn.place(relx=0.73, rely=0.92)
        ## END OF EDIT ##


    delete_btn = ct.CTkButton(frame_2b, text='Delete', width=35, height=25, command=delete_plant,fg_color=btn_color, hover_color='red')
    edit_btn = ct.CTkButton(frame_2b, text='Info - Edit', width=35, height=25, command=edit_plant, fg_color=btn_color)
    add_btn = ct.CTkButton(frame_2b, text='Add New Plant', width=35, height=25, command=add_plant, fg_color=btn_color)
    pots_btn = ct.CTkButton(frame_2b, text='Go to PyPots', width=35, height=25, command=pots_page, fg_color=btn_color)
    delete_btn.place(relx=0.85, rely=0.94, anchor=CENTER)
    edit_btn.place(relx=0.7, rely=0.94, anchor=CENTER)
    add_btn.place(relx=0.55, rely=0.94, anchor=CENTER)
    pots_btn.place(relx=0.1, rely=0.94, anchor=CENTER)

    # PLANTS unutar welcome page (gornji btns)

###########################################################################################################
def pots_page():

    frame_2_pot = ct.CTkFrame(frame_2, border_width=1, border_color='green', width=870, height=535, fg_color='#ECFEFA')
    frame_2_pot.place(x=15, y=75)    

    scrollbar_y = Scrollbar(frame_2_pot, orient=VERTICAL)
    
    global pots_tree
    pots_tree = ttk.Treeview(frame_2_pot)
    pots_tree.place(relx=0.01, rely=0.03, width=840, height=460)
    
    pots_tree.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.configure(command=pots_tree.yview)
    scrollbar_y.place(relx=0.98, rely=0.1, width=15, height=430)
    
    pots_tree.configure(selectmode='extended')

    pots_tree.configure(
        columns=(
            'ID',
            'Name',
            'Status'
        )
    )
    # pots_tree.heading('#0', text='ID', anchor=CENTER)
    pots_tree.heading('ID', text='Pot ID', anchor=CENTER)
    pots_tree.heading('Name', text='Pot Name / Location', anchor=W)
    pots_tree.heading('Status', text='Status', anchor=W)

    pots_tree.column('#0', stretch=NO, width=0)
    pots_tree.column('#1', stretch=NO, width=80, anchor=CENTER)
    pots_tree.column('#2', stretch=NO, minwidth=125, width=320)
    pots_tree.column('#3', stretch=YES, minwidth=100, width=300)

    # ovdje je iid=name jer ce po tome raspoznati biljke i radit query - edit ili delete button
    def insert_pots(id, name, plant):
        pots_tree.insert(parent='', index='end', text=id, iid=id , values=(id, name, plant))  # iid=0..
    
    pots_list = sql_data.load_pots()   # list of tuples
    
    for pot in pots_list:
        if pot[2] == None: 
            status = 'Empty Pot'
            insert_pots(pot[0], pot[1], status)
        else:
            status = sql_data.load_plant_name(pot[2])  # id od biljke pa se dobije naziv
            insert_pots(pot[0], pot[1], status[0])


    def to_empty_pots():
        pots_tree.delete(*pots_tree.get_children())
        empty_pots_btn.place_forget()
        all_pots_btn = ct.CTkButton(frame_2_pot, text='See All Pots', width=35, height=25, command=pots_page, fg_color=btn_color)
        all_pots_btn.place(relx=0.3, rely=0.94, anchor=CENTER)

        for pot in pots_list:
            if pot[2] == None: 
                status = 'Empty Pot'
                insert_pots(pot[0], pot[1], status)

  
    delete_btn = ct.CTkButton(frame_2_pot, text='Delete', width=35, height=25, command=delete_pot,fg_color=btn_color, hover_color='red')
    edit_btn = ct.CTkButton(frame_2_pot, text='Info / Edit', width=35, height=25, command=edit_pot, fg_color=btn_color)
    add_btn = ct.CTkButton(frame_2_pot, text='Add New Pot', width=35, height=25, command=add_new_pot, fg_color=btn_color)
    pots_btn = ct.CTkButton(frame_2_pot, text='Go to Plants', width=35, height=25, command=plants_page, fg_color=btn_color)
    empty_pots_btn = ct.CTkButton(frame_2_pot, text='See Empty Pots', width=35, height=25, command=to_empty_pots, fg_color=btn_color)
    
    delete_btn.place(relx=0.85, rely=0.94, anchor=CENTER)
    edit_btn.place(relx=0.7, rely=0.94, anchor=CENTER)
    add_btn.place(relx=0.55, rely=0.94, anchor=CENTER)
    pots_btn.place(relx=0.1, rely=0.94, anchor=CENTER)
    empty_pots_btn.place(relx=0.3, rely=0.94, anchor=CENTER)


def delete_pot():
    try:
        pot_id = pots_tree.selection()[0]
        sql_data.delete_pot(pot_id)
        pots_page()
    except IndexError:
        messagebox.showerror("Delete notification", "Choose a pot first !")

def edit_pot():
    try:
        pot_id = pots_tree.selection()[0]                       # uzima onaj iid iz ttk-a, broj - index sutpca
    except IndexError:
        messagebox.showerror("Edit notification", "Choose a pot first !")
        return
   
    # novi frame preko popisa posuda
    global frame_2c_edit_pot
    frame_2c_edit_pot = ct.CTkFrame(frame_2, border_width=1, border_color='green', width=870, height=535, fg_color='#ECFEFA')
    frame_2c_edit_pot.place(x=15, y=75)

    pot_name, plant_id = sql_data.load_one_pot(pot_id)
    
    # Ako posuda ima/nema biljku
    if plant_id != None:
        plant_name = sql_data.load_photo(plant_id)[0]   
        # PRIKAZ SLIKE i ostalih info, mogucnost izmjena podataka   
        # plant_name, plant_info = sql_data.load_photo(plant_id)   # odabran naziv biljke iz tkk, po tome se radi query i moze se ucitat stvoreni .png
        
        img_old = Image.open('./photos/plant_from_bin.png')
        img_new = img_old.resize((175,225))
        my_img=ImageTk.PhotoImage(img_new)
        plant_pic = Label(frame_2c_edit_pot, image=my_img)
        plant_pic.image = my_img                  
        plant_pic.place(relx=0.72, rely=0.13)

        name_lbl = ct.CTkLabel(frame_2c_edit_pot, text=plant_name, width=100, height=30, text_font=("Helvetica", 13, 'bold'))
        name_lbl.place(relx=0.76, rely=0.06)
    
        current_temp = api_weather.get_current_info()
        moist, ph, salinity, light = sync_values.generate_values()
        degree_sign = u'\N{DEGREE SIGN}'
        
        current_temp_lbl = ct.CTkLabel(frame_2c_edit_pot, text=f'Air Temperature:\t{current_temp} {degree_sign}C', width=100, height=30)
        current_moist_lbl = ct.CTkLabel(frame_2c_edit_pot, text=f'Soil Moisture:\t{moist} %', width=100, height=30)
        current_ph_lbl = ct.CTkLabel(frame_2c_edit_pot, text=f'Soil pH:\t \t{ph}', width=100, height=30)
        current_salinity_lbl = ct.CTkLabel(frame_2c_edit_pot, text=f'Soil Salinity:  \t{salinity}', width=100, height=30)
        current_light_lbl = ct.CTkLabel(frame_2c_edit_pot, text=f'Light Level:  \t{light}', width=100, height=30)
        graph_opt_label = ct.CTkLabel(frame_2c_edit_pot, text='Graph options', width=100, height=30, text_font=("Helvetica", 9, 'bold'))

        def empty_pot():
            sql_data.update_pot(pot_id, None)
            edit_pot()

        def which_type(chosen_value):
            
            if chosen_value == 'Air Temperature - Line Chart':
                graphs.one_day_temp('line')
            elif chosen_value == 'Air Temperature - Bar Chart':
                graphs.one_day_temp('')
            elif chosen_value == 'Soil Moisture - Line Chart':
                graphs.one_day_moist('line')
            elif chosen_value == 'Soil Moisture - Bar Chart':
                graphs.one_day_moist('')
            elif chosen_value == 'Soil pH - Line Chart':
                graphs.one_day_ph('line')
            elif chosen_value == 'Soil pH - Bar Chart':
                graphs.one_day_ph('')
            elif chosen_value == 'Soil Salinity - Line Chart':
                graphs.one_day_salinity('line')
            elif chosen_value == 'Soil Salinity - Pie Chart':
                graphs.one_day_salinity('pie')
            elif chosen_value == 'Soil Salinity - Bar Chart':
                graphs.one_day_salinity('')
            elif chosen_value == 'Light Level - Line Chart':
                graphs.one_day_light('line')
            elif chosen_value == 'Light Level - Pie Chart':
                graphs.one_day_light('pie')
            elif chosen_value == 'Light Level - Bar Chart':
                graphs.one_day_light('')
            else:
                pass
        
        chosen_value = ct.StringVar()
        graph_value = ['Air Temperature - Line Chart', 'Air Temperature - Bar Chart', 
                       'Soil Moisture - Line Chart', 'Soil Moisture - Bar Chart',
                       'Soil pH - Line Chart', 'Soil pH - Bar Chart',
                       'Soil Salinity - Line Chart', 'Soil Salinity - Pie Chart', 'Soil Salinity - Bar Chart', 
                       'Light Level - Line Chart', 'Light Level - Pie Chart', 'Light Level - Bar Chart']
        
        drop_value = ct.CTkOptionMenu(master=frame_2c_edit_pot, variable=chosen_value, command=which_type, values=graph_value, width=100, height=22,fg_color=btn_color )
        drop_value.place(relx=0.13, rely=0.67)
        drop_value.set('Choose a Graph')


        current_temp_lbl.place(relx=0.13, rely=0.23)
        current_moist_lbl.place(relx=0.13, rely=0.28)
        current_ph_lbl.place(relx=0.13, rely=0.33)
        current_salinity_lbl.place(relx=0.13, rely=0.38)
        current_light_lbl.place(relx=0.13, rely=0.43)
        graph_opt_label.place(relx=0.13, rely=0.6)
    
        empty_pot_btn = ct.CTkButton(frame_2c_edit_pot, text='Empty the Pot',width=35, height=25, fg_color=btn_color, command=empty_pot, hover_color='red')
        empty_pot_btn.place(relx=0.77, rely=0.77)
        sync_btn = ct.CTkButton(frame_2c_edit_pot, text='SYNC', width=35, height=25, fg_color=btn_color, text_font=("Helvetica", 11, 'bold'), command=edit_pot)
        sync_btn.place(relx=0.5, rely=0.05)

    else:
        img_old = Image.open('./photos/empty_pot.png')
        img_new = img_old.resize((175,225))
        my_img=ImageTk.PhotoImage(img_new)
        plant_pic = Label(frame_2c_edit_pot, image=my_img)
        plant_pic.image = my_img                   
        plant_pic.place(relx=0.72, rely=0.13)
        name_lbl = ct.CTkLabel(frame_2c_edit_pot, text='Empty Pot', width=100, height=30, text_font=("Helvetica", 13, 'bold'), text_color='red')
        name_lbl.place(relx=0.76, rely=0.05)

    global chosen_plant
    chosen_plant = ct.StringVar()

    list_of_plants = []
    aaa = sql_data.load_plants()
    for plant in aaa:
        list_of_plants.append(plant[1])
    
    
    def clicked_plant(chosen_plant):
        drop.set(chosen_plant)
        # uzet id od odabrane biljke i stavit id u tablicu za pot, ponovo ucitaj edit pot
        plant_id = sql_data.load_plant_id(chosen_plant)[0][0]
        # # pot_id imam od tree.select, plan_id je novi
        sql_data.update_pot(pot_id, plant_id)
        edit_pot()

    
    global drop
    drop = ct.CTkOptionMenu(master=frame_2c_edit_pot, variable=chosen_plant, command=clicked_plant, values=list_of_plants, width=100, height=15,fg_color=btn_color )
    drop.place(relx=0.76, rely=0.68)
    drop.set('Choose a Plant')

    add_plant_lbl = ct.CTkLabel(frame_2c_edit_pot, text='Add - Change Plant', width=100, height=30, text_font=("Helvetica", 9, 'bold'))
    pot_name_lbl = ct.CTkLabel(frame_2c_edit_pot, text=pot_name, width=100, height=30, text_font=("Helvetica", 13, 'bold'))
    pot_id_lbl = ct.CTkLabel(frame_2c_edit_pot, text=f'ID:\t{pot_id}', width=80, height=30, text_font=("Helvetica", 12, 'bold'))
    back_btn = ct.CTkButton(frame_2c_edit_pot, text='Back', width=35, height=25, fg_color=btn_color, command=pots_page)

    add_plant_lbl.place(relx=0.77, rely=0.6)
    pot_name_lbl.place(relx=0.13, rely=0.06)
    pot_id_lbl.place(relx=0.13, rely=0.13)
    back_btn.place(relx=0.07, rely=0.92)
    
    ## END of EDIT POT ##


def add_new_pot():

    frame_2_add_pot = ct.CTkFrame(frame_2, border_width=1, border_color='green', width=870, height=535, fg_color='#ECFEFA')
    frame_2_add_pot.place(x=15, y=75)

    title_label = ct.CTkLabel(frame_2_add_pot, text='ADD NEW POT', text_font=("Helvetica", 13, 'bold'))
    id_label = ct.CTkLabel(frame_2_add_pot, text=' Pot ID [Unique number]')
    name_label = ct.CTkLabel(frame_2_add_pot, text='Name Of Pot - Location')
    new_pot_id_entry = ct.CTkEntry(frame_2_add_pot, width=220, height=8, borderwidth=3, relief='flat')
    new_pot_name_entry = ct.CTkEntry(frame_2_add_pot, width=220, height=8, borderwidth=3, relief='flat')
    choose_plant_label = ct.CTkLabel(frame_2_add_pot, text='Choose a Plant')

    
    title_label.place(relx=0.41, rely=0.08) 
    id_label.place(relx=0.41, rely=0.2)
    new_pot_id_entry.place(relx=0.37, rely=0.27)
    name_label.place(relx=0.41, rely=0.38)
    new_pot_name_entry.place(relx=0.37, rely=0.45)
    choose_plant_label.place(relx=0.41, rely=0.55)

    chosen_plant = ct.StringVar()

    list_of_plants = []
    aaa = sql_data.load_plants()
    for plant in aaa:
        list_of_plants.append(plant[1])
    list_of_plants.append('Empty Pot')

    drop_plant = ct.CTkOptionMenu(master=frame_2_add_pot, variable=chosen_plant, values=list_of_plants, width=150, height=25, fg_color=btn_color )
    drop_plant.place(relx=0.41, rely=0.64)
    drop_plant.set('Choose a Plant')

    def save_pot():
        new_id = new_pot_id_entry.get()
        new_name = new_pot_name_entry.get()
        plant_name = chosen_plant.get()
        
        if plant_name == 'Choose a Plant':
            messagebox.showinfo('New Pot', 'Choose plant option before saving :)')
        
        elif plant_name == 'Empty Pot':
            insert_status = sql_data.insert_pot(new_id, new_name, None)
            if insert_status != -1:
                messagebox.showinfo('New Pot', 'Successfully Added! :)')
                pots_page()
            else:
                messagebox.showerror('New Pot', 'Pot ID Already Exists. Try Again!')
                new_pot_id_entry.delete(0, END)
        
        else:                                                                           # ako je odabrana neka biljka
            plant_id = sql_data.load_plant_id(plant_name)[0][0]
            insert_status = sql_data.insert_pot(new_id, new_name, plant_id)
        
            if insert_status != -1:
                messagebox.showinfo('New Pot', 'Successfully Added! :)')
                pots_page()
            
            else:
                messagebox.showerror('New Pot', 'Pot ID Already Exists. Try Again!')
                new_pot_id_entry.delete(0, END)


    save_new_pot_btn = ct.CTkButton(frame_2_add_pot, text='Save New Pot', command=save_pot, width=35, height=30, fg_color='#72FF6B')
    back_btn = ct.CTkButton(frame_2_add_pot, text='Cancel', width=35, height=30, fg_color=btn_color, command=pots_page)

    save_new_pot_btn.place(relx=0.6, rely=0.9)
    back_btn.place(relx=0.35, rely=0.9)

    
### END of POT Functions ###


def my_profile():
   
    global fname_entry, lname_entry, pass_entry

    frame_2_profile = ct.CTkFrame(frame_2, border_width=1, border_color='green', width=870, height=535, fg_color='#ECFEFA')
    frame_2_profile.place(x=15, y=75)
    profile_label = ct.CTkLabel(frame_2_profile, text='My Profile Page', text_font=("Helvetica", 12, 'bold'))
    username_label = ct.CTkLabel(frame_2_profile, text=f'Username: \t ', text_font=("Helvetica", 11))
    fname_label = ct.CTkLabel(frame_2_profile, text=f'First Name: \t ', text_font=("Helvetica", 11))
    lname_label = ct.CTkLabel(frame_2_profile, text=f'Last Name: \t ', text_font=("Helvetica", 11))
    pass_label = ct.CTkLabel(frame_2_profile, text=f'Current Password: \t ', text_font=("Helvetica", 11))
    
    username_entry = ct.CTkEntry(frame_2_profile, width=220, height=8, borderwidth=3, relief='flat', placeholder_text=welcome_username, cursor = 'X_cursor', text_color='grey')
    # username_entry.configure(text_font =('Italic', 9))
    username_entry.configure(state=DISABLED)
    fname_entry = ct.CTkEntry(frame_2_profile, width=220, height=8, borderwidth=3, relief='flat')
    lname_entry = ct.CTkEntry(frame_2_profile, width=220, height=8, borderwidth=3, relief='flat')
    pass_entry = ct.CTkEntry(frame_2_profile, width=220, height=8, borderwidth=3, relief='flat', show='*', placeholder_text='Must Enter to Make Changes')

    first, last, passw = sql_data.load_user_info(welcome_username)

    fname_entry.insert(0, first)
    lname_entry.insert(0, last)
    # pass_entry.insert(0, passw)


    profile_label.place(relx=0.42, rely=0.07)
    username_label.place(relx=0.22, rely=0.25)
    fname_label.place(relx=0.22, rely=0.32)
    lname_label.place(relx=0.22, rely=0.39)
    pass_label.place(relx=0.22, rely=0.46)

    username_entry.place(relx=0.38, rely=0.25)
    fname_entry.place(relx=0.38, rely=0.32)
    lname_entry.place(relx=0.38, rely=0.39)
    # pass_entry.place(relx=0.38, rely=0.51)
    pass_entry.place(relx=0.38, rely=0.46)


        
    def change_pass():
       
        global pass_1_entry, pass_2_entry, pass_1_label, pass_2_label, cancel_change

        def change_clicked():
            pass_1_label.place_forget()
            pass_1_entry.place_forget()
            pass_2_label.place_forget()
            pass_2_entry.place_forget()
            cancel_change.place_forget()

        pass_1_label = ct.CTkLabel(frame_2_profile, text=f'New Password: \t ', text_font=("Helvetica", 11))
        pass_1_entry = ct.CTkEntry(frame_2_profile, width=220, height=8, borderwidth=3, relief='flat', show='*')
        pass_2_label = ct.CTkLabel(frame_2_profile, text=f'New Password: \t ', text_font=("Helvetica", 11))
        pass_2_entry = ct.CTkEntry(frame_2_profile, width=220, height=8, borderwidth=3, relief='flat', show='*')
        cancel_change = ct.CTkButton(frame_2_profile, text=f'Cancel Password Change',width=35, height=25, fg_color=btn_color, command=change_clicked)

        pass_1_label.place(relx=0.22, rely=0.6)
        pass_1_entry.place(relx=0.38, rely=0.6)
        pass_2_label.place(relx=0.22, rely=0.67)
        pass_2_entry.place(relx=0.38, rely=0.67)
        cancel_change.place(relx=0.38, rely=0.74)


    def save_info():
        
        # usrname = username_entry.get()
        usrname = welcome_username
        fname = fname_entry.get()
        lname = lname_entry.get()
        old_password = pass_entry.get()      # usporedit sa vec dobivenom iz sql
        
        try:
            new_password_1 = pass_1_entry.get()
            new_password_2 = pass_2_entry.get()
        
        except NameError:
             new_password_1 = ''
             new_password_2 = ''

        # promijena passworda i/ili drugi stvari
        if old_password == passw and new_password_1 == new_password_2 and new_password_1 != '':
            
            print(usrname, fname, lname, old_password, new_password_1, new_password_2)
            sql_data.update_user(fname, lname, usrname, new_password_1 )
            messagebox.showinfo('User Info', f'Successfully Updated! :)\nNew Password: {new_password_1}')
            
            pass_1_entry.delete(0, END)
            pass_2_entry.delete(0, END)

            my_profile()     

        # ako ne zelim promijeniti password onda moraju oba biti prazni '', ostaje stari password
        elif old_password == passw and new_password_1 == new_password_2 and new_password_1 == '' and new_password_2 == '':
            print(usrname, fname, lname, old_password, new_password_1, new_password_2)
            sql_data.update_user(fname, lname, usrname, old_password )
            messagebox.showinfo('User Info', 'Successfully Updated! :)')
           
            my_profile()

        elif old_password == passw and new_password_1 != new_password_2:
            messagebox.showwarning('Current Password', "New Passwords Don't Match. Try Again!")
        
        elif old_password == '':
            messagebox.showwarning('Current Password', 'Enter Your Current Password to Save Changes. Try Again!')
        
        elif old_password != passw:
            messagebox.showwarning('Current Password', 'Current Password is incorrect. Try Again!')
        
        else:
            messagebox.showwarning('Warning', 'Somthing Went Wrong. Try Again!')



    # BUTTONS
    change_pass_btn = ct.CTkButton(frame_2_profile, text='New Password',width=35, height=25, fg_color=btn_color, command=change_pass)
    to_plants_btn = ct.CTkButton(frame_2_profile, text='Go to Plants',width=35, height=25, fg_color=btn_color, command=plants_page)
    to_pots_btn = ct.CTkButton(frame_2_profile, text='Go to Pots',width=35, height=25, fg_color=btn_color, command=pots_page)
    save_info_btn = ct.CTkButton(frame_2_profile, text='Save',width=35, height=25, fg_color=btn_color, command=save_info)
    
    change_pass_btn.place(relx=0.38, rely=0.53)
    to_plants_btn.place(relx=0.22, rely=0.92)
    to_pots_btn.place(relx=0.35, rely=0.92)
    save_info_btn.place(relx=0.58, rely=0.92)


def log_in():
    global username_entry, password_entry
    # frame_1
    show_frame(frame_1)

    # LOG IN
    lbl_login = ct.CTkLabel(frame_1, text='WELCOME TO PYFLORA!\n\nLOG IN', text_font=("Helvetica", 14, 'bold'), text_color='grey' )
    lbl_login.grid(row=0, column=0, padx=25, pady=25)

    # frame_1b za username, password i button_signin
    frame_1b = ct.CTkFrame(master=frame_1, width=500, height=300, corner_radius=10, border_width=1, border_color='#EDFAE1',fg_color='#ADEE70')
    frame_1b.place(relx=0.25, rely=0.35)

    lbl_username = ct.CTkLabel(frame_1b, text='\nUsername', text_font=("Helvetica", 9, 'bold'))
    username_entry = ct.CTkEntry(frame_1b, width=200, height=8, borderwidth=3, relief='flat')
    lbl_password = ct.CTkLabel(frame_1b, text='\nPassword', text_font=("Helvetica", 9, 'bold'))
    password_entry = ct.CTkEntry(frame_1b, width=200, height=8, borderwidth=3, show='*', relief='flat')

    lbl_username.pack( padx=150, pady=5,)
    username_entry.pack(padx=25, pady=5) 
    lbl_password.pack( padx=25, pady=7, )
    password_entry.pack( padx=25, pady=10)

    # ovjde sada treba provjeriti upisano sa sql db, treba ove varijable global staviti 
    def check_credentials():
        global welcome_username
        welcome_username = username_entry.get()
        provjera = sql_data.username_exists(welcome_username, password_entry.get())

        # sqlite vraća None ako ne valjaju podaci za query username i password
        if provjera != None:
            welcome_page()
        else:
            messagebox.showerror("Try again", "Username/password not valid!\n\nTry admin 1111")
            password_entry.delete(0, END)
            
    # SIGN IN BUTTON
    button_signin= ct.CTkButton(master=frame_1b, text='Sign In', width=80, height=40, fg_color=btn_color, command=check_credentials)
    button_signin.pack(padx=25, pady=5)

log_in() # prikazat ce frame_1, prvo se otvara ova stranica kad se pokrece aplikacija



if __name__ == '__main__':
    root.mainloop()

