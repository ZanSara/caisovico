  #!/usr/local/bin/python
  # -*- coding: utf-8 -*-
  # The above is needed to set the correct encoding, see https://www.python.org/dev/peps/pep-0263/
  
  
  # ISSUES:
  # 1. Later on, should consider storing error messages in a log file...
  # 2. Maybe try to solve issues related to the upload of the pictures for the news.
  # 3. Maybe set the navbar to change from style to style, putting there the buttons from the related sidebox
  # 4. By now, I do not delete files in the uploads folder, I only overwrite their names in the database, making them orphans.
  
  
  # var: dictionary that contains all the template context variables
  # item: dictionary that contains all the object-related variables (titles, texts, etc...) Contained inside var.
  

from flask import Flask, request, session, abort, url_for, redirect, send_from_directory, flash
from jinja2 import Environment, PackageLoader
from config import UPLOAD_FOLDER_PICS, UPLOAD_FOLDER_DOCS, DATABASE_PATH
from utils import login, logout
from database import upload_news, load_news, update_news, upload_note, load_note, update_note, update_doc, upload_doc, load_doc, retrieve_item, retrieve_index, load_lista, delete_item
import sys, sqlite3, os     # sys if for errors handling, os is for file managing


env = Environment(loader=PackageLoader('core', '/templates'))

app = Flask(__name__, static_folder="static")
app.config['UPLOAD_FOLDER_DOCS'] = UPLOAD_FOLDER_DOCS
app.config['UPLOAD_FOLDER_PICS'] = UPLOAD_FOLDER_PICS

app.secret_key = ".ASF\x89m\x14\xc9s\x94ff\xfaq\xca}h\xe1/\x1f3\x1dFxj\xdc\xf0\xf9"



def style(style):
    """ 
        style(style):
    This is just an utility to make some modification regarding the
    styles of different sections of the website (css, boxes order)
    """
    if style=="home":
        var = {"menu": "base/menu-home.html"};
        var["url_for_css"] = "/static/css/style-home.css"
        
    elif style=="rifugio":
        var = {"menu": "base/menu-rif.html"};
        var["url_for_css"] = "/static/css/style-rifugio.css"
        
    elif style=="programmi":
        var = {"menu": "base/menu-prog.html"};
        var["url_for_css"] = "/static/css/style-programmi.css"
        
    elif style=="sezione":
        var = {"menu": "base/menu-sez.html"};
        var["url_for_css"] = "/static/css/style-sezione.css"
        
    elif style=="webmaster":
        var = {"menu": "base/menu-web.html"};
        var["url_for_css"] = "/static/css/style-webmaster.css"

    return var;
    

# ********* Navbar links ***********************************************
@app.route("/" , methods=["GET"])
def home():
    var = style("home")
    template = env.get_template("home.html")
    return template.render(var)

@app.route("/archivio" , methods=["GET"])
def archivio():
    var = style("home")
    template = env.get_template("archivio.html")
    return template.render(var)

@app.route("/galleria" , methods=["GET"])
def galleria():
    var = style("home")
    template = env.get_template("galleria.html")
    return template.render(var)


# ********** Rifugio links *********************************************
    
@app.route("/rifugio/" , methods=["GET"])
def rif1():
    var = style("rifugio")
    template = env.get_template("rif-home.html")
    return template.render(var)

@app.route("/rifugio/mappe" , methods=["GET"])
def rifmappe():
    var = style("rifugio")
    template = env.get_template("rif-mappe.html")
    return template.render(var)

@app.route("/rifugio/bivacco" , methods=["GET"])
def rifbivacco():
    var = style("rifugio")
    template = env.get_template("rif-bivacco.html")
    return template.render(var)

@app.route("/rifugio/ampliamenti" , methods=["GET"])
def rifamplia():
    var = style("rifugio")
    template = env.get_template("rif-ampliamenti.html")
    return template.render(var)

@app.route("/rifugio/storia" , methods=["GET"])
def rifstoria():
    var = style("rifugio")
    template = env.get_template("rif-storia.html")
    return template.render(var)

# ********** Programmi links *******************************************

@app.route("/programmi" , methods=["GET"])
def proghome():
    var = style("programmi")
    template = env.get_template("prog-home.html")
    return template.render(var)
    
@app.route("/programmi/norme" , methods=["GET"])
def prognorme():
    var = style("programmi")
    template = env.get_template("prog-norme.html")
    return template.render(var)


# ********** Sezione links *******************************************

@app.route("/sezione" , methods=["GET"])
def sezhome():
    var = style("sezione")
    template = env.get_template("sez-home.html")
    return template.render(var)
    
@app.route("/sezione/contatti" , methods=["GET"])
def sezcontatti():
    var = style("sezione")
    template = env.get_template("sez-contatti.html")
    return template.render(var)

@app.route("/sezione/quote" , methods=["GET"])
def sezquote():
    var = style("sezione")
    template = env.get_template("sez-quote.html")
    return template.render(var)

@app.route("/sezione/storia" , methods=["GET"])
def sezstoria():
    var = style("sezione")
    template = env.get_template("sez-storia.html")
    return template.render(var)


