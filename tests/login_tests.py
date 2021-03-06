import sys
from software.app_files import database as db
from software.app_files import login
from tests.modified_app_files import login_mod

db.connectDB()

def test_encrypt():
	assert login.encrypt("ABC") == "CDE"

def test_decrypt():
	assert login.decrypt("CDE") == "ABC"

def test_beginFlow():
	assert login_mod.beginFlow(db.getUser("Lq{3","Lq{345")) == True

def test_start():
	assert login_mod.start('Joy1', 'Joy123', False) == "User flow began 1"
