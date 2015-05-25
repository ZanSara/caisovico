#!/usr/local/bin/python
  # -*- coding: utf-8 -*-
  # The above is needed to set the correct encoding, see https://www.python.org/dev/peps/pep-0263/

from werkzeug import secure_filename
from utils import datepick_to_datetime, datetime_to_datepick, allowed_pic, allowed_doc, set_to_string, get_extension
import sys, sqlite3, json, os, datetime
  


# *********** NEWS Management ******************************************

# Legend:   
#   file(s):    file objects without labels
#   photo(s):   file objects with labels (in a list of tuples, no dictionaries!)
#   path(s)     file names without labels
#   pic(s):     file names with labels and ID (in a list of tuples, no dictionaries!)
#   Remember! In the tuples, the order is (<index>, label, photo)


def load_news(request):
    """
        load_news(request):
    Loads all the data from the form without performing any convalidation.
    Loads also any empty field in the 'item' dictionary.
    """
    item = {}
    item['title'] = request.form['titolo']
    item['content'] = request.form['testo']
    item['date'] = request.form['data']
    
    files, labels = [], []
    for i in xrange(1, 6):
        if request.files['foto{0}'.format(i)]:
            files.append(request.files['foto{0}'.format(i)])
            labels.append(request.form['descrizione{0}'.format(i)])

    item['files'] = files
    item['labels'] = labels
    return item
    
def retrieve_news(id, cursor):
    '''
        retrieve_news(id, cursor):
    Returns a dictionary with all the data regarding a specific news
    (found by id).
    Does not retrieve every photo, but a list of their labels, and sets 
    a flag (addphoto) if there are less than 5 pictures.
    '''
    row = cursor.execute("SELECT * FROM news WHERE id == ?", [id]).fetchone()
    item = {'id':id, 'date':datetime_to_datepick(row[1]), 'title':row[2], 'content':row[3]}
    item['pics'] = json.loads(str(row[4]))
    
    if len(item['pics']) < 5:
        item['addphoto'] = True
    elif len(item['pics']) > 5:
        raise ValueError(u'Si è verificato un errore durante il caricamento delle foto.<br>Contatta il webmaster.')
    return item
    
def check_news(item):
    '''
        check_news(item):
    Performs convalidation on the data loaded from load_news() and raises
    ValueError if something is wrong.
    '''
    if not item['title']:
        raise ValueError(u'Impossibile caricare una notizia senza titolo') 
    if not item['content']:
        raise ValueError(u'Impossibile caricare una notizia senza testo')
    # datepick_to_datetime() itself will raise the ValueError in case
    item['date'] = datepick_to_datetime(item['date']) 

    for l in item['labels']:
        if l=='':
            raise ValueError( u"Impossibile caricare foto senza una descrizione." )
            
    for f in item['files']:
        if not allowed_pic(f.filename):
            raise ValueError( u'''{0} non può essere caricato:<br>
                                  '*.{1}' non è tra le estensioni ammesse. (ovvero {2})<br>
                                  Ricarica le foto.
                               '''.format(f.filename, get_extension(f.filename), set_to_string(ALLOWED_EXTENSIONS)) )
                               # Secondary issue: now the user have to reload all the photos. 
                               # It is possible to let him see again what they loaded, and correct?
    return
    
def upload_news(request, cursor, app):
    '''
        upload_news(request, cursor, app):
    This function performs a fresh upload of all the material previously
    loaded and checked.
    It adds a new row in the database without overwriting anything.
    In case of failure, it returns all the non-checked raw loaded data, 
    to be displayed again to the user and let they correct it.
    NB: it DOESN'T DEAL with the ValueErrors. The caller is supposed to
    manage them.
    '''
    item = load_news(request)
    check_news(item)

    paths = []
    for f in item['files']:
        filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(f.filename)))
        f.save(os.path.join(app.config['UPLOAD_FOLDER_PICS'], filename))
        paths.append(filename)

    pics = zip(xrange(len(paths)), item['labels'], paths)
    cursor.execute("INSERT INTO news (data, title, text, pics) VALUES (?, ?, ?, ?)", [item['date'], item['title'], item['content'], json.dumps(pics)])
    return

def update_news(request, cursor, app, id):
    '''
        update_news(request, cursor, app, id):
    This function updates a news, meaning that it can identify and overwrite
    a specific row in the database. Basically the same as the above for
    the text parts, but slightly different concerning the management of pictures
    (see update_newspics() )
    NB: it DOESN'T DEAL with the ValueErrors. The caller is supposed to
    manage them.
    '''
    item = load_news(request)
    check_news(item)
    cursor.execute("UPDATE news SET data=?, title=?, text=? WHERE id = ?", [item['date'], item['title'], item['content'], id])
    # Photos will be managed separately
    return item


