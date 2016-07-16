import web,model
import json

class sync:
	limit = ""#"limit 2"
	def POST(self):
		self.data = web.input()
		web.header('Content-Type', 'application/json')
		
		if not hasattr(self.data, "sync"): 
			return web.NotFound()
		elif self.data.sync=="all": 
			return self.sync_all() 
		elif self.data.sync=="get_inbox":
			return self.get_inbox()
		elif self.data.sync=="get_outbox":
			return self.get_outbox()
		
	
	def sync_all(self):
		query1 = """select id,a.nosambungan,nama,aduan,waktu,kategori,lat,`long` 
			from aduan a
			join pelanggan p on a.nosambungan=p.nosambungan
			where tindak_lanjut is Null 
			order by waktu desc """
		result1 = model.get_query(query1)
		
		query2 = """select id,a.nosambungan,nama,aduan,waktu,kategori,
			tindak_lanjut,waktu_tindak_lanjut,manajer,lat,`long`  
			from aduan a
			join pelanggan p on a.nosambungan=p.nosambungan
			where tindak_lanjut is not null 
			order by waktu desc """
		result2 = model.get_query(query2)
		
		result = {"inbox":result1,"outbox":result2}
		return json.dumps(result)
	
	def get_inbox(self):
		data = self.data
		try:
			username = data.username
			last_msg = ""
			if data.last_msg != "0" :
				last_msg = " and waktu>'"+data.last_msg+"' "
		except:
			web.notfound()
		
		query1 = """select id,a.nosambungan,nama,aduan,waktu,kategori,lat,`long`
			from aduan a
			join pelanggan p on a.nosambungan=p.nosambungan
			where tindak_lanjut is Null """+last_msg+"""
			order by waktu desc """+self.limit
		result = model.get_query(query1)
		
		query_update = "update manajer set have_notif_inbox=0 where username=%s"
		model.query(query_update,(username,))
		
		return json.dumps(result)
	
	def get_outbox(self):
		data = self.data
		try:
			username = data.username
			last_msg = ""
			if data.last_msg != "0" :
				last_msg = " and waktu>'"+data.last_msg+"' "
		except:
			web.notfound()
		
		query = """select id,a.nosambungan,nama,aduan,waktu,
			tindak_lanjut,waktu_tindak_lanjut, kategori, manajer,lat,`long`
			from aduan a
			join pelanggan p on a.nosambungan=p.nosambungan
			where tindak_lanjut is not Null """+last_msg+"""
			order by waktu desc """+self.limit
		result = model.get_query(query)
		
		query_update = "update manajer set have_notif_outbox=0 where username=%s"
		model.query(query_update,(username,))
		return json.dumps(result)
		
	
		
		
		
		
		
