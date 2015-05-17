#!/usr/local/bin/python
  # -*- coding: utf-8 -*-
  # The above is needed to set the correct encoding, see https://www.python.org/dev/peps/pep-0263/

from werkzeug import secure_filename
from utils import datepick_to_datetime, allowed_file, set_to_string, get_extension
from config import ALLOWED_EXTENSIONS
import sqlite3, json, os, datetime
  

  
# *********** UPLOAD ***************************************************

def load_news(request, var, cursor, app):
	title = request.form['titolo']
	text = request.form['testo']
	date = request.form['data']
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
			
	paths = []
	for f in photo:
		if f:
			if not allowed_file(f.filename):
				var['msg'] = "Attenzione! Le foto non possono essere caricate.<br>Controlla le estensioni! Estensioni ammesse: {0}".format(set_to_string(ALLOWED_EXTENSIONS))
				return var
			filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(f.filename)))
			f.save(os.path.join(app.config['UPLOAD_FOLDER_PICS'], filename))
			paths.append(filename)
					
	cursor.execute("INSERT INTO news (data, title, text, pics) VALUES (?, ?, ?, ?)", [datepick_to_datetime(date), title, text, json.dumps(zip(paths, caps))])
	# Per decodificare, json.load(jsonyfied_var)
	var['upload_fail'] = 0
	var["upload_success"] = 'success'
	var['msg'] = "Upload completato con successo"
	return var
	
    
def load_note(request, var, cursor, app):
	text = request.form['testo']
	if not text:
		var['msg'] = "Impossibile caricare una nota vuota"
		return var
	cursor.execute("INSERT INTO notes VALUES (null, ?)", [text])
	var['upload_fail'] = 0
	var["upload_success"] = 'success'
	var['msg'] = "Upload completato con successo"
	return var


def load_doc(request, var, cursor, app):
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
    filename = 'File{0}.{1}'.format(str(datetime.datetime.now()).translate(None, '.:- ')[:-3], get_extension(secure_filename(f.filename)))
    f.save(os.path.join(app.config['UPLOAD_FOLDER_DOCS'], filename))
    cursor.execute("INSERT INTO docs (name, path) VALUES (?, ?)", [name, json.dumps(filename)])
    var["upload_fail"] = 0
    var["upload_success"] = 'success'
    var['msg'] = "Upload completato con successo"
    return var
    
    

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
            
    print lista 
    if lista == []:
        lista = [{'id':0, 'date':'', 'title':'Errore durante il caricamento della lista.<br>Riprova o contatta il webmaster.'}]
    return lista
    
