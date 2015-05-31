#!/usr/local/bin/python
  # -*- coding: utf-8 -*-
  # The above is needed to set the correct encoding, see https://www.python.org/dev/peps/pep-0263/

from werkzeug import secure_filename
from config import ALLOWED_EXTENSIONS_DOCS, ALLOWED_EXTENSIONS_PICS, BASE_PATH
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
    try:
        for i in xrange(0, 5):
            if request.files['foto{0}'.format(i)] or request.form['descrizione{0}'.format(i)]:      # filters a lot of empty pairs
                files.append(request.files['foto{0}'.format(i)])
                labels.append(request.form['descrizione{0}'.format(i)])
            files.append(request.files['foto'])
            labels.append(request.form['descrizione'])
    except KeyError:    # KeyError = Bad Request Error
        pass            # It means I'm trying to UPDATE less than 5 photos (see the structure of web-res-upload.html)
                        # or that I didn't added any new photo
    
    item['photos'] = zip(labels, files)
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

    for p in item['photos']:
        if p[0] == '' and p[1].filename != None:     # If I have a photo without the label
            raise ValueError( u"Impossibile caricare foto senza una descrizione." )

        if p[1].filename == '' and p[0] != '':      # Here I have only the label
            p = (p[0], '')                          # and I 'erase' the file
        # It is possible to UPDATE the label of an existing photo (so a pair label-nophoto is allowed),
        # while it is impossible to load a photo without a label, because the label is always rendered in the page
        # and thus loaded with the photo. In case of UPLOAD I must check again and raise errors for every unpaired label.
        
    for f in item['photos']:
        print '#########', f
        if not allowed_pic(f[1].filename):
            raise ValueError( u'''{0} non può essere caricato:<br>
                                  '*.{1}' non è tra le estensioni ammesse (ovvero {2}).<br>
                                  Ricarica le foto.
                               '''.format(f[1].filename, get_extension(f[1].filename), set_to_string(ALLOWED_EXTENSIONS_PICS)) )
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
    
    # See check_news()
    for l in item['photos']:
        if l[1]=='' and l[0]!= None:
            raise ValueError( u"Impossibile caricare una descrizione senza la relativa foto." )

    paths, labels = [], []
    for f in item['photos']:
        filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(f[1].filename)))
        f[1].save(os.path.join(app.config['UPLOAD_FOLDER_PICS'], filename))
        paths.append(filename)
        labels.append(f[0])

    pics = zip(xrange(len(paths)), labels, paths)
    cursor.execute("INSERT INTO news (data, title, text, pics) VALUES (?, ?, ?, ?)", [item['date'], item['title'], item['content'], json.dumps(pics)])
    return

def update_news(request, cursor, app, id):
    '''
        update_news(request, cursor, app, id):
    This function updates a news, meaning that it can identify and 
    overwrite a specific row in the database. Basically the same as the 
    above for the text parts, but slightly different concerning the 
    management of pictures.
    NB: it DOESN'T DEAL with the ValueErrors. The caller is supposed to
    manage them.
    '''
    item = load_news(request)
    check_news(item)
    
    print item['photos']
    
    
    
    
    #cursor.execute("UPDATE news SET data=?, title=?, text=?, pics=? WHERE id = ?", [item['date'], item['title'], item['content'], item['pics'], id])

    return item


# *********** NEWS PICTURES Management *********************************

def load_newspics(request, id):
    '''
        load_newspics(request, id):
    Loads everything from the request, without performing any valitation.
    Loads also the value of the 'new' flag as first element of the output 
    tuple. May raise only 'BAD REQUEST' (KeyError) errors.
    NB: requires the ID only to build a standard tuple, as found in the 
    database.
    '''
    return (id, request.form['descrizione'], request.files['foto'])

def retrieve_newspics(id, index, cursor):
    '''
        retrieve_newspics(request):
    Retrieve a specific picture of a specific news (found by index and 
    id respectively) from the database.
    '''
    pics = json.loads( cursor.execute("SELECT pics FROM news WHERE id=?", [id]).fetchone()[0] )
    if int(index) >= len(pics):
        raise ValueError(u'Index out of range')
    return pics[index]

def check_newspics(item):
    '''
        check_newspics(request):
    Performs some validation on the data loaded from loda_newspics() and 
    raises ValueError if something is wrong.
    Doesn't check if the value of the checkbox exists.
    '''
    if not item[1]:
        raise ValueError(u"Impossibile caricare una foto senza descrizione")
    if item[2]:
        if not allowed_pic(item[2].filename):
            raise ValueError(u"Upload fallito! Estensioni ammesse: {0}".format(set_to_string(ALLOWED_EXTENSIONS_PICS)) )
    return


