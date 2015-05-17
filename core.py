  #!/usr/local/bin/python
  # -*- coding: utf-8 -*-
  # The above is needed to set the correct encoding, see https://www.python.org/dev/peps/pep-0263/

from flask import Flask, request, session, abort, url_for, redirect, send_from_directory
from jinja2 import Environment, PackageLoader
from config import UPLOAD_FOLDER_PICS, UPLOAD_FOLDER_DOCS, ALLOWED_EXTENSIONS, DATABASE_PATH
from utils import login, logout
from database import load_news, load_note, load_doc
import sqlite3, os


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
		var = {"sidebar":["base/boxprog.html", "base/boxrif.html", "base/boxsez.html", "base/boxweb.html"]};
		var["url_for_css"] = "/static/css/style-programmi.css"
		
	elif style=="sezione":
		var = {"sidebar":["base/boxsez.html", "base/boxrif.html", "base/boxprog.html", "base/boxweb.html"]};
		var["url_for_css"] = "/static/css/style-sezione.css"
		
	elif style=="webmaster":
		var = {"sidebar":["base/boxweb.html", "base/boxrif.html", "base/boxprog.html", "base/boxsez.html"]};
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
	
@app.route('/uploads/<filename>')
def static_file(filename):
	""" Serves static files """
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/pannello/area-riservata/login", methods=["GET", "POST"])
def weblogin():
	var = style("webmaster")
				
	if request.method == "POST":
		log = login(request.form["user"], request.form["password"])
		if log:
			var['msg'] = log
			template = env.get_template("web-res-login.html")
			return template.render(var)
		else:
			return redirect(url_for('webres'))

	template = env.get_template("web-res-login.html")
	return template.render(var)
	

@app.route("/pannello/area-riservata/logout", methods=["GET"])
def weblogout():
	if not session.get('logged_in'):
		return redirect(url_for('weblogin'))
	var = style("webmaster")
	log = logout()
	if log:
		var['msg'] = log
		template = env.get_template("web-res-login.html")
		return template.render(var)
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
	
	if request.method == 'POST':
		var["upload_fail"] = 'fail'
		var['msg']="Upload non riuscito. Riprova o contatta il webmaster."
		conn = sqlite3.connect(DATABASE_PATH)
		with conn:
			cursor = conn.cursor()
			if obj=="news":
				var = load_news(request, var, cursor, app)
			elif obj=='note':
				var = load_note(request, var, cursor, app)
			elif obj=='doc':
				var = load_doc(request, var, cursor, app)
		conn.commit()
		conn.close()

	return template.render(var)
	
	
@app.route("/pannello/area-riservata/manage/<obj>", methods=["GET", "POST"])
def webmanage(obj):
	if not session.get('logged_in'):
		redirect(url_for('weblogin'))
		
	var = style("webmaster")
	var['obj'] = obj
	template = env.get_template("web-res-manage-main.html")


	var['lista'] = [ u'ciao', u'hello', u'ça va', u'добро утро', u'你好吗']
	var['lista'] = [ {'id': 1, 'date':'today',  'title': u'ciao'},
					 {'id': 2, 'date':'tooday',  'title': u'hello'}, 
					 {'id': 3, 'date':'toooday',  'title': u'ça va'},
					 {'id': 4, 'date':'tooooday',  'title': u'добро утро'},
					 {'id': 5, 'date':'tday',  'title': u'你好吗'}  ]

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
