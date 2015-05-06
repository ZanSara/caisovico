from flask import Flask, request
from jinja2 import Environment, PackageLoader


env = Environment(loader=PackageLoader('core', '/templates'))

app = Flask(__name__, static_folder="static")

app.secret_key = ".ASF\x89m\x14\xc9s\x94\xfaq\xca}\xe1/\x1f3\x1dFx\xdc\xf0\xf9"



# Serves static files (css, js and pictures)
@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route("/" , methods=["GET"])
def home():
    var = {"boxes":['boxes/boxrif.html','boxes/boxprog.html','boxes/boxsez.html','boxes/boxweb.html',]}
    template = env.get_template("home.html")
    return template.render(var)







if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")




