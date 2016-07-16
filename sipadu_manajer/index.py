#!/usr/bin/python
import sys, os, signal
os.kill(os.getpid(), signal.SIGINT)
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import web
from sync import sync
from login import *
from notification import *
from tindak_lanjut import *
urls = (
	'/login/','login',
	'/check_token/','check_token',
	'/sync/','sync',
	'/notification/','notification',
	'/tindak_lanjut/','tindak_lanjut',
)


app = web.application(urls, globals())

#web.config.debug = True

application = app.wsgifunc()