# ********** Webmaster links *******************************************

@app.route("/pannello" , methods=["GET"])
def webhome():
    var = style("webmaster")
    template = env.get_template("web-home.html")
    return template.render(var)
    
@app.route("/pannello/feedback" , methods=["GET"])
def webfed():
    var = style("webmaster")
    template = env.get_template("web-feedback.html")
    return template.render(var)

@app.route("/pannello/webmaster" , methods=["GET"])
def webmaster():
    var = style("webmaster")
    template = env.get_template("web-master.html")
    return template.render(var)


@app.route("/pannello/area-riservata", methods=["GET", "POST"])
def webres():
    if not session.get('logged_in'):
        return redirect(url_for('weblogin'))
    var = style("webmaster")
    template = env.get_template("web-res-home.html")
    return template.render(var)


# ************ RESERVED AREA *******************************************

#************* Misc ****************************************************
    
@app.route('/uploads/<folder>/<filename>')
def static_file(folder, filename):
    """ Serves static files """
    if folder=='photos':
        return send_from_directory(app.config['UPLOAD_FOLDER_PICS'], filename)
    return send_from_directory(app.config['UPLOAD_FOLDER_DOCS'], filename)


@app.route("/pannello/area-riservata/login", methods=["GET", "POST"])
def weblogin():
    """ Performs the login """
    var = style("webmaster")
                
    if request.method == "POST":
        try:
            login(request.form["user"], request.form["password"])
        except (IndexError, ValueError) as e:
            var['msg'] = e
            template = env.get_template("web-res-login.html")
            return template.render(var)
        return redirect(url_for('webres'))

    template = env.get_template("web-res-login.html")
    return template.render(var)
    

@app.route("/pannello/area-riservata/logout", methods=["GET", "POST"])
def weblogout():
    """ Performs the logout """
    if not session.get('logged_in'):
        return redirect(url_for('weblogin'))
        
    var = style("webmaster")

    try:
        logout()
    except Exception as e:
        var['msg'] = e
        template = env.get_template("web-res-login.html")
        return template.render(var)
        # ISSUE!
        # If I logout, the logout fails, and I immediately try to login 
        # again, I find myself asking this function to handle my login. 
        # Should FULLY redirect to the welogin() function, not only render it.
    return redirect(url_for('weblogin'))


# ************* Upload *************************************************

@app.route("/pannello/area-riservata/upload/<obj>", methods=["GET", "POST"])
def webupload(obj):
    ''' 
        webupload(obj):
    Uploads an object (news, note, doc): writes everything in the 
    database and upload any file needed.
    '''
    if not session.get('logged_in'):
        return redirect(url_for('weblogin'))
    
    var = style("webmaster")
    var['obj'] = obj
    var['item'] = {}
    template = env.get_template("web-res-upload2.html")

    if request.method == 'POST':
        conn = sqlite3.connect(DATABASE_PATH)
        try:
            with conn:
                cursor = conn.cursor()
                if obj=="news":
                    upload_news(request, cursor, app)
                elif obj=='note':
                    upload_note(request, cursor)
                elif obj=='doc':
                    upload_doc(request, cursor, app)
                else:
                    raise ValueError(u'Unknown OBJ value')
            conn.commit()
            var["upload"] = 'success'
            var['msg'] = u'Upload completato con successo'
            conn.close()
        except ValueError as e:
            if obj=="news":
                load_news(request)
            elif obj=='note':
                load_note(request)
            elif obj=='doc':
                load_doc(request)
            var["upload"] = 'fail'
            var['msg'] = e
    
    return template.render(var)


# ************ Manage **************************************************

@app.route("/pannello/area-riservata/manage/<obj>", methods=["GET"])
def webmanage(obj):
    '''
        webmanage(obj):
    Renders a list of all the available object present in the database, 
    and allows the user to select the one he wants to modify.
    '''
    if session.get('logged_in')==None:
        return redirect(url_for('weblogin'))
        
    var = style("webmaster")
    var['obj'] = obj
    var['manage'] = 'manage'
    template = env.get_template("web-res-manage-main.html")
    
    conn = sqlite3.connect(DATABASE_PATH)
    with conn:
        try:
            cursor = conn.cursor()
            var['lista'] = load_lista(obj, cursor)
        except Exception as e:
            var['msg'] = e
    conn.close()
    
    if var['lista'] == []:
        var['msg'] = 'Nessun elemento trovato'
    
    return template.render(var)
    
    
