import web,model
import paho.mqtt.publish as publish

class notification:
	topic = "USERS/SIPADU_PELANGGAN/"
	topic_manajer = "USERS/SIPADU_MANAJER/"
	auth = {"username":"user","password":"rahasia"}
	def POST(self):
		self.data = web.input()
		web.header('Content-Type', 'application/json')
		
		if not hasattr(self.data, "action"): 
			return web.NotFound()
		elif self.data.action == "get_notif":
			return self.get_notif()
		elif self.data.action=="notif_inbox":
			return self.notif_inbox_manajer()
		
	def get_notif(self):
		data = self.data 
		
		try:
			nosambungan = data.nosambungan
		except:
			web.notfound()
		
		query = """select a.id from aduan a join pelanggan_notif n 
			on a.id=n.id_aduan 
			where a.nosambungan=%s group by a.id
		"""
		
		data = (nosambungan,)
		result = model.get_query(query, data)
		
		if result==None: return "tidak ada notif";
		
		for id_row in result:
			id_tb = id_row["id"]
			publish.single(self.topic+nosambungan, id_tb,hostname="localhost",auth=self.auth,client_id="sipadu_notif_pelanggan")
		
		
	def notif_inbox_manajer(self):
		query = "select username from manajer"
		result = model.get_query(query)
		msgs = []
		for row in result:
			username = row['username']
			msg = {'topic':self.topic_manajer+username, 'payload':"inbox"}
			msgs.append(msg)
		publish.multiple(msgs,hostname="localhost",auth=self.auth,client_id="sipadu_notif_inbox")
