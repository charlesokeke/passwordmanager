import sqlite3
import getpass
import os
import string
import random
import datetime
from sqlite3 import Error


class Main:
    #self.database = "C:\\Users\\" + getpass.getuser() + "\\Desktop\\Dbfolder\\pswDb.db"
    def __init__(self):
        if not os.path.exists('C:\\Users\\' + getpass.getuser() + '\\Desktop\\Dbfolder'):
            os.mkdir('C:\\Users\\' + getpass.getuser() + '\\Desktop\\Dbfolder')
        self.database = "C:\\Users\\" + getpass.getuser() + "\\Desktop\\Dbfolder\\pswDb.db"
        self.conn = self.create_connection()
        self.sql_create_site_table = """ CREATE TABLE IF NOT EXISTS site_data (
                                                user_id integer PRIMARY KEY,
                                                password text NOT NULL,
                                                name text NOT NULL,
                                                user_data_id integer NOT NULL,
                                                date text,
                                                site text,
                                                FOREIGN KEY(user_data_id) REFERENCES user_data(id)
         
                                            ); """
        self.sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user_data (
                                                        id integer PRIMARY KEY,
                                                        user_id text NOT NULL,
                                                        password text NOT NULL,
                                                        date text
                                                        

                                                    ); """
        self.create_table()

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.database)
            conn.execute("PRAGMA foreign_keys = 1")
            return conn
        except Error as e:
            print(e)
        return conn

    def create_table(self):
        try:
            c = self.conn.cursor()
            c.execute(self.sql_create_user_table)
            c.execute(self.sql_create_site_table)
        except Error as e:
            print(e)

    def init_passwd(self):
        generated_password = ""
        alphabet_string_lowercase = string.ascii_lowercase
        alphabet_string_uppercase = string.ascii_uppercase
        special_characters = list(set(string.punctuation))
        numbers = string.digits

        while len(generated_password) <= 12:
            generated_password += alphabet_string_lowercase[random.randint(0, len(alphabet_string_lowercase) - 1)]
            generated_password += alphabet_string_uppercase[random.randint(0, len(alphabet_string_uppercase) - 1)]
            generated_password += special_characters[random.randint(0, len(special_characters) - 1)]
            generated_password += numbers[random.randint(0, len(numbers) - 1)]

        # print("".join((random.sample(list(generated_password), len(generated_password) - 1))))
        generated_password = list(generated_password)
        random.shuffle(generated_password)
        generated_password = "".join(generated_password)
        return generated_password

    def insert_password(self, task):
       try:
           sql = f''' INSERT INTO site_data(password, name,user_data_id,date,site)
                                       VALUES(?,?,?,?,?) '''
           cur = self.conn.cursor()
           #t = list(task)
           #t.insert(0, self.init_passwd())
           cur.execute(sql, task)
           self.conn.commit()
           return cur.lastrowid
       except Error as e:
           print(e)

    def find_password(self, data,id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM site_data WHERE site LIKE ? AND user_data_id=? ", (data,id))
        rows = cur.fetchall()
        return rows

    def find_all_password(self,id):
        # enviroment variable will be set when user logs in or created. Use that variable to fin all password
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM site_data WHERE user_data_id =?",(id,))
        rows = cur.fetchall()
        return rows

    def delete_password(self, id):

        sql = 'DELETE FROM user_data WHERE id=?'
        cur = self.conn.cursor()
        cur.execute(sql, (id,))
        self.conn.commit()

    def delete_all_password(self):
        sql = 'DELETE FROM user_data'
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

    def insert_user(self, task):
        #create an enviroment variable when a user is created
        sql = f''' INSERT INTO user_data(user_id, password,date)
                  VALUES(?,?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, task)
        self.conn.commit()
        print(cur.lastrowid)
        return cur.lastrowid

    def authenticate(self, user_id, password):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM user_data WHERE user_id=? AND password=? ", (user_id, password))
            found_user = cur.fetchone()
            print(found_user)
            return found_user
        except Error as e:
            print(e)
            return False
#user = Main()
#user.insert_user(("charles","charles",datetime.date.today()))
#user.insert_password(("tesfa",3,datetime.date.today(),"yahoo.com"))
# user.authenticate("Tesfa","password")
#user.insert_user(("Tesfa","password",datetime.date.today()))