@app.route("/pannello/area-riservata/manage/<obj>/<int:id>", methods=["GET", "POST"])
def webmodify(obj, id):
    '''
        webmodify(obj, id):
    Allows the user to modify the details of an object.
    '''
    if not session.get('logged_in'):
        return redirect(url_for('weblogin'))

    var = style("webmaster")
    var['obj'] = obj
    var['item'] = {}
    template = env.get_template("web-res-upload2.html")
    
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        
        if request.method=='POST':
            conn = sqlite3.connect(DATABASE_PATH)
            with conn:
                cursor = conn.cursor()
                if obj=="news":
                    update_news(request, cursor, app, id)
                elif obj=='note':
                    update_note(request, cursor, id)
                elif obj=='doc':
                    update_doc(request, cursor, app, id)
                conn.commit()
                var['item'] = retrieve_item(obj, id, cursor)    # Ensures that the data has actually been written
                var['msg'] = 'Upload completato con successo'
                var['upload'] = 'success'
        else:
            with conn:
                cursor = conn.cursor()
                var['item'] = retrieve_item(obj, id, cursor)

    except (ValueError) as e:
        var['msg'] = e
        var['upload'] = 'fail'
        var['item'] = retrieve_item(obj, id, cursor)
        
    conn.close()
    
    return template.render(var)



@app.route("/pannello/area-riservata/manage/news/<int:id>/pics/<index>", methods=["GET", "POST"])
def weupdatepics(id, index):
    '''
        weupdatepics(id, index):
    Allows the user to modify the details of an object.
    '''
    if not session.get('logged_in'):
        return redirect(url_for('weblogin'))
    
    var = style("webmaster")
    var['obj'] = 'news'
    var['id'] = id
    template = env.get_template("web-res-manage-photos.html")
    
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        with conn:
            cursor = conn.cursor()
            
            if index=="add":
                var['new'] = True
                var['index'] = retrieve_index(id, cursor)
            else:
                var['new'] = False
                var['index'] = int(index)
                var['item'] = retrieve_newspics(id, var['index'], cursor)
                
            if request.method=="POST":
                update_newspics(request, cursor, app, id, var['index'])
                conn.commit()
                var['item'] = retrieve_newspics(id, var['index'], cursor)
                if not var['item']:
                    raise ValueError (u"Errore durante il caricamento della foto")
                    return template.render(var)
                var['msg'] = 'Upload completato con successo'
                var['upload'] = 'success'


        conn.close()
    except (ValueError, KeyError, IndexError) as e:
        var['msg'] = e
        var['upload'] = 'fail'
        
    return template.render(var)
    
    
# *********** Delete ***************************************************
    
@app.route("/pannello/area-riservata/delete/<obj>", methods=["GET"])
def webdeletelist(obj):
    '''
        webdeletelist(obj):
    Renders a list of all the objects available in the database, 
    and allows the user to select the one he wants to delete.
    '''
    if not session.get('logged_in'):
        return redirect(url_for('weblogin'))
        
    var = style("webmaster")
    var['obj'] = obj
    var['manage'] = 'delete'
    template = env.get_template("web-res-manage-main.html")
    
    conn = sqlite3.connect(DATABASE_PATH)
    with conn:
        try:
            cursor = conn.cursor()
            var['lista'] = load_lista(obj, cursor)
        except Exception as e:
            var['msg'] = e
    conn.close()
    
    if var['lista'] == []:
        var['msg'] = 'Nessun elemento trovato'
    
    return template.render(var)
    
    
@app.route("/pannello/area-riservata/delete/<obj>/<int:id>", methods=["GET", "POST"])
def webdeleteid(obj, id):
    '''
        webdeleteid(obj):
    Renders the object selected and ask confirmation to delete the object.
    Then deletes it.
    '''
    if not session.get('logged_in'):
        return redirect(url_for('weblogin'))
        
    var = style("webmaster")
    var['obj'] = obj
    var['manage'] = 'delete'
    template = env.get_template("web-res-delete.html")
    
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        with conn:
            cursor = conn.cursor()
            if request.method=='POST':
                delete_item(obj, cursor, app, id)
                var['deleted'] = True
            else:
                cursor = conn.cursor()
                var['item'] = retrieve_item(obj, id, cursor)
            
    except ValueError as e:
            var['upload'] = 'fail'
            var['msg'] = e
            var['item'] = retrieve_item(obj, id, cursor)
    
    conn.close()
    
    
    
    return template.render(var)
    
    
@app.route("/pannello/area-riservata/delete/<obj>/<int:id>/<index>", methods=["GET"])
def webdeletepic(obj, id, index):
    '''
        webdeletepic(obj):
    Renders the object selected and ask confirmation to delete the picture.
    Then deletes it.
    '''
    if not session.get('logged_in'):
        return redirect(url_for('weblogin'))
        
    var = style("webmaster")
    var['obj'] = obj
    var['manage'] = 'delete'
    template = env.get_template("web-res-delete-pic.html")
    
    conn = sqlite3.connect(DATABASE_PATH)
    with conn:
        if request.method == 'POST':
            pass
        else:
            try:
                cursor = conn.cursor()
                var['item'] = retrieve_item(obj, id, cursor)
            except ValueError as e:
                var['upload'] = 'fail'
                var['msg'] = e
            
    conn.close()
    
    return template.render(var)

    
    
    
    
    
    
    
#*** ERROR HANDLERS ****************

#@app.errorhandler(404)
#def page_not_found(e):
    #return render_template('404.html'), 404
#@app.errorhandler(401)
#def unauthorized(e):
    #return render_template('401.html'), 401
#@app.errorhandler(500)
#def internal_error(e):
    #return render_template('500.html'), 500





if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
