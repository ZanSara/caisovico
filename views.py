  #!/usr/local/bin/python
  # -*- coding: utf-8 -*-
  # The above is needed to set the correct encoding, see https://www.python.org/dev/peps/pep-0263/
  
try:
    from config import app, env
    from flask import request, session, abort, url_for, redirect, send_from_directory, render_template
    from decorators import login_required
    from utils import login, logout
    from core import nl2br, style, find_postit, managepostit, eventi, prossimagita, fullnews, upload, manage, modify, delete, deletepic
except Exception as e:
    print 'VIEWS IMPORTING ERROR: {0}'.format(e)
    app.logger.error('VIEWS IMPORTING ERROR: {0}'.format(e) )
    raise




# ********* Home & News links ******************************************

@app.route("/" , methods=["GET"])
def viewhome():
    var = style("home")
    template = env.get_template("homepage.html")
    #try:
    #var = find_postit(var)
    #except Exception as e:
        # "Safety Homepage". 
        # It's so ugly to get a 500 right in the homepage if something is wrong with the database.
        #template = env.get_template("home-safety.html")
        #app.logger.critical('*** HOMEPAGE FAILED TO LOAD *** (Error: {0})'.format(e))
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

@app.route("/programmi/prossima-gita" , methods=["GET"])
def prognuovagita():
    var = style("programmi")
    #var = prossimagita()
    template = env.get_template("prog-nuovagita.html")
    return template.render(var)
    
@app.route("/programmi/eventi/<year>" , methods=["GET"])
def progeventi(year):
    var = style("programmi")
    #var = eventi(year)
    template = env.get_template("prog-eventi.html")
    return template.render(var)

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
    
@app.route("/sezione/documenti" , methods=["GET"])
def sezavvisi():
    var = style("sezione")
    template = env.get_template("sez-documenti.html")
    return template.render(var)

@app.route("/sezione/storia" , methods=["GET"])
def sezstoria():
    var = style("sezione")
    template = env.get_template("sez-storia.html")
    return template.render(var)

@app.route("/sezione/quote" , methods=["GET"])
def sezquote():
    var = style("sezione")
    template = env.get_template("sez-quote.html")
    return template.render(var)

@app.route("/sezione/assicurazioni" , methods=["GET"])
def sezassic():
    var = style("sezione")
    template = env.get_template("sez-assic.html")
    return template.render(var)

@app.route("/sezione/contatti" , methods=["GET"])
def sezcontatti():
    var = style("sezione")
    template = env.get_template("sez-contatti.html")
    return template.render(var)

# ********** Webmaster links *******************************************

@app.route("/pannello/feedback" , methods=["GET"])
def webfeedback():
    var = style("webmaster")
    template = env.get_template("web-feedback.html")
    return template.render(var)

@app.route("/pannello/webmaster" , methods=["GET"])
def webmaster():
    var = style("webmaster")
    template = env.get_template("web-master.html")
    return template.render(var)


@app.route("/pannello/area-riservata", methods=["GET", "POST"])
@login_required
def webreserved():
    var = style("webmaster")
    template = env.get_template("web-res-home.html")
    return template.render(var)


# ************ RESERVED AREA *******************************************

#************* Utils ***************************************************
    
@app.route('/uploads/<folder>/<filename>')
def static_file(folder, filename):
    """ Serves static files """
    try:
        if folder=='photos':
            return send_from_directory(app.config['UPLOAD_FOLDER_PICS'], filename)
        elif folder=='thumb':
            return send_from_directory(app.config['UPLOAD_FOLDER_THUMB'], filename)
        return send_from_directory(app.config['UPLOAD_FOLDER_DOCS'], filename)
    except Exception as e:
        app.logger.error("An exception occurred trying to send '{0}' from '{1}'. Does the file exist?".format(filename, folder))
    return abort(404)


@app.route("/pannello/area-riservata/login", methods=["GET", "POST"])
def viewlogin():
    var = style("webmaster")
                
    if request.method == "POST":
        try:
            login(request.form["user"], request.form["password"])
        except (IndexError, ValueError) as e:
            app.logger.info("Login failed with user:'{0}', pwd:'{1}' Error code: {2}".format(request.form["user"], request.form["password"], e) )
            var['msg'] = e
            template = env.get_template("web-res-login.html")
            return template.render(var)
        except Exception as e:
            app.logger.error('Unexpected error during login. Error code: {}'.format(e) )
            raise
        app.logger.info("User '{0}' logged in successfully".format(request.form["user"]) )
        return redirect(url_for('webreserved'))

    template = env.get_template("web-res-login.html")
    return template.render(var)
    

@app.route("/pannello/area-riservata/logout", methods=["GET", "POST"])
@login_required
def viewlogout():
    var = style("webmaster")
    template = env.get_template("web-res-login.html")
    user = session.get('username')

    try:
        logout()
    except Exception as e:
        app.logger.error('Error during logout of: {0} (Error code: {1})'.format(user, e) )
        var['msg'] = "Errore Interno.<br>Ripetere il login e tentare nuovamente il logout.<br>Se il problema persiste, contatta immediatamente il webmaster."
        return template.render(var)
        
    var['success'] = True
    var['msg'] = 'Logout completato con successo'
    app.logger.info("User '{0}' logged out successfully".format(user) )
    return template.render(var)


# ************* Upload *************************************************

@app.route("/pannello/area-riservata/upload/<obj>", methods=["GET", "POST"])
@login_required
def viewupload(obj):
    var = style("webmaster")
    var['obj'] = obj
    var['item'] = {}
    var = upload(var, request)
    template = env.get_template("web-res-upload.html")
    return template.render(var)




# ************ Manage **************************************************

@app.route("/pannello/area-riservata/manage/postit", methods=["GET", "POST"])
@login_required
def viewmanage_calendario():
    var = style("webmaster")
    var = managepostit(var, request)
    template = env.get_template("web-res-manage-postit.html")    
    return template.render(var)


@app.route("/pannello/area-riservata/manage/calendario", methods=["GET"])
@login_required
def viewmanage_postit():
    var = style("webmaster")
    #var = manage(var)
    template = env.get_template("web-res-manage-calendario.html")    
    return template.render(var)
    

@app.route("/pannello/area-riservata/manage/<obj>", methods=["GET"])
@login_required
def viewmanage(obj):
    var = style("webmaster")
    var['obj'] = obj
    var['manage'] = 'manage'
    var = manage(var)
    template = env.get_template("web-res-manage-main.html")    
    return template.render(var)
    
    
@app.route("/pannello/area-riservata/manage/<obj>/<int:id>", methods=["GET", "POST"])
@login_required
def viewmodify(obj, id):
    var = style("webmaster")
    var['obj'] = obj
    var['id'] = id
    var['item'] = {}
    var = modify(var, request)
    template = env.get_template("web-res-upload.html")
    return template.render(var)

    
# *********** Delete ***************************************************
    
@app.route("/pannello/area-riservata/delete/<obj>/<int:id>", methods=["GET", "POST"])
@login_required
def viewdelete(obj, id):
    var = style("webmaster")
    var['obj'] = obj
    var['id'] = id
    var['manage'] = 'delete'
    var = delete(var)
    template = env.get_template("web-res-delete.html")
    return template.render(var)
    

@app.route("/pannello/area-riservata/delete/news/<int:id>/<int:index>", methods=["GET", "POST"])
@login_required
def viewdeletepic(id, index):
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


