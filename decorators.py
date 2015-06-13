#!/usr/local/bin/python
  # -*- coding: utf-8 -*-
  # The above is needed to set the correct encoding, see https://www.python.org/dev/peps/pep-0263/
   
try:
    from config import app
    from functools import wraps
    from flask import g, request, session, redirect, url_for
except Exception as e:
    print 'DECORATORS IMPORTING ERROR: {0}'.format(e)
    app.logger.critical('DECORATORS IMPORTING ERROR: {0}'.format(e) )
    raise


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') is None:
            app.logger.info('Tried to access Area Riservata without permission')
            return redirect(url_for('viewlogin'))
        return f(*args, **kwargs)
    return decorated_function
