from flask import Flask, request, url_for, send_from_directory
from jinja2 import Environment, PackageLoader

import os.path


env = Environment(loader=PackageLoader('core', '/templates'))

app = Flask(__name__, static_folder="static")

app.secret_key = ".ASF\x89m\x14\xc9s\x94\xfaq\xca}\xe1/\x1f3\x1dFx\xdc\xf0\xf9"



def style(style):
	""" style() is just an utility to make some modification regarding the
		styles of different sections of the website (css, boxes order)"""
	if style=="home":
		var = {"sidebar":["base/boxrif.html", "base/boxprog.html", "base/boxsez.html", "base/boxweb.html"]};
		var["url_for_css"] = "static/css/style-home.css"
		
	elif style=="rifugio":
		var = {"sidebar":["base/boxrif.html", "base/boxprog.html", "base/boxsez.html", "base/boxweb.html"]};
		var["url_for_css"] = "static/css/style-rifugio.css"
		
	elif style=="programmi":
		var = {"sidebar":["base/boxprog.html", "base/boxrif.html", "base/boxsez.html", "base/boxweb.html"]};
		var["url_for_css"] = "static/css/style-programmi.css"
		
	elif style=="sezione":
		var = {"sidebar":["base/boxsez.html", "base/boxrif.html", "base/boxprog.html", "base/boxweb.html"]};
		var["url_for_css"] = "static/css/style-sezione.css"
		
	elif style=="webmaster":
		var = {"sidebar":["base/boxweb.html", "base/boxrif.html", "base/boxprog.html", "base/boxsez.html"]};
		var["url_for_css"] = "static/css/style-webmaster.css"
		
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
	
@app.route("/pannello/area-riservata" , methods=["GET"])
def webres():
	var = style("webmaster")
	template = env.get_template("web-reserved.html")
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










if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
