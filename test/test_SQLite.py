import pytest
import sys
sys.path.append('..')
sys.path.append('../drivers')
from SQLite import SQLite
from joinsdb import JoinsDb

# SQLite test
def test_SQLite() :
    jdb = JoinsDb()
    jdb.setStorage(SQLite("sample.sqlite3"))
    assert [(0, 0), (1, 0), (2, 0), (3, 1), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 1)] == jdb.executeQuery("select * from g2_r")
    jdb.close()