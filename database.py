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
#   pic(s):     file names with labels  (in a list of tuples, no dictionaries!)


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
    return item
    
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
    item = check_news(item)

    paths = []
    for f in item['files']:
        filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(f.filename)))
        f.save(os.path.join(app.config['UPLOAD_FOLDER_PICS'], filename))
        paths.append(filename)

    pics = zip(paths, item['labels'])
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
    item = check_news(item)
    cursor.execute("UPDATE news SET data=?, title=?, text=? WHERE id = ?", [item['date'], item['title'], item['content'], id])
    # Photos will be managed separately
    return item

# *********** NEWS PICTURES Management *********************************

def load_newspics(request, var):
    name = request.form['descrizione']
    f = request.files['foto']
    if not f.isfile():        # <----------------------------------------------- HERE
        var['upload'] = 'fail'
        var['msg'] = u"Upload fallito E NESSUNO SA PERCHE'! "
        return var      # This means that load_newspics already stated an error message that should reach the caller function
    if not allowed_pic(f.filename):
        var['upload'] = 'fail'
        var['msg'] = u"Upload fallito! Estensioni ammesse: {0}".format(set_to_string(ALLOWED_EXTENSIONS))
        var['photo'] = []
        return var
    var['photo'] = [f, name]
    print var['photo']
    return var


def update_newspics(request, var, cursor, app, id):
    new_pics = load_newspics(request, var)      # Loads the new photo
    if not new_pics:
        var['upload'] = 'fail'
        var['msg'] = u'Errore interno. Contatta il webmaster.'
        return var
    print "++++++++++++++++++++++++", new_pics
    
    photo = new_pics['photo']

    old_pics = retrieve_item('news', id, cursor)['pics']   # Retrieve the old list of photos for that news
    old_pics = [ [ph['path'], ph['title']] for ph in old_pics ]
    
    if var['new']:
        if len(old_pics) >= 5:
            var['upload'] = 'fail'
            var['msg'] = u'Impossibile caricare più di cinque fotografie.'
            return var
        filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(photo[0].filename)))
        photo[0].save(os.path.join(app.config['UPLOAD_FOLDER_PICS'], filename))
        old_pics.append([filename, photo[1]])
        cursor.execute("UPDATE news SET pics=? WHERE id = ?", [json.dumps(old_pics), id])
    else:
        if photo[0]:
            filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(photo[0].filename)))
            photo[0].save(os.path.join(app.config['UPLOAD_FOLDER_PICS'], filename))
            old_pics[var['index']][0] = filename
        if photo[1]:
            old_pics[var['index']][1] = photo[1]
        cursor.execute("UPDATE news SET pics=? WHERE id = ?", [json.dumps(old_pics), id])
    
    var["upload"] = 'success'
    var['msg'] = u"Upload completato con successo"
    return var    
        
    
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
    return item
    
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
    item = check_note(item)
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
    item = check_note(item)
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
    return item

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
    item = check_doc(item)

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
        raise ValueError(u'Errore durante il caricamento della lista.<br>Riprova o contatta il webmaster.')
    return lista


def retrieve_item(obj, id, cursor):
    if obj=='news':
        row = cursor.execute("SELECT * FROM news WHERE id == ?", [id]).fetchone()
        item = {'id':id, 'date':datetime_to_datepick(row[1]), 'title':row[2], 'content':row[3]}
        if row[4]:
            photos, captions = zip(* json.loads(str(row[4])) )
            pics = zip(xrange(len(photos)), photos, captions)
            item['pics'] = [ {'id':pic[0], 'path':pic[1], 'title':pic[2]} for pic in pics ]
            if len(photos) < 5:
                item['addphoto'] = True
       
    if obj=='note':
        row = cursor.execute("SELECT * FROM notes WHERE id == ?", [id]).fetchone()
        item = {'id':id, 'content':row[1]}
        
    if obj=='doc':
        row = cursor.execute("SELECT * FROM docs WHERE id == ?", [id]).fetchone()
        item = {'id':id, 'title':row[1], 'path':row[2]}
    
    return item
    
    
def retrieve_photo(id, index, cursor):
    pics = json.loads( cursor.execute("SELECT pics FROM news WHERE id=?", [id]).fetchone()[0] )
    if int(index) < len(pics):
        return pics[index]
    return 0
    

