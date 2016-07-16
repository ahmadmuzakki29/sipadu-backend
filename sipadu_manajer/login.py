import web
import random, string, json
import model

class login:
	def POST(self):
		self.data = web.input()
		web.header('Content-Type', 'application/json')
		
		if not hasattr(self.data, "auth"): return web.NotFound()
		else: return self.auth() 
	
	def auth(self):
		data = self.data
		
		try:
			username = data.username 
			password = data.password
			
			query = ("select username,token from manajer "
				"where username=%s and password=%s")
			
			res = model.get_query(query,(username,password))
			if res!=None:
				return self.berhasil(username)
			else:
				return self.gagal()
		except:
			web.NotFound()

	def berhasil(self,username):
		token = self.createToken(username)
		query = "update manajer set token='"+token+"' where username='"+username+"'"
		model.query(query)
		
		data = {"response":"OK","token":token}
		return json.dumps(data)
	
	def createToken(self,username):
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
			param = (data.username,data.token)
			
			query = "select username from manajer where username=%s and token=%s"
			result = model.get_query(query, param)
			
			if result!=None:
				return json.dumps({"response":"OK"})
			else:
				return json.dumps({"response":"ERROR"})
		except:
			return web.notfound()
	
