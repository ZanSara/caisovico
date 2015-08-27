    #!/usr/local/bin/python
  # -*- coding: utf-8 -*-
  # The above is needed to set the correct encoding, see https://www.python.org/dev/peps/pep-0263/
    
  
  # MAIN ISSUES:
  # 1. Later on, should consider storing error messages in a log file... DONE
  # 2. Should rethink the database structure concerning pictures' storage: 
  #    there should be a 'pics' table linked with a relationship "many to one" with 'news'
  # 3. Why I may add only one picture a time, when modifying a news?
  # 4. Interface issue: should check if the javascript has been loaded, and open all the sideboxes by default.
  # Secondary issues somewhere in the code
  
  # var: dictionary that contains all the template context variables
  # item: dictionary that contains all the object-related variables (titles, texts, etc...). Contained inside var.


try:
    from config import app, env, UPLOAD_FOLDER_PICS, UPLOAD_FOLDER_DOCS, DATABASE_PATH
    from flask import request, abort
    from jinja2 import evalcontextfilter, Markup, escape
    from database import upload_news, load_news, update_news, upload_note, load_note, update_note, update_doc, upload_doc, load_doc, retrieve_item, retrieve_index, load_lista, delete_item, delete_pic, load_page, get_totpage
    
    from database import find_postit, last_leaflet, last_doc, find_rec
    import sys, sqlite3, os, re     # sys for errors handling, os for file managing
except Exception as e:
    app.logger.critical('CORE IMPORTING ERROR: {0}'.format(e) )
    print 'CORE IMPORTING ERROR: {0}'.format(e)
    raise




# ********* Home & News ************************************************

def home(var):
    conn = sqlite3.connect(DATABASE_PATH)
    with conn:
        cursor = conn.cursor()
        var['postit'] = find_postit()
        var['leaflet'] = last_leaflet()    #load_page('news', cursor, 5, 0)
        var['doc'] = last_doc()
        # Both leaflet and doc may be None. Then look for a filler.
        if var['leaflet']==None:
            var['recleft'] = find_rec(0)
        if var['doc']==None:
            if var['leaflet']==None:
                var['recright'] = find_rec(1)
            else:
                var['recright'] = find_rec(0)
    return var
    
def homepages(var, index):
    conn = sqlite3.connect(DATABASE_PATH)
    with conn:
        cursor = conn.cursor()
        var['newslist'] = load_page('news', cursor, 5, index-1)
        var['noteslist'] = load_page('note', cursor, 5, index-1)
        var['curpage'] = index
        var['totpage'] = get_totpage(5, cursor)
    return var
    
def fullnews(var, id):
    conn = sqlite3.connect(DATABASE_PATH)
    with conn:
        cursor = conn.cursor()
        var['item'] = retrieve_item('news', id, cursor)
    return var
    # Issue!
    # From this page, when I press the Back button I am redirect on the
    # homepage, not the n-th page where I actually found the news.



# ************ RESERVED AREA *******************************************
    
# ************* Upload *************************************************

def upload(var, request):
    ''' 
        upload(var, obj, request):
    Uploads an object (news, note, doc): writes everything in the 
    database and upload any file needed.
    '''
    if request.method == 'POST':
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            with conn:
                cursor = conn.cursor()
                if var['obj']=="news":
                    upload_news(request, cursor, app)
                elif var['obj']=='note':
                    upload_note(request, cursor)
                elif var['obj']=='doc':
                    upload_doc(request, cursor, app)
                else:
                    raise ValueError(u'Unknown OBJ value')
            conn.commit()
            var["upload"] = 'success'
            var['msg'] = u'Upload completato con successo'
            app.logger.info('Upload completed successfully')
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            app.logger.error('SQLite failure during upload. Error code:{e}'.format(e) )
            raise
        except ValueError as e:
            if var['obj']=="news":
                load_news(request)
            elif var['obj']=='note':
                load_note(request)
            elif var['obj']=='doc':
                load_doc(request)
            var["upload"] = 'fail'
            var['msg'] = e
            app.logger.info('Upload failed due to ValueError. Error Code: {0}'.format(e) )
        except Exception as e:
            app.logger.error('Unexpected Exception in UPLOAD. Error Code: {0}'.format(e) )
            raise          
    return var
    
# ************ Manage **************************************************

def manage(var):
    '''
        manage(var):
    Renders a list of all the available object present in the database, 
    and allows the user to select the one he wants to modify.
    '''
    conn = sqlite3.connect(DATABASE_PATH)
    with conn:
        try:
            cursor = conn.cursor()
            var['lista'] = load_lista(var['obj'], cursor)
        except Exception as e:
            var['msg'] = e
            app.logger.error('Unexpected error in MANAGE. Error Code: {0}'.format(e) )
            raise
    conn.close()
    if var['lista'] == []:
        var['msg'] = 'Nessun elemento trovato'
        app.logger.warning('Table {0} is or seems empty'.format(var['obj']) )
    return var
    
