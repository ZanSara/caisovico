import os

BASE_PATH = os.getcwd()
UPLOAD_FOLDER_DOCS = 'uploads/docs'
UPLOAD_FOLDER_PICS = 'uploads/photos'
ALLOWED_EXTENSIONS_PICS = set(['png', 'jpg', 'jpeg', 'gif', 'tif', 'tiff'])
ALLOWED_EXTENSIONS_DOCS = set(['txt', 'pdf'])
DATABASE_PATH = 'base.sqlite'
