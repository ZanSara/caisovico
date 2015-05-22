#!/usr/local/bin/python
  # -*- coding: utf-8 -*-
  # The above is needed to set the correct encoding, see https://www.python.org/dev/peps/pep-0263/

from werkzeug import secure_filename
from utils import datepick_to_datetime, datetime_to_datepick, allowed_file, set_to_string, get_extension
from config import ALLOWED_EXTENSIONS
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
    Load all the data from the form without performing any convalidation.
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
        check_news(item)
    Performs convalidation on the data loaded from load_news()
    '''
    if not item['title']:
        raise ValueError(u'Impossibile caricare una notizia senza titolo')
        return 
    if not item['content']:
        raise ValueError(u'Impossibile caricare una notizia senza testo')
        return
    try:
        item['date'] = datepick_to_datetime(item['date'])
    except ValueError:
        raise
        return item

    for l in item['labels']:
        if l=='':
            raise ValueError( u"Inserire i titoli di tutte le foto." )
            return item
    for f in files:
        if not allowed_file(f.filename):
            raise ValueError( u'''{0} non può essere caricato.<br>
                                  {1} non è tra le estensioni ammesse. ({2})
                               '''.format(f.filename, get_extension(f.filename), set_to_string(ALLOWED_EXTENSIONS)) )
            # ISSUE:
            # The user does not find their files after reading the error,
            # but finds all the capitons. This can be confusing.
            return item
    return item
    
def upload_news(request, cursor, app):
    item = load_news(request)
    print 'UPLOAD NEWS:', item
    try:
        item = check_news(item)
        print item
        paths = []
        for f in item['files']:
            filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(f.filename)))
            f.save(os.path.join(app.config['UPLOAD_FOLDER_PICS'], filename))
            paths.append(filename)
        pics = zip(paths, item['labels'])
        cursor.execute("INSERT INTO news (data, title, text, pics) VALUES (?, ?, ?, ?)", [item['date'], item['title'], item['content'], json.dumps(pics)])            
    except ValueError:
        print 'VALUE ERROR:', item
        raise
    except KeyError:
        print 'KEY ERROR:', item
        raise Exception('ERRORE: KeyError in upload_news(). Contatta il webmaster.')
    finally:
        return item
    


def update_news(request, var, cursor, app, id):
    var = load_news(request, var)
    if var['item']:
        item = var['item']
        cursor.execute("UPDATE news SET data=?, title=?, text=? WHERE id = ?", [item['date'], item['title'], item['content'], id])
        # Photos can be managed separately
        var["upload"] = 'success'
        var['msg'] = u"Upload completato con successo"
    return var

# *********** NEWS PICTURES Management *********************************

def load_newspics(request, var):
    name = request.form['descrizione']
    f = request.files['foto']
    if not f.isfile():        # <----------------------------------------------- HERE
        var['upload'] = 'fail'
        var['msg'] = u"Upload fallito E NESSUNO SA PERCHE'! "
        return var      # This means that load_newspics already stated an error message that should reach the caller function
    if not allowed_file(f.filename):
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
    
def load_note(request, var):
    text = request.form['testo']
    if not text:
        var['msg'] = u"Impossibile caricare una nota vuota"
        return var 
    var['item'] = {'content': text }
    return var 
    
def upload_note(request, var, cursor):
    var = load_note(request, var)
    if var['item']:
        item = var['item']
        cursor.execute("INSERT INTO notes VALUES (null, ?)", [item['content']])
        var["upload"] = 'success'
        var['msg'] = u"Upload completato con successo"
    return var

def update_note(request, var, cursor, id):
    var = load_note(request, var)
    if var['item']:
        item = var['item']
        cursor.execute("UPDATE notes SET text = ? WHERE id = ?", [item['content'], id])
        var["upload"] = 'success'
        var['msg'] = u"Upload completato con successo"
    return var
    

# *********** DOCS Management ******************************************

def load_doc(request, var):
    name = request.form['descrizione']
    f = request.files['doc']
    if not name:
        var['msg'] = u"Inserire il nome del documento"
        return var
    if not f:
        var['msg'] = u"Nessun file selezionato"
        return var
    if not allowed_file(f.filename):
        var['msg'] = u"Upload fallito! Estensioni ammesse: {0}".format(set_to_string(ALLOWED_EXTENSIONS))
        return var
    var['item'] = {'title':name, 'file': f}
    return var
  
  
def upload_doc(request, var, cursor, app):
    var = load_doc(request, var)
    if var['item']:
        item = var['item']
        filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(item['file'].filename)))
        item['file'].save(os.path.join(app.config['UPLOAD_FOLDER_DOCS'], filename))
        cursor.execute("INSERT INTO docs (name, path) VALUES (?, ?)", [item['title'], json.dumps(filename)])
        var["upload"] = 'success'
        var['msg'] = u"Upload completato con successo"
    return var
 
 
def update_doc(request, var, cursor, app, id):
    var = load_doc(request, var)
    if var['item']:
        item = var['item']
        if item['file']:
            filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(item['file'].filename)))
            item['file'].save(os.path.join(app.config['UPLOAD_FOLDER_DOCS'], filename))
            cursor.execute("UPDATE docs SET path=? WHERE id = ?", [json.dumps(filename), id])
        cursor.execute("UPDATE docs SET name=? WHERE id = ?", [item['title'], id])
        var["upload"] = 'success'
        var['msg'] = u"Upload completato con successo"
    return var
 

 
# *********** Others ***************************************************

def load_lista(obj, cursor):
    lista = []
    if obj=='news':
        for item in cursor.execute("SELECT id, data, title FROM news").fetchall():
            lista.append( {'id':item[0], 'data':item[1], 'title':item[2]  } )
    if obj=='note':
        for item in cursor.execute("SELECT id, text FROM notes").fetchall(): 
            lista.append( {'id':item[0], 'title':item[1] } )
    if obj=='doc':
        for item in cursor.execute("SELECT id, name FROM docs").fetchall(): 
            lista.append( {'id':item[0], 'title':item[1] } )
    if lista == []:
        lista = [{'id':0, 'date':'', 'title':u'Errore durante il caricamento della lista.<br>Riprova o contatta il webmaster.'}]
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
    print pics
    if int(index) < len(pics):
        return pics[index]
    return 0
    