# *********** NEWS PICTURES Management *********************************

def load_newspics(request):
    '''
        load_newspics(request):
    Loads everything from the request, without performing any valitation.
    Loads also the value of the 'new'flag as first element of the output 
    tuple. May raise only 'BAD REQUEST' errors.
    '''
    return (request.form['new'], request.form['descrizione'], request.files['foto'])

def retrieve_newspics(id, index, cursor):
    '''
        retrieve_newspics(request):
    Retrieve a specific picture of a specific news (found by index and 
    id respectively) from the database.
    '''
    pics = json.loads( cursor.execute("SELECT pics FROM news WHERE id=?", [id]).fetchone()[0] )
    if int(index) < len(pics):
        return pics[index]
    raise ValueError(u'Index out of range')
    return

def check_newspics(item):
    '''
        check_newspics(request):
    Performs some validation on the data loaded from loda_newspics() and 
    raises ValueError if something is wrong.
    Doesn't check if the value of the checkbox exists.
    '''
    if not item[1]:
        raise ValueError(u"Impossibile caricare una foto senza descrizione")
    if file:
        if not allowed_pic(item[2].filename):
            raise ValueError(u"Upload fallito! Estensioni ammesse: {0}".format(set_to_string(ALLOWED_EXTENSIONS)) )
    return


def update_newspics(request, cursor, app, id):
    '''
        update_newspics(request, cursor, app, id):
    This function updates a single picture previously selected by the user.
    It handles two situations: or adds a new picture to the pictures
    list, or overwrites a specific picture (or its label). To distinguish 
    between the two situations it checks the value of the 'new' flag,
    the first value of the tuple returned by 'load_newspics()'
    '''    
    item = load_newspics(request)
    check_newspics(item)
    
    # I have to create a new list of tuples basing on the old one.
    old_pics = retrieve_item('news', id, cursor)['pics']
    
    if item['new']==True:
        # If the flag 'new' is set to True, I simply need to append the 
        # new picture to the old list and overwrite the paths' list in 
        # the database
        if len(old_pics) >= 5:
            raise ValueError(u'Impossibile caricare più di 5 fotografie')
            
        filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(item[2].filename)))
        item[2].save(os.path.join(app.config['UPLOAD_FOLDER_PICS'], filename))
        
        # The index of the last photo is equal to the lenght of the list
        old_pics.append( (len(old_pics), item[1], filename) )
        
        cursor.execute("UPDATE news SET pics=? WHERE id = ?", [json.dumps(old_pics), id])
        
    else:
        # If the flag 'new' is set to False, I need to overwrite a 
        # specific photo, recognizable by its index, and then overwrite
        # the paths' list in the database.
        # Note: in this case is also possible that I need to overwrite
        # only the label of the photo
        
        if item[2]:
            filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(item[2].filename)))
            item[2].save(os.path.join(app.config['UPLOAD_FOLDER_PICS'], filename))
            
            # item[0] = index of the new photo
            # old_pics[n][0] = filename of the n-th photo
            old_pics[item[0]][2] = filename
            # In this way I upload a new picture keeping the same label
            
        if item[1]:
            old_pics[item[0]][1] = item[1] 
            
        cursor.execute("UPDATE news SET pics=? WHERE id = ?", [json.dumps(old_pics), id])
    
    return item
        
    
# *********** NOTES Management *****************************************  

def load_note(request):
    """
        load_note(request):
    Loads the content of the form without performing any convalidation.
    Loads also empty fields in the 'item' dictionary.
    """
    item = {'content': request.form['testo'] }
    return item


def retrieve_note(id, cursor):
    """
        retrieve_note(id, cursor):
    Retrieves the text of a note from the database, by ID
    """
    row = cursor.execute("SELECT * FROM notes WHERE id == ?", [id]).fetchone()
    item = {'id':id, 'content':row[1]}
    return item

def check_note(item):
    '''
        check_note(item):
    Performs convalidation on the data loaded from load_note() and 
    raises ValueError if something is wrong.
    '''
    if not item['content']:
        raise ValueError(u'Impossibile caricare una nota vuota') 
    return
    
def upload_note(request, cursor):
    '''
        upload_note(request, cursor):
    This function performs a fresh upload of the loaded and checked note.
    It adds a new row in the database without overwriting anything.
    In case of failure, it returns the non-checked note, to be displayed 
    again to the user and let they correct it.
    NB: it DOESN'T DEAL with the ValueErrors. The caller is supposed to
    manage them.
    '''
    item = load_note(request)
    check_note(item)
    cursor.execute("INSERT INTO notes VALUES (null, ?)", [item['content']])
    return

