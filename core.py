  #!/usr/local/bin/python
  # -*- coding: utf-8 -*-
  # The above is needed to set the correct encoding, see https://www.python.org/dev/peps/pep-0263/
  
  
  # ISSUES:
  # 1. Later on, should consider storing error messages in a log file...
  

from flask import Flask, request, session, abort, url_for, redirect, send_from_directory
from jinja2 import Environment, PackageLoader
from config import UPLOAD_FOLDER_PICS, UPLOAD_FOLDER_DOCS, ALLOWED_EXTENSIONS, DATABASE_PATH
from utils import login, logout
from database import upload_news, upload_note, upload_doc, load_lista, retrieve_item, update_news, update_newspics, update_note, retrieve_photo
import sys, sqlite3, os     # sys if for errors handling, os is for file managing


env = Environment(loader=PackageLoader('core', '/templates'))

app = Flask(__name__, static_folder="static")
app.config['UPLOAD_FOLDER_DOCS'] = UPLOAD_FOLDER_DOCS
app.config['UPLOAD_FOLDER_PICS'] = UPLOAD_FOLDER_PICS

app.secret_key = ".ASF\x89m\x14\xc9s\x94ff\xfaq\xca}h\xe1/\x1f3\x1dFxj\xdc\xf0\xf9"



def style(style):
    """ style() is just an utility to make some modification regarding the
        styles of different sections of the website (css, boxes order)"""
    if style=="home":
        var = {"sidebar":["base/boxrif.html", "base/boxprog.html", "base/boxsez.html", "base/boxweb.html"]};
        var["url_for_css"] = "/static/css/style-home.css"
        
    elif style=="rifugio":
        var = {"sidebar":["base/boxrif.html", "base/boxprog.html", "base/boxsez.html", "base/boxweb.html"]};
        var["url_for_css"] = "/static/css/style-rifugio.css"
        
    elif style=="programmi":
        var = {"sidebar":["base/boxrif.html", "base/boxprog.html", "base/boxsez.html", "base/boxweb.html"]};
        #var = {"sidebar":["base/boxprog.html", "base/boxrif.html", "base/boxsez.html", "base/boxweb.html"]};
        var["url_for_css"] = "/static/css/style-programmi.css"
        
    elif style=="sezione":
        var = {"sidebar":["base/boxrif.html", "base/boxprog.html", "base/boxsez.html", "base/boxweb.html"]};
        #var = {"sidebar":["base/boxsez.html", "base/boxrif.html", "base/boxprog.html", "base/boxweb.html"]};
        var["url_for_css"] = "/static/css/style-sezione.css"
        
    elif style=="webmaster":
        var = {"sidebar":["base/boxrif.html", "base/boxprog.html", "base/boxsez.html", "base/boxweb.html"]};
        #var = {"sidebar":["base/boxweb.html", "base/boxrif.html", "base/boxprog.html", "base/boxsez.html"]};
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



# ************ Reserved Area *******************************************
    
@app.route('/uploads/<folder>/<filename>')
def static_file(folder, filename):
    """ Serves static files """
    if folder=='photos':
        return send_from_directory(app.config['UPLOAD_FOLDER_PICS'], filename)
    return send_from_directory(app.config['UPLOAD_FOLDER_DOCS'], filename)


@app.route("/pannello/area-riservata/login", methods=["GET", "POST"])
def weblogin():
    var = style("webmaster")
                
    if request.method == "POST":
        try:
            login(request.form["user"], request.form["password"])
        except (IndexError, ValueError) as e:
            var['msg'] = 'ERRORE: {0}'.format(e)
            template = env.get_template("web-res-login.html")
            return template.render(var)
        return redirect(url_for('webres'))

    template = env.get_template("web-res-login.html")
    return template.render(var)
    

@app.route("/pannello/area-riservata/logout", methods=["GET", "POST"])
def weblogout():
    if not session.get('logged_in'):
        return redirect(url_for('weblogin'))
    var = style("webmaster")
    try:
        logout()
    except Exception as e:
        var['msg'] = 'ERRORE: {0}'.format(e)
        template = env.get_template("web-res-login.html")
        return template.render(var)
        # ISSUE!
        # If I logout, the logout fails, and I immediately try to login 
        # again, I find myself asking this function to handle my login. 
        # Should FULLY redirect to the welogin() function, not only render it.
    return redirect(url_for('weblogin'))


