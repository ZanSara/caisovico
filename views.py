  #!/usr/local/bin/python
  # -*- coding: utf-8 -*-
  # The above is needed to set the correct encoding, see https://www.python.org/dev/peps/pep-0263/
  
#try:
import logging
from flask import request, session, abort, url_for, redirect, send_from_directory, render_template
from utils import login, logout
from config import env, app
from core import nl2br, style, home, homepages, fullnews, upload, manage, modify, delete, deletepic
#except Exception as e:
    #print 'VIEWS IMPORTING ERROR: {}'.format(e)
    #logging.critical('VIEWS IMPORTING ERROR')



# ********* Home & News links ******************************************

@app.route("/" , methods=["GET"])
def viewhome():
    var = style("home")
    var = home(var)
    template = env.get_template("home.html")
    return template.render(var)
    
@app.route("/<int:index>" , methods=["GET"])
def viewhomepages(index):
    var = style("home")
    var = homepages(var, index)
    if index > var['totpage']:
        app.logger.warning('404: tried to access home-page n^{}'.format(index))
        return abort(404)
    template = env.get_template("home.html")
    return template.render(var)
    
@app.route("/news/<id>" , methods=["GET"])
def viewfullnews(id):
    var = style("home")
    var = fullnews(var, id)
    template = env.get_template("home-fullnews.html")
    return template.render(var) 
    

# ********** Rifugio links *********************************************
    
@app.route("/rifugio/" , methods=["GET"])
def rifhome():
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

#************* Utils ***************************************************
    
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
            var['msg'] = e
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
        var['msg'] = e
        template = env.get_template("web-res-login.html")
        return template.render(var)
    return redirect(url_for('weblogin'))
    # ISSUE!
    # If I logout, the logout fails, and I immediately try to login 
    # again, I find myself asking this function to handle my login. 
    # Should FULLY redirect to the welogin() function, not only render it.
        

# ************* Upload *************************************************

@app.route("/pannello/area-riservata/upload/<obj>", methods=["GET", "POST"])
def viewupload(obj):
    if not session.get('logged_in'):
        return redirect(url_for('weblogin'))
    var = style("webmaster")
    var['obj'] = obj
    var['item'] = {}
    var = upload(var, request)
    template = env.get_template("web-res-upload.html")
    return template.render(var)


# ************ Manage **************************************************

@app.route("/pannello/area-riservata/manage/<obj>", methods=["GET"])
def viewmanage(obj):
    if session.get('logged_in')==None:
        return redirect(url_for('weblogin'))
    var = style("webmaster")
    var['obj'] = obj
    var['manage'] = 'manage'
    var = manage(var)
    template = env.get_template("web-res-manage-main.html")    
    return template.render(var)
    
    
@app.route("/pannello/area-riservata/manage/<obj>/<int:id>", methods=["GET", "POST"])
def viewmodify(obj, id):
    if not session.get('logged_in'):
        return redirect(url_for('weblogin'))
    var = style("webmaster")
    var['obj'] = obj
    var['id'] = id
    var['item'] = {}
    var = modify(var, request)
    template = env.get_template("web-res-upload.html")
    return template.render(var)

    
# *********** Delete ***************************************************
    
@app.route("/pannello/area-riservata/delete/<obj>/<int:id>", methods=["GET", "POST"])
def viewdelete(obj, id):
    if not session.get('logged_in'):
        return redirect(url_for('weblogin'))
    var = style("webmaster")
    var['obj'] = obj
    var['id'] = id
    var['manage'] = 'delete'
    var = delete(var)
    template = env.get_template("web-res-delete.html")
    return template.render(var)
    

@app.route("/pannello/area-riservata/delete/news/<int:id>/<int:index>", methods=["GET", "POST"])
def viewdeletepic(id, index):
    if not session.get('logged_in'):
        return redirect(url_for('weblogin'))
    var = style("webmaster")
    var['obj'] = 'pic'
    var['id'] = id
    var['index'] = index
    var['manage'] = 'delete'
    var = deletepic(var)
    template = env.get_template("web-res-delete.html")
    return template.render(var)
    

    
# *********** Error Handlers *******************************************

@app.errorhandler(404)
def page_not_found(e):
    var = style("home")
    template = env.get_template("404.html")
    return template.render(var), 404
    
@app.errorhandler(401)
def unauthorized(e):
    var = style("home")
    template = env.get_template("401.html")
    return template.render(var), 401
    
@app.errorhandler(500)
def internal_error(e):
    var = style("home")
    var['msg'] = e
    template = env.get_template("500.html")
    return template.render(var), 500