def update_note(request, cursor, id):
    '''
        update_note(request, cursor, id):
    This function updates a note, meaning that it can identify and overwrite
    a specific row in the database. Basically the same as the above, only 
    the database request is different.
    NB: it DOESN'T DEAL with the ValueErrors. The caller is supposed to
    manage them.
    '''
    item = load_note(request)
    check_note(item)
    cursor.execute("UPDATE notes SET text = ? WHERE id = ?", [item['content'], id])
    return item

# *********** DOCS Management ******************************************
    
def load_doc(request):
    """
        load_doc(request):
    Loads all the data from the form without performing any convalidation.
    Loads also any empty field in the 'item' dictionary.
    """
    item = {}
    item['title'] = request.form['descrizione']
    item['file'] = request.files['doc']
    return item
    
def retrieve_doc(id, cursor):
    """
        retrieve_doc(id, cursor):
    Retrieves filename and title of the selected document (by ID)
    """
    row = cursor.execute("SELECT * FROM docs WHERE id == ?", [id]).fetchone()
    item = {'id':id, 'title':row[1], 'path':row[2]}
    return item

def check_doc(item):
    '''
        check_doc(item):
    Performs convalidation on the data loaded from load_doc() and raises
    ValueError if something is wrong.
    '''
    if not item['title']:
        raise ValueError(u'Impossibile caricare documento senza descrizione') 
        # Secondary issue: the user does not find their file after seeing 
        # the error message.
    if not item['file']:
        raise ValueError(u'Nessun file selezionato')
    if not allowed_doc(f.filename):
        raise ValueError(u"Upload fallito. Estensioni ammesse: {0}".format(set_to_string(ALLOWED_EXTENSIONS)) )
    return
    
def upload_doc(request, cursor, app):
    '''
        upload_doc(request, cursor, app):
    This function performs a fresh upload of all the data previously
    loaded and checked.
    It adds a new row in the database without overwriting anything.
    In case of failure, it returns all the non-checked raw loaded data, 
    to be displayed again to the user and let they correct it.
    NB: it DOESN'T DEAL with the ValueErrors. The caller is supposed to
    manage them.
    '''
    item = load_doc(request)
    check_doc(item)

    filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(f.filename)))
    f.save(os.path.join(app.config['UPLOAD_FOLDER_PICS'], filename))
    
    cursor.execute("INSERT INTO docs (name, path) VALUES (?, ?)", [item['title'], json.dumps(filename)])
    return

def update_doc(request, cursor, app, id):
    '''
        update_doc(request, cursor, app, id):
    This function updates a document, meaning that it can identify and 
    overwrite a specific row in the database. 
    NB #1: It doesn't call check_doc(), because the user may want to change
    only the label, without replacing the original file, and reverse.
    NB #2: it DOESN'T DEAL with the ValueErrors. The caller is supposed to
    manage them.
    '''
    item = load_doc(request)
    
    if item['file']:
        filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(f.filename)))
        f.save(os.path.join(app.config['UPLOAD_FOLDER_PICS'], filename))
        cursor.execute("UPDATE docs SET path=? WHERE id = ?", [json.dumps(filename), id])
    if item['title']:
        cursor.execute("UPDATE docs SET name=? WHERE id = ?", [item['title'], id])
    else:
        raise ValueError(u'''Impossibile caricare un documento senza titolo.<br>
                             Se il titolo non è stato caricato automaticamente, contatta il webmaster.''')
    return item

 
# *********** Others ***************************************************

def load_lista(obj, cursor):
    '''
        load_lista(obj, cursor):
    This function retrieve a list of the elements in a specific table of 
    the database. Overwrites the actual content of every Exception raised
    during the loading process, resulting in a generic error message for 
    the user.
    '''
    lista = []
    try:
        if obj=='news':
            for item in cursor.execute("SELECT id, data, title FROM news").fetchall():
                lista.append( {'id':item[0], 'data':item[1], 'title':item[2]  } )
        if obj=='note':
            for item in cursor.execute("SELECT id, text FROM notes").fetchall(): 
                lista.append( {'id':item[0], 'title':item[1] } )
        if obj=='doc':
            for item in cursor.execute("SELECT id, name FROM docs").fetchall(): 
                lista.append( {'id':item[0], 'title':item[1] } )
    except Exception:
        raise Exception(u'Errore durante il caricamento della lista.<br>Riprova o contatta il webmaster.')
    return lista
    
    

    

