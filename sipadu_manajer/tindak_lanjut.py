import web,model
import paho.mqtt.publish as publish
import json
class tindak_lanjut:
	topic = "USERS/SIPADU_PELANGGAN/"
	topic_manajer = "USERS/SIPADU_MANAJER/"
	auth = {"username":"user","password":"rahasia"}
	def POST(self):
		self.data = web.input()
		web.header('Content-Type', 'application/json')
		
		if not hasattr(self.data, "action"): 
			return web.NotFound()
		if self.data.action=="simpan":
			return self.simpanTindakLanjut()
		
	def simpanTindakLanjut(self):
		data = self.data
		
		try:
			_id = data.id
			tindak_lanjut = data.tindak_lanjut
			username = data.username
		except:
			return web.notfound()
		
		query = """update aduan set tindak_lanjut=%s, 
			waktu_tindak_lanjut=sysdate(2), manajer=%s where id=%s"""
		model.query(query,(tindak_lanjut,username,_id))
		
		self.notif_pelanggan(_id)
		self.notif_manajer(username)
		
		query = "select waktu_tindak_lanjut from aduan where id=%s"
		result = model.get_query(query,(_id,))
		waktu = result[0]["waktu_tindak_lanjut"]
		return json.dumps({"waktu_tindak_lanjut":waktu})
	
	def notif_pelanggan(self,_id):
		query = "select nosambungan from aduan	where id=%s"
		data = (_id,)
		result = model.get_query(query, data)
		nosambungan = result[0]["nosambungan"]
		publish.single(self.topic+nosambungan, payload=str(_id),hostname="localhost",auth=self.auth,client_id="sipadu_notif_pelanggan")
	
	def notif_manajer(self,username):
		query = "select username from manajer where not username = %s"
		result = model.get_query(query,(username,))
		messages = []
		for row in result:
			username = row['username']
			msg = {'topic':self.topic_manajer+username, 'payload':"inbox"}
			messages.append(msg)
		publish.multiple(messages,hostname="localhost",auth=self.auth,client_id="sipadu_notif_inbox")
