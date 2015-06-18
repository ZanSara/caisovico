import os, shutil, sqlite3
import unittest
import views

from config import app, BASE_PATH, DATABASE_PATH, UPLOAD_FOLDER_DOCS, UPLOAD_FOLDER_PICS
from core import home, homepages



class CAITestCase(unittest.TestCase):

    def setUp(self):
        # Set self attributes
        os.rename('base.sqlite', 'base-safe.sqlite')
        self.database = 'base.sqlite'
        self.var = {}
        self.app = app.test_client()
        # Create an empty clone of the database for testing purposes
        try:
            test_conn = sqlite3.connect(self.database)
            old_conn = sqlite3.connect('base-safe.sqlite')
            with old_conn:
                cursor = old_conn.cursor()
                old_scheme = list(cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite%'") ) # Skips sqlite_sequence
            with test_conn:
                cursor = test_conn.cursor()
                for item in old_scheme:
                    result = cursor.execute(item[0])
                result = cursor.execute('INSERT INTO users VALUES (?, ?)', ["admin", "admin"])
        except Exception as e:
            print '#############################################', e
            raise
            
    def tearDown(self):
        # This should overwrite the test database
        os.rename('base-safe.sqlite', 'base.sqlite')
        
    
  
    # ******* Empty Database Tests *************************************
    # Here I loaded no news or notes.
    
    def test_homepage_empty_http(self):
        # Check the httpresponse
        res = self.app.get('/')
        self.assertIn( 'Al momento non ci sono notizie sulla nostra homepage', res.data)
        self.var = home(self.var)
        self.assertEqual( len(self.var['newslist']), 0 )
        self.assertEqual( len(self.var['noteslist']), 0 )
        self.assertEqual( self.var['curpage'], 1 )
        self.assertGreaterEqual( self.var['totpage'], 1 )
    def test_homepage_empty_var(self):
        # Check home's var's content
        self.var = home(self.var)
        self.assertIn( len(self.var['newslist']), xrange(0, 6) )
        self.assertLessEqual( len(self.var['noteslist']), 5 )
        self.assertEqual( self.var['curpage'], 1 )
        self.assertGreaterEqual( self.var['totpage'], 1 )
    def test_homepage_empty_nonext(self):
        # Check non-existent next homepages
        res = self.app.get('/2')
        self.assertIn( '404 - Pagina Inesistente', res.data )
    def test_homepage_empty_nonews(self):
        # Check no fullnews available
        res = self.app.get('/news/0')
        self.assertIn( '404 - Pagina Inesistente', res.data )
    def test_homepage_empty_nodb(self):
        # Check what happens if the database does not exist
        os.remove(self.database)
        res = self.app.get('/')
        self.assertIn( 'inconveniente tecnico', res.data)
    
    
    # NO TESTS for static pages  
     
     
    # ******* Static Files Tests ***************************************
    
    def test_sendstaticfiles_200(self):
        # Pictures
        shutil.copyfile('xtest.jpg', '{}/xtest.jpg'.format(UPLOAD_FOLDER_PICS))
        res = self.app.get('{}/xtest.jpg'.format(UPLOAD_FOLDER_PICS))
        self.assertEqual(200, res.status_code)
        os.remove('{}/xtest.jpg'.format(UPLOAD_FOLDER_PICS))
        # Docs
        shutil.copyfile('xtest.jpg', '{}/xtest.jpg'.format(UPLOAD_FOLDER_DOCS))
        res = self.app.get('{}/xtest.jpg'.format(UPLOAD_FOLDER_DOCS))
        self.assertEqual(200, res.status_code)
        os.remove('{}/xtest.jpg'.format(UPLOAD_FOLDER_DOCS))
    def test_sendstaticfiles_404(self):
         # Pictures
        res = self.app.get('{}/xtest.jpg'.format(UPLOAD_FOLDER_PICS))
        self.assertEqual(404, res.status_code)
        # Docs
        res = self.app.get('{}/xtest.jpg'.format(UPLOAD_FOLDER_DOCS))
        self.assertEqual(404, res.status_code)
        
        
    # ******* Admin Login Tests ****************************************
     
    def login(self, user, pwd):
        return self.app.post('/pannello/area-riservata/login', data=dict(
        user=user,
        password=pwd
    ), follow_redirects=True)
    def logout(self):
        return self.app.get('/pannello/area-riservata/logout', follow_redirects=True)
    def test_loginlogout_admin(self):
        # Should hide the password here!
        res = self.login('admin', 'admin')
        self.assertIn( 'Utility del Server', res.data )
        res = self.login('a', 'admin')
        self.assertIn( 'Nome utente non valido', res.data )
        res = self.login('admin', 'a')
        self.assertIn( 'Password errata', res.data )
    
    
    # ******* Upload Tests *********************************************
     
            
      


if __name__ == '__main__':
    unittest.main()
