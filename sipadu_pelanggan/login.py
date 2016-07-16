import web
import random, string, json
import model

class login_pelanggan:
	def POST(self):
		self.data = web.input()
		web.header('Content-Type', 'application/json')
		
		if not hasattr(self.data, "auth"): return web.NotFound()
		else: return self.auth() 
	
	def auth(self):
		data = self.data
		
		try:
			nosambungan = data.nosambungan 
			password = data.password
			
			query = ("select nosambungan,token from pelanggan "
				"where nosambungan=%s and password=%s")
			
			res = model.get_query(query,(nosambungan,password))
			if res!=None:
				return self.berhasil(nosambungan)
			else:
				return self.gagal()
		except:
			web.NotFound()

	def berhasil(self,nosambungan):
		token = self.createToken(nosambungan)
		query = "update pelanggan set token='"+token+"' where nosambungan='"+nosambungan+"'"
		model.query(query)
		
		data = {"response":"OK","token":token}
		return json.dumps(data)
	
	def createToken(self,nosambungan):
		length = 50
		return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))
		
	def gagal(self):
		data = {"response":"ERROR","message":"Login Gagal!"}
		return json.dumps(data)

class check_token:
	def POST(self):
		self.data = web.input()
		web.header('Content-Type', 'application/json')
		
		if not hasattr(self.data, "check"): return web.NotFound()
		else: return self.check()
	
	def check(self):
		data = self.data
		
		try:
			param = (data.nosambungan,data.token)
			
			query = "select nosambungan from pelanggan where nosambungan=%s and token=%s"
			result = model.get_query(query, param)
			
			if result!=None:
				return json.dumps({"response":"OK"})
			else:
				return json.dumps({"response":"ERROR"})
		except:
			return web.notfound()
	
