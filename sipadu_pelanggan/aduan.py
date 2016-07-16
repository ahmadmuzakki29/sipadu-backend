import web
import json,model
from notification import notification as notif
class sync_aduan:
	cols = "id,waktu,kategori,aduan,tindak_lanjut,waktu_tindak_lanjut"
	def POST(self):
		self.data = web.input()
		web.header('Content-Type', 'application/json')
		
		if not hasattr(self.data, "sync"): 
			web.NotFound()
		elif self.data.sync=="all":
			return self.sync_all();
		elif self.data.sync=="latest":
			return self.sync_last()
	
	def sync_all(self):
		
		try:
			nosambungan = self.data.nosambungan
		except:
			web.notfound()
		
		query = "select "+self.cols+" from aduan where nosambungan=%s"
		result = model.get_query(query,(nosambungan,))
		
		if(result==None): return json.dumps([])
		else: return json.dumps(result)
				
	def sync_last(self):
		try:
			nosambungan = self.data.nosambungan
			waktu = self.data.waktu
		except:
			web.notfound()
			
		query = "select "+self.cols+" from aduan where waktu > %s and nosambungan=%s"
		result = model.get_query(query,(waktu,nosambungan))
		
		if(result==None): return json.dumps([])
		else: return json.dumps(result)



class simpan_aduan:
	def POST(self):
		self.data = web.input()
		web.header('Content-Type', 'application/json')
		
		if not hasattr(self.data, "simpan_aduan"): 
			web.NotFound()
		else:
			return self.simpan();
	
	def simpan(self):
		data = self.data
		
		try:
			nosambungan = data.nosambungan
			kategori = data.kategori
			aduan = data.aduan
			lat = 0 if not hasattr(data, "lat") else data.lat
			longitude = 0 if not hasattr(data,"long") else data.long
		except:
			web.notfound()
		
		field = (nosambungan,kategori,aduan,lat,longitude)
		query = "insert into aduan(nosambungan,waktu,kategori,aduan,lat,`long`) value(%s,sysdate(2),%s,%s,%s,%s)"
		_id = model.query(query, field)
		
		query = "select waktu from aduan where id=%s"
		result = model.get_query(query, (_id,)) 
		waktu = result[0]["waktu"]
		data = {"id":_id,"waktu":waktu}
		
		notif().notif_inbox_manajer()
		return json.dumps(data)


class tindak_lanjut:
	def POST(self):
		self.data = web.input()
		web.header('Content-Type', 'application/json')
		
		if not hasattr(self.data, "action"): 
			web.NotFound()
		elif self.data.action == "get_tindak_lanjut":
			return self.get_tindak_lanjut();
	
	def get_tindak_lanjut(self):
		data = self.data 
		try:
			_id = data.id
		except:
			web.notfound()
		
		field = (_id,)
		query = "select tindak_lanjut,waktu_tindak_lanjut from aduan where id=%s"
		result = model.get_query(query, field)
		
		query = "delete from pelanggan_notif where id_aduan=%s"
		model.query(query,field);
		return json.dumps(result[0])
		
