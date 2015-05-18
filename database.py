#!/usr/local/bin/python
  # -*- coding: utf-8 -*-
  # The above is needed to set the correct encoding, see https://www.python.org/dev/peps/pep-0263/

from werkzeug import secure_filename
from utils import datepick_to_datetime, datetime_to_datepick, allowed_file, set_to_string, get_extension
from config import ALLOWED_EXTENSIONS
import sqlite3, json, os, datetime
  


# *********** NEWS Management ******************************************

def load_news(request, var):
    title = request.form['titolo']
    text = request.form['testo']
    date = request.form['data']
    if not datepick_to_datetime(date):
        var['msg'] = "Inserire una data valida"
        return var
    if not title:
        var['msg'] = "Impossibile caricare una notizia senza titolo"
        return var
    if not text:
        var['msg'] = "Impossibile caricare una notizia senza testo"
        return var
        
    photo = []
    caps = []
    for i in xrange(1, 5):
        if request.files['foto{0}'.format(i)]:
            photo.append(request.files['foto{0}'.format(i)])
            caps.append(request.form['descrizione{0}'.format(i)])
            
    for f in photo:
        if f:
            if not allowed_file(f.filename):
                var['msg'] = "Attenzione! Le foto non possono essere caricate.<br>Controlla le estensioni! Estensioni ammesse: {0}".format(set_to_string(ALLOWED_EXTENSIONS))
                return var
    var['item'] = {'title':title, 'date':datepick_to_datetime(date), 'content':text, 'caps':caps, 'photo':photo}            
    return var
    
    
def upload_news(request, var, cursor, app):
    var = load_news(request, var)
    item = var['item']
    
    if var['item']:
        paths = []
        for f in item['photo']:
            filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(f.filename)))
            f.save(os.path.join(app.config['UPLOAD_FOLDER_PICS'], filename))
            paths.append(filename)
        pics = json.dumps(zip(paths, item['caps']))
        cursor.execute("INSERT INTO news (data, title, text, pics) VALUES (?, ?, ?, ?)", [item['date'], item['title'], item['content'], pics])
        
        var['item'] = { 'title':item['title'], 'date':item['date'], 'content':item['content'], 'pics':pics }
        var['upload_fail'] = 0
        var["upload_success"] = 'success'
        var['msg'] = "Upload completato con successo"
    return var

def update_news(request, var, cursor, app, id):
    pass
    
# *********** NOTES Management *****************************************  
    
def load_note(request, var):
    text = request.form['testo']
    if not text:
        var['msg'] = "Impossibile caricare una nota vuota"
        return var 
    var['item'] = {'content': text }
    return var 
    
def upload_note(request, var, cursor):
    var = load_note(request, var)
    if var['item']:
        item = var['item']
        cursor.execute("INSERT INTO notes VALUES (null, ?)", [item['content']])
        var['upload_fail'] = 0
        var["upload_success"] = 'success'
        var['msg'] = "Upload completato con successo"
    return var

def update_note(request, var, cursor, id):
    var = load_note(request, var)
    if var['item']:
        item = var['item']
        cursor.execute("UPDATE notes SET text = ? WHERE id = ?", [item['content'], id])
        var['upload_fail'] = 0
        var["upload_success"] = 'success'
        var['msg'] = "Upload completato con successo"
    return var
    

# *********** DOCS Management ******************************************

def load_doc(request, var):
    name = request.form['descrizione']
    f = request.files['doc']
    if not name:
        var['msg'] = "Inserire il nome del documento"
        return var
    if not f:
        var['msg'] = "Nessun file selezionato"
        return var
    if not allowed_file(f.filename):
        var['msg'] = "Upload fallito! Estensioni ammesse: {0}".format(set_to_string(ALLOWED_EXTENSIONS))
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
        var["upload_fail"] = 0
        var["upload_success"] = 'success'
        var['msg'] = "Upload completato con successo"
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
        var['upload_fail'] = 0
        var["upload_success"] = 'success'
        var['msg'] = "Upload completato con successo"
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
        lista = [{'id':0, 'date':'', 'title':'Errore durante il caricamento della lista.<br>Riprova o contatta il webmaster.'}]
    return lista


def retrieve_item(obj, id, cursor):
    if obj=='news':
        row = cursor.execute("SELECT * FROM news WHERE id == ?", [id]).fetchone()
        data = datetime_to_datepick(row[1])
        item = {'data':data, 'title':row[2], 'content':row[3]}
        print item
        item_foto = json.loads(str(row[4]))
        print item_foto
       
    if obj=='note':
        row = cursor.execute("SELECT * FROM notes WHERE id == ?", [id]).fetchone()
        item = {'content':row[1]}
        
    if obj=='doc':
        row = cursor.execute("SELECT * FROM docs WHERE id == ?", [id]).fetchone()
        item = {'title':row[1], 'path':row[2]}
    
    return item
