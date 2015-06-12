#!/usr/local/bin/python
  # -*- coding: utf-8 -*-
  # The above is needed to set the correct encoding, see https://www.python.org/dev/peps/pep-0263/
    
    
try:
    import logging, os
    from flask import Flask
    from jinja2 import Environment, PackageLoader
except Exception as e:
    print 'CONFIG IMPORTING ERROR: {}'.format(e)
    logging.CRITICAL('CONFIG IMPORTING ERROR')

   
# *********** Definitions **********************************************

BASE_PATH = os.getcwd()
UPLOAD_FOLDER_DOCS = 'uploads/docs'
UPLOAD_FOLDER_PICS = 'uploads/photos'
ALLOWED_EXTENSIONS_PICS = set(['png', 'jpg', 'jpeg', 'gif', 'tif', 'tiff'])
ALLOWED_EXTENSIONS_DOCS = set(['txt', 'pdf'])
DATABASE_PATH = 'base.sqlite'

# *********** Setup ****************************************************

app = Flask(__name__, static_folder="static")
app.config['UPLOAD_FOLDER_DOCS'] = UPLOAD_FOLDER_DOCS
app.config['UPLOAD_FOLDER_PICS'] = UPLOAD_FOLDER_PICS
app.secret_key = ".ASF\x89m\x14\xc9s\x94ff\xfaq\xca}h\xe1/\x1f3\x1dFxj\xdc\xf0\xf9..."

env = Environment(loader=PackageLoader('config', '/templates'))

