  #!/usr/local/bin/python
  # -*- coding: utf-8 -*-
  # The above is needed to set the correct encoding, see https://www.python.org/dev/peps/pep-0263/

try:
    from views import app
    import logging
    from logging.handlers import RotatingFileHandler
except Exception as e:
    print '####', e
    raise

# Logging stuff
file_handler = RotatingFileHandler('log/log.log', 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('''#### %(asctime)s ==> %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]'''))

# Change logging.INFO to logging.DEBUG to see debugging verbose information
file_handler.setLevel(logging.INFO)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.info('Starting up...')



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    
    
    # Only matter of style...
    file_handler.setFormatter(logging.Formatter('''#### %(asctime)s ==> %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]
################'''))
    app.logger.info('Switching off..')
