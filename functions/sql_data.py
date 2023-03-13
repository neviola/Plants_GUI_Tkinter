import sqlite3


conn = sqlite3.connect('pyflora.db')
cursor = conn.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS Users (
                    fname TEXT,
                    lname TEXT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL  
                                                 )""")

cursor.execute(""" CREATE TABLE IF NOT EXISTS Plants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    foto BLOB,s
                    name TEXT,
                    info TEXT                     
                                                 )""")

cursor.execute(""" CREATE TABLE IF NOT EXISTS Pots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    name TEXT,
                    plant_id INTEGER KEY REFERENCES Plants(id)                    
                                                 )""")


def username_exists(username, password):

    cursor.execute('SELECT * FROM Users WHERE username = :user AND password = :pass', {'user' :username, 'pass': password})
    ime = cursor.fetchone()
    return ime                  # returns None ako ne postoji username ili password, inače tuple


def insert_user(fname, lname, username, password):
    with conn:
        try:
            cursor.execute('''INSERT INTO Users 
                                VALUES (:fname, :lname, :username, :password)''', {'fname' :fname, 'lname' :lname,
                                                                                    'username': username, 'password':password })
        except sqlite3.IntegrityError:
            return -1 #'Password already exists'

# insert_user('ivan', 'ivanic', 'admin', '1234')


def load_user_info(username):
    with conn:
        cursor.execute('SELECT fname, lname, password FROM Users WHERE username = :user', {'user' :username})
        user_info = cursor.fetchone()
        return user_info


def update_user(fname, lname, username, password):
    with conn:
        cursor.execute('''UPDATE Users 
                          SET fname = :fname, lname = :lname, password = :password
                          WHERE username = :username''', {'fname': fname, 
                          	                              'lname': lname, 
                                                          'password': password,
                                                          'username': username})


def to_binary(path):
    with open (path, 'rb') as f:
        binar_photo = f.read()
        return binar_photo


def insert_plant(id, foto, name, info):   
    with conn:
        try:
            cursor.execute('''INSERT INTO Plants 
                                VALUES (:id, :foto, :name, :info)''', {'id' :id,
                                                                       'foto' :foto,
                                                                       'name': name,
                                                                       'info': info })
        except:
            return -1   # vrati -1 ako id vec postoji

# insert_plant(3, to_binary('./plant_pics/chili.jpg'), 'chili', 'Zalijevati 1 tjedno, drzati na suncanom dijelu')


def load_photo(id):
    # Ucitava binarnu sliku iz sqla i zapisuje kao plant_from_bin.png pa to mogu ucitati u Tk
    with conn:
        cursor.execute('SELECT foto, name, info FROM Plants WHERE id = :iid', {'iid' :id})
        img_tuple = cursor.fetchone()
        img_bin = img_tuple[0]
        img_name = img_tuple[1]
        img_info = img_tuple[2]
        
        with open('./photos/plant_from_bin.png', 'wb') as f:
            f.write(img_bin)
        return img_name, img_info
      

def load_plant_name(id):
    with conn:
        cursor.execute('SELECT name FROM Plants WHERE id = :iid', {'iid' :id})
        plants_list = cursor.fetchone()
        return plants_list


def load_plant_id(name):
    with conn:
        cursor.execute('SELECT id FROM Plants WHERE name = :name', {'name' :name})
        plants_list = cursor.fetchall()
        return plants_list


def load_plants():
    with conn:
        cursor.execute('SELECT id, name, info FROM Plants ')
        plants_list = cursor.fetchall()
        return plants_list
    

def update_plant(id, new_info):
    with conn:
        cursor.execute('''UPDATE Plants 
                          SET info = :new_info
                          WHERE id = :id''', {'new_info':new_info,  
                                              'id':id})


def update_plant_image(id, new_photo):
    with conn:
        cursor.execute('''UPDATE Plants 
                          SET foto = :new_foto
                          WHERE id = :id''', {'new_foto':new_photo,  
                                              'id':id})


def delete_plant(id):
    with conn:
        cursor.execute('''DELETE FROM Plants 
                          WHERE id = :id''', {'id':id})



##################  POT Methods ################

def insert_pot(id, name, plant_id):   
    with conn:
        try:
            cursor.execute('''INSERT INTO Pots 
                                VALUES (:id, :name, :plant_id)''', {'id' :id,
                                                                    'name': name,
                                                                    'plant_id': plant_id })
        except:
            return -1 


def load_pots():
    with conn:
        cursor.execute('SELECT id, name, plant_id FROM Pots')
        pots_list = cursor.fetchall()
        return pots_list


def delete_pot(id):
    with conn:
        cursor.execute('''DELETE FROM Pots 
                          WHERE id = :id''', {'id':id})


def load_one_pot(id):
    # Ucitava binarnu sliku iz sqla i zapisuje kao plant_from_bin.png pa to mogu ucitati u Tk
    with conn:
        cursor.execute('SELECT name, plant_id FROM Pots WHERE id = :iid', {'iid' :id})
        pot_tuple = cursor.fetchone()
        pot_name = pot_tuple[0]
        plant_id = pot_tuple[1]
        
        return pot_name, plant_id


def update_pot(pot_id, plant_id):
    with conn:
        cursor.execute('''UPDATE Pots 
                          SET plant_id = :new_plant_id
                          WHERE id = :pot_id''', {'new_plant_id':plant_id,  
                                                  'pot_id':pot_id})