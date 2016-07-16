#!/usr/bin/python
import sys, os, signal
os.kill(os.getpid(), signal.SIGINT)
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import web
from login import *
from aduan import *
from notification import *

urls = (
	'/login_pelanggan/', 'login_pelanggan',
	'/sync_aduan/','sync_aduan',
	'/check_token/','check_token',
	'/simpan_aduan/','simpan_aduan',
	'/notification/','notification',
	'/tindak_lanjut/','tindak_lanjut'
)


app = web.application(urls, globals())

#web.config.debug = True

application = app.wsgifunc()