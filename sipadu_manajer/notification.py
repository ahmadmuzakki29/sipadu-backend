import web,model
import paho.mqtt.publish as publish

class notification:
	topic = "USERS/SIPADU_MANAJER/"
	auth = {"username":"user","password":"rahasia"}
	def POST(self):
		self.data = web.input()
		web.header('Content-Type', 'application/json')
		
		if not hasattr(self.data, "action"): 
			return web.NotFound()
		elif self.data.action == "get_notif":
			return self.get_notif()
		
	def get_notif(self):
		data = self.data 
		
		try:
			username = data.username
		except:
			return web.notfound()
		
		query = "select have_notif_inbox,have_notif_outbox from manajer where username=%s"
		result = model.get_query(query,(username,))
		result = result[0]
		notif_in = result["have_notif_inbox"]
		notif_out = result["have_notif_outbox"]
		if notif_in=="1":
			publish.single(self.topic+username, "inbox",hostname="localhost",auth=self.auth,client_id="sipadu_notif_inbox")
		
		if notif_out=="1":
			publish.single(self.topic+username, "outbox",hostname="localhost",auth=self.auth,client_id="sipadu_notif_outbox")
		