@app.route("/pannello/area-riservata", methods=["GET", "POST"])
def webres():
    if not session.get('logged_in'):
        return redirect(url_for('weblogin'))

    var = style("webmaster")
    template = env.get_template("web-res-home.html")
    return template.render(var)
    


@app.route("/pannello/area-riservata/upload/<obj>", methods=["GET", "POST"])
def webupload(obj):
    if not session.get('logged_in'):
        redirect(url_for('weblogin'))

    var = style("webmaster")
    var['obj'] = obj
    template = env.get_template("web-res-upload.html")
    item = {}

    if request.method == 'POST':
        conn = sqlite3.connect(DATABASE_PATH)
        try:
            print "try:"
            with conn:
                cursor = conn.cursor()
                if obj=="news":
                    item = upload_news(request, cursor, app)
                elif obj=='note':
                    item = upload_note(request, cursor)
                elif obj=='doc':
                    item = upload_doc(request, cursor, app)
            conn.commit()
            var["upload"] = 'success'
            var['msg'] = u'Upload completato con successo'
            var['item'] = {}    # To avoid the user believing he is modifying the newly-updated data, while he's writing a new one.
            conn.close()
        except ValueError as e:
            print 'CORE #1 ', item
            var['item'] = item
            var["upload"] = 'fail'
            var['msg'] = e
        except:
            var['msg'] = 'Errore inaspettato :/'
    
    var['item'] = item
    print 'CORE #2', item
    return template.render(var)
    
    
@app.route("/pannello/area-riservata/manage/<obj>", methods=["GET"])
def webmanage(obj):
    if not session.get('logged_in'):
        redirect(url_for('weblogin'))
        
    var = style("webmaster")
    var['obj'] = obj
    var['item'] = {}
    template = env.get_template("web-res-manage-main.html")
    
    conn = sqlite3.connect(DATABASE_PATH)
    with conn:
        cursor = conn.cursor()
        var['lista'] = load_lista(obj, cursor)
    conn.close()

    return template.render(var)
    
    
@app.route("/pannello/area-riservata/manage/<obj>/<id>", methods=["GET", "POST"])
def webmodify(obj, id):
    if not session.get('logged_in'):
        redirect(url_for('weblogin'))

    var = style("webmaster")
    var['obj'] = obj
    template = env.get_template("web-res-upload.html")
    
    conn = sqlite3.connect(DATABASE_PATH)
    with conn:
        cursor = conn.cursor()
        var['item'] = retrieve_item(obj, id, cursor)
    conn.close()
        
    if request.method=='POST':
        var["upload"] = 'fail'
        var['msg'] = u"Upload non riuscito. Riprova o contatta il webmaster."
        conn = sqlite3.connect(DATABASE_PATH)
        with conn:
            cursor = conn.cursor()
            if obj=="news":
                var = update_news(request, var, cursor, app, id)
            elif obj=='note':
                var = update_note(request, var, cursor, id)
            elif obj=='doc':
                var = update_doc(request, var, cursor, app, id)
        conn.commit()
        var['item'] = retrieve_item(obj, id, cursor)    # Ensures that the data has actually been written
        conn.close()
        

    return template.render(var)
    

@app.route("/pannello/area-riservata/manage/news/<id>/pics/<index>", methods=["GET", "POST"])
def weupdatepics(id, index):
    if not session.get('logged_in'):
        redirect(url_for('weblogin'))
    var = style("webmaster")
    
    var['obj'] = 'news'
    var['id'] = id
    var['item'] = {}
    template = env.get_template("web-res-manage-photos.html")
    
    if index=="add":
        var['new'] = True
        # var['index'] is left undefined
    else:
        var['new'] = False
        index = int(index)
        var['index'] = index
    
    conn = sqlite3.connect(DATABASE_PATH)
    with conn:
        cursor = conn.cursor()
        if request.method=="POST":
            var = update_newspics(request, var, cursor, app, id)
            conn.commit()
        
        if var['new'] == False:    
            photo = retrieve_photo(id, var['index'], cursor)
            if not photo:
                var['upload'] = 'fail'
                var['msg'] = u"Errore durante il caricamento della foto."
                return template.render(var)
            var['item'] = photo

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
