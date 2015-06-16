import os, sqlite3
import unittest

from config import app, BASE_PATH, DATABASE_PATH
from core import home



class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Create an empty clone of the database for testing purposes
        test_conn = sqlite3.connect('test.sqlite')
        old_conn = sqlite3.connect(DATABASE_PATH)
        with old_conn:
            cursor = old_conn.cursor()
            old_scheme = list(cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite%'") ) # Skips sqlite_sequence
        with test_conn:
            cursor = test_conn.cursor()
            for item in old_scheme:
                result = cursor.execute(item[0])
        self.database = 'test.sqlite'
        

    def tearDown(self):
        pass
        os.remove('test.sqlite')
        
        
    def test_loadhomepage(self):
        var = {}
        var = home(var)
        self.assertIn( len(var['newslist']), xrange(0, 6) )
        self.assertLessEqual( len(var['noteslist']), 5 )
        self.assertEqual( var['curpage'], 1 )
        self.assertGreaterEqual( var['totpage'], 1 )
            
        

if __name__ == '__main__':
    unittest.main()
