 #!/usr/local/bin/python
  # -*- coding: utf-8 -*-
  # The above is needed to set the correct encoding, see https://www.python.org/dev/peps/pep-0263/
    

from flask import session
from config import DATABASE_PATH, ALLOWED_EXTENSIONS_PICS, ALLOWED_EXTENSIONS_DOCS
import sys, sqlite3, datetime


def login(name, passw):
    conn = sqlite3.connect(DATABASE_PATH)
    with conn:
        user = list(conn.execute("SELECT * FROM users WHERE username = ?", ([name])))
        try:
            if user[0][1] != passw:       # Suppose that I will get only one user with this username
                raise ValueError("Password errata")
            session["logged_in"] = True
            session["username"] = user[0][0]
            return
        except IndexError:
            raise ValueError("Nome utente non valido")
            return


def logout():
    if not session.pop("logged_in", None):
        raise Exception("Logout fallito. Torno nell'Area Riservata e riprova.")
    return



def datepick_to_datetime(data):
    """ Convert the date format given by datepickr (string) into the datetime format """
    if str(data).count("/") != 2:
        raise ValueError('Inserire una data valida')
        return
    d = data.split("/")
    return datetime.date(int(d[2]), int(d[1]), int(d[0]))
def datetime_to_datepick(data):
    """ Convert the date in the datetime format into the format given by datepickr (string) """
    if str(data).count("-") != 2:
        return
    d = data.split("-")
    return '/'.join([d[2], d[1], d[0]])


def allowed_pic(filename):
    """ Checks for the file extension to be one of the allowed ones """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PICS
def allowed_doc(filename):
    """ Checks for the file extension to be one of the allowed ones """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_DOCS


def set_to_string(myset):
    mystring = ''
    for item in list(myset):
        mystring = '{0} {1},'.format(mystring, item)
    return mystring[1:-1]
        
def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()
    
    