def modify(var, request):
    '''
        modify(var, request):
    Allows the user to modify the details of an object.
    '''
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        if request.method=='POST':
            conn = sqlite3.connect(DATABASE_PATH)
            with conn:
                cursor = conn.cursor()
                if var['obj']=="news":
                    update_news(request, cursor, app, var['id'])
                elif var['obj']=='note':
                    update_note(request, cursor, var['id'])
                elif var['obj']=='doc':
                    update_doc(request, cursor, app, var['id'])
                conn.commit()
                var['item'] = retrieve_item(var['obj'], var['id'], cursor)    # Ensures that the data has actually been written
                var['msg'] = 'Upload completato con successo'
                var['upload'] = 'success'
        else:
            with conn:
                cursor = conn.cursor()
                var['item'] = retrieve_item(var['obj'], var['id'], cursor)
    except ValueError as e:
        var['msg'] = e
        var['upload'] = 'fail'
        var['item'] = retrieve_item(var['obj'], var['id'], cursor)
        app.logger.info('Modification failed due to Value Error. Erro Code: {0}'.format(e) )
    except sqlite3.Error as e:
            if conn:
                conn.rollback()
            app.logger.error('SQLite failure during modification. Error code:{e}'.format(e) )
            raise
    except Exception as e:
        var['msg'] = e
        app.logger.error('Unexpected error in MODIFY. Error Code: {0}'.format(e) )
        raise
    return var
    
 
# *********** Delete ***************************************************
 
def delete(var):
    '''
        delete(var):
    Renders the object selected and ask confirmation to delete the object.
    Then deletes it.
    '''   
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        with conn:
            cursor = conn.cursor()
            if request.method=='POST':
                delete_item(var['obj'], cursor, app, var['id'])
                var['deleted'] = True
            else:
                cursor = conn.cursor()
                var['item'] = retrieve_item(var['obj'], var['id'], cursor)
    except ValueError as e:
            var['upload'] = 'fail'
            var['msg'] = e
            var['item'] = retrieve_item(var['obj'], var['id'], cursor)
            app.logger.info('Deletion failed due to Value Error. Erro Code: {0}'.format(e) )
    except sqlite3.Error as e:
            if conn:
                conn.rollback()
            app.logger.error('SQLite failure during deletion of a full object. Error code:{e}'.format(e) )
            raise
    except Exception as e:
        var['msg'] = e
        app.logger.error('Unexpected error in DELETE. Error Code: {0}'.format(e) )
        raise
    return var
    
def deletepic(var):
    '''
        deletepic(var):
    Renders the picture selected and ask confirmation.
    Then deletes it.
    '''  
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        with conn:
            cursor = conn.cursor()
            if request.method=='POST':
                delete_pic(cursor, app, var['id'], var['index'])
                var['deleted'] = True
            else:
                cursor = conn.cursor()
                var['item'] = retrieve_item('news', var['id'], cursor)['pics'][var['index']]
    except ValueError as e:
            var['upload'] = 'fail'
            var['msg'] = e
            var['item'] = retrieve_item('news', var['id'], cursor)['pics'][var['index']]
            app.logger.info('Deletion failed due to Value Error. Erro Code: {0}'.format(e) )
    except Exception as e:
        var['msg'] = e
        app.logger.error('Unexpected error in DELETEPIC. Error Code: {0}'.format(e) )
        raise
    return var
    

# ************** Misc **************************************************

# Multiline rendering

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' %  p.replace('\n', Markup('<br>\n'))  # One new <p></p> for each paragraph.
    #result = u'\n\n'.join(u'<br>%s' % p.replace('\n', Markup('<br>\n'))     # One <br> for each newline
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

env.filters['nl2br'] = nl2br


def style(style):
    """ 
        style(style):
    This is just an utility to make some modification regarding the
    styles of different sections of the website (css, open boxes, menu)
    """
    if style=="home":
        var = {"menu": "base/menu-home.html"};
        var["url_for_css"] = "/static/css/style-home.css"
        var["openbox"] = "rifugio"
        
    elif style=="rifugio":
        var = {"menu": "base/menu-rif.html"};
        var["url_for_css"] = "/static/css/style-rifugio.css"
        var["openbox"] = "rifugio"
        
    elif style=="programmi":
        var = {"menu": "base/menu-prog.html"};
        var["url_for_css"] = "/static/css/style-programmi.css"
        var["openbox"] = "programmi"
        
    elif style=="sezione":
        var = {"menu": "base/menu-sez.html"};
        var["url_for_css"] = "/static/css/style-sezione.css"
        var["openbox"] = "sezione"
        
    elif style=="webmaster":
        var = {"menu": "base/menu-web.html"};
        var["url_for_css"] = "/static/css/style-webmaster.css"
        var["openbox"] = "pannello"

    return var