def update_newspics(request, cursor, app, id, index):
    '''
        update_newspics(request, cursor, app, id):
    This function updates a single picture previously selected by the user.
    It handles two situations: or adds a new picture to the pictures
    list, or overwrites a specific picture (or its label). To distinguish 
    between the two situations it checks the value of the 'new' flag,
    the first value of the tuple returned by 'load_newspics()'
    '''    
    item = load_newspics(request, id)
    check_newspics(item)
    
    # I have to create a new list of tuples basing on the old one.
    old_pics = retrieve_item('news', id, cursor)['pics']
    
    if request.path[-3:]=='add':
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
            old = retrieve_newspics(id, index, cursor)
            
            filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(item[2].filename)))
            item[2].save(os.path.join(app.config['UPLOAD_FOLDER_PICS'], filename))
            old_pics[index][2] = filename
            try:
                os.remove(os.path.join(BASE_PATH, app.config['UPLOAD_FOLDER_PICS'], old[2]))
            except OSError:
                pass # If the file there isn't, I simply load a new one and leave the corrupted one (if exists) orphan.
                     # Should log about it, anyway
        if item[1]:
            old_pics[index][1] = item[1] 
            
        cursor.execute("UPDATE news SET pics=? WHERE id = ?", [json.dumps(old_pics), id])
    
    return
        
    
# *********** NOTES Management *****************************************  

def load_note(request):
    """
        load_note(request):
    Loads the content of the form without performing any convalidation.
    Loads also empty fields in the 'item' dictionary.
    """
    item = {'content': request.form['testo'] }
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
    return

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
        
    if not allowed_doc(item['file'].filename):
        raise ValueError(u"Upload fallito. Estensioni ammesse: {0}".format(set_to_string(ALLOWED_EXTENSIONS_DOCS)) )
        
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
    
    filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(item['file'].filename)))
    item['file'].save(os.path.join(app.config['UPLOAD_FOLDER_DOCS'], filename))
    
    cursor.execute("INSERT INTO docs (name, path) VALUES (?, ?)", [item['title'], filename])
    return

def update_doc(request, cursor, app, id):
    '''
        update_doc(request, cursor, app, id):
    This function updates a document, meaning that it can identify and 
    overwrite a specific row in the database. 
    NB #1: It doesn't call check_doc(), because the user may want to change
    only the label, without replacing the original file, and reverse.
    NB #2: it doesn't deal with the ValueErrors. The caller is supposed to
    manage them.
    '''
    item = load_doc(request)
    
    if item['file']:
        old_file = retrieve_item('doc', id, cursor)
        
        # First of all I upload the new file
        filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(item['file'].filename)))
        item['file'].save(os.path.join(app.config['UPLOAD_FOLDER_DOCS'], filename))
        cursor.execute("UPDATE docs SET path=? WHERE id = ?", [json.dumps(filename), id])
        
        #Then I remove the old one
        os.remove(os.path.join(BASE_PATH, app.config['UPLOAD_FOLDER_DOCS'], old_file['path']))
        
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
    
    
def retrieve_item(obj, id, cursor):
    '''
        retrieve_item(obj, id, cursor):
    Returns a dictionary with all the data regarding a specific object
    (found by id).
    OBJ == 'NEWS': Does not retrieve every photo, but a list of their 
    labels, and sets a flag (addphoto) if there are less than 5 pictures.
    
    '''
    if obj=='news':
        row = cursor.execute("SELECT * FROM news WHERE id == ?", [id]).fetchone()
        item = {'id':id, 'date':datetime_to_datepick(row[1]), 'title':row[2], 'content':row[3]}
        item['pics'] = json.loads(str(row[4]))

        if len(item['pics']) < 5:
            item['addphoto'] = True
        elif len(item['pics']) > 5:
            raise ValueError(u'Si è verificato un errore durante il caricamento delle foto.<br>Contatta il webmaster.')
            
    elif obj=='note':
        row = cursor.execute("SELECT * FROM notes WHERE id == ?", [id]).fetchone()
        item = {'id':id, 'content':row[1]}

    elif obj=='doc':
        row = cursor.execute("SELECT * FROM docs WHERE id == ?", [id]).fetchone()
        item = {'id':row[0], 'title':row[1], 'path':row[2]}
    
    else:
        raise ValueError(u'Unknown OBJ value.')

    return item

def retrieve_index(id, cursor):
    '''
        retrieve_index(id, cursor):
    This function retrieves the last available position in the list of 5
    photos related to a specific picture.
    '''
    try:
        index = len(json.loads( cursor.execute("SELECT pics FROM news WHERE id == ?", [id]).fetchone() ))
    except TypeError:
        index = 0   # Empty-list case, where json.loads() fails
        
    if index >= 5:
        raise ValueError(u"Errore durante il caricamento della lista.")
    return index


def delete_item(obj, cursor, app, id):
    '''
        delete_item(obj, cursor, id):
    Deletes a specific object in the database.
    '''
    if obj=='news':
        pics = retrieve_item(obj, id, cursor)['pics']
        for pic in pics:
            os.remove(os.path.join(BASE_PATH, app.config['UPLOAD_FOLDER_PICS'], pic[2]))
        cursor.execute('DELETE FROM news WHERE id == ?', [id])
    elif obj=='note':
        cursor.execute('DELETE FROM notes WHERE id == ?', [id])
    elif obj=='doc':
        try:
            os.remove(os.path.join(BASE_PATH, app.config['UPLOAD_FOLDER_DOCS'], retrieve_item(obj, id, cursor)['path']))
        except OSError:
            pass # If the file there isn't, or cannot be deleted, I simply delete its database entry and leave it orphan.
                 # Should log about it, anyway
        cursor.execute('DELETE FROM docs WHERE id == ?', [id])
    else:
        raise ValueError(u'Unknown OBJ value')
    return
