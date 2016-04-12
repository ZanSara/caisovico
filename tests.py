import os, io, shutil, sqlite3
import unittest
import views

from config import app, BASE_PATH, DATABASE_PATH, UPLOAD_FOLDER_DOCS, UPLOAD_FOLDER_PICS
from core import home, homepages
from database import retrieve_item



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
        # Testing superuser, see setUp()
        res = self.login('admin', 'admin')
        self.assertIn( 'Utility del Server', res.data )
        res = self.login('a', 'admin')
        self.assertIn( 'Nome utente non valido', res.data )
        res = self.login('admin', 'a')
        self.assertIn( 'Password errata', res.data )
        
    def test_loginrequired(self):
        # Not logged
        res = self.app.get('/pannello/area-riservata/logout', follow_redirects=True)
        self.assertIn('Login', res.data)
        res = self.app.get('/pannello/area-riservata/upload/news', follow_redirects=True)
        self.assertIn('Login', res.data)
        res = self.app.get('/pannello/area-riservata/manage/news', follow_redirects=True)
        self.assertIn('Login', res.data)
        res = self.app.get('/pannello/area-riservata/manage/news/0', follow_redirects=True)
        self.assertIn('Login', res.data)
        res = self.app.get('/pannello/area-riservata/delete/news/0', follow_redirects=True)
        self.assertIn('Login', res.data)
        res = self.app.get('/pannello/area-riservata/delete/news/0/0', follow_redirects=True)
        self.assertIn('Login', res.data)
        # Logged
        res = self.login('admin', 'admin')
        res = self.app.get('/pannello/area-riservata/upload/news', follow_redirects=True)
        self.assertIn('Upload', res.data)
        res = self.app.get('/pannello/area-riservata/manage/news', follow_redirects=True)
        self.assertIn('Notizie', res.data)
        res = self.app.get('/pannello/area-riservata/manage/news/0', follow_redirects=True)
        self.assertIn('Modifica', res.data)
        res = self.app.get('/pannello/area-riservata/delete/news/0', follow_redirects=True)
        self.assertIn('Elimina', res.data)
        res = self.app.get('/pannello/area-riservata/delete/news/0/0', follow_redirects=True)
        self.assertIn('Elimina', res.data)
        res = self.app.get('/pannello/area-riservata/logout', follow_redirects=True)
        self.assertIn('Logout completato con successo', res.data)
        
    
    # ******* Upload Tests *********************************************
    # Requires admin permissions!
    
    def login_admin(self):
        # Testing admin, see setUp()
        return self.login('admin', 'admin')
        
    def upload(self, obj, req):
        return self.app.post('/pannello/area-riservata/upload/{}'.format(obj), data=req, follow_redirects=True)
    
    def retrieve_lastinserted(self, obj):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            return cursor.execute('SELECT COUNT(*) FROM {}'.format(obj)).fetchone()[0]
        print 'LastInserted Error!'
        return -1
            
        
        # ******* News Sector ***********************
    
    def check_upload_news(self, id, expect):
        # Here I assume that retrieve_item() from database.py works fine (will test it later)
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            result = retrieve_item('news', id, cursor)
        self.assertEqual( expect['data'], result['date'])
        self.assertEqual( expect['titolo'], result['title'])
        self.assertEqual( expect['testo'], result['content'])
        for i in xrange(len(result['pics'])):
            expectfile = open(expect['foto{}'.format(i)][0], 'rb')
            resultfile = open("uploads/photos/{0}".format(result['pics'][i][2]), 'rb')
            self.assertEqual( expectfile.read(), resultfile.read() )
            expectfile.close()
            resultfile.close()
            self.assertEqual(expect['descrizione{}'.format(i)], result['pics'][i][1])
        return
    def make_news(self, data, title, text, foto, descrizione):
        req = {
            'data': data,
            'titolo': title,
            'testo': text
            }
        for i in xrange(0, len(foto)):
            req['foto{}'.format(i)] = foto[i]
            req['descrizione{}'.format(i)] = descrizione[i]
        return req

    def test_uploadnews_onlytext_ok(self):
        self.login_admin()
        expect = self.make_news('01/06/2015', 'Only Text OK', 'Text of the 1st "Only Text" Test News.', [], [])
        res = self.upload('news', expect)
        self.assertIn('Upload completato con successo', res.data)
        self.check_upload_news(self.retrieve_lastinserted('news'), expect)
    def test_uploadnews_onlytext_wrongdata(self):
        self.login_admin()
        expect = self.make_news('01-06-2015', 'Only Text WrongData', 'Text of the 2nd "Only Text" Test News.', [], [])
        res = self.upload('news', expect)
        self.assertIn('Inserire una data valida', res.data)
        with self.assertRaises(Exception): # Tests that the news wasn't loaded in the database
            self.check_upload_news(self.retrieve_lastinserted('news'), expect)
    def test_uploadnews_onlytext_nodata(self):
        self.login_admin()
        expected = self.make_news('', 'Only Text NoData', 'Text of the 3rd "Only Text" Test News.', [], [])
        res = self.upload('news', expected)
        self.assertIn('Inserire una data valida', res.data)
        with self.assertRaises(Exception):
            self.check_upload_news(self.retrieve_lastinserted('news'), expect)
    def test_uploadnews_onlytext_notitle(self):
        self.login_admin()
        expected = self.make_news('01-06-2015', '', 'Text of the 4th "Only Text" Test News.', [], [])
        res = self.upload('news', expected)
        self.assertIn('Impossibile caricare una notizia senza titolo', res.data)
        with self.assertRaises(Exception):
            self.check_upload_news(self.retrieve_lastinserted('news'), expect)
    def test_uploadnews_onlytext_notext(self):
        self.login_admin()
        expected = self.make_news('01-06-2015', 'Only Text NoText', '', [], [])
        res = self.upload('news', expected)
        self.assertIn('Impossibile caricare una notizia senza testo', res.data)
        with self.assertRaises(Exception):
            self.check_upload_news(self.retrieve_lastinserted('news'), expect)
    
    def test_uploadnews_onepicture(self):
        self.login_admin()
        photo = open('xtest.jpg', 'rb')
        expect = self.make_news('01/06/2015', 'OnePicture', 'Text of the "OnePicture" Test News.', [photo], ['OnePicture test photo'])
        res = self.upload('news', expect)
        self.assertIn('Upload completato con successo', res.data)
        self.check_upload_news(self.retrieve_lastinserted('news'), expect)
    
    
            
        # ******* Notes Sector ***********************
        
    def check_upload_notes(self, id, expect):
        # Here I assume that retrieve_item() from database.py works fine (will test it later)
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            result = retrieve_item('note', id, cursor)
        self.assertEqual(expect['testo'], result['content'])
    def make_note(self, text):
        return {'testo':text}
        
    def test_uploadnote_ok(self):
        self.login_admin()
        expect = self.make_note('Test Note 1')
        res = self.upload('note', expect)
        self.assertIn('Upload completato con successo', res.data)
        self.check_upload_notes(self.retrieve_lastinserted('notes'), expect)
    def test_uploadnote_empty(self):
        self.login_admin()
        expect = self.make_note('')
        res = self.upload('note', expect)
        self.assertIn('Impossibile caricare una nota vuota', res.data)
        with self.assertRaises(Exception):
            self.check_upload_notes(self.retrieve_lastinserted('notes'), expect)


if __name__ == '__main__':
    unittest.main()
