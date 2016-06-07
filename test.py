import unittest
import json
from app import app
from models.models import *

class Test(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True

	def tearDown(self):
		db.execute_sql("Delete from activity")
		db.execute_sql("Delete from user")

	def test_test(self):
		result = self.app.get('/test')
		self.assertEquals(result.status_code, 200)
		json_obj = json.loads(result.data)
		self.assertEquals(json_obj['message'], "hello")

	def test_register(self):
		longMessage = True
		raw_body = {}
		result = self.app.post('/register',data=json.dumps(raw_body), content_type='application/json')
		self.assertEquals(result.status_code, 200)
		json_obj = json.loads(result.data)
		self.assertEquals(json_obj['success'], False)
		
		#missing password
		raw_body['username'] = 'test'
		result = self.app.post('/register',data=json.dumps(raw_body), content_type='application/json')
		self.assertEquals(result.status_code, 200)
		json_obj = json.loads(result.data)
		self.assertEquals(json_obj['success'], False)
		
		#missing email
		raw_body['password'] = '1234'
		result = self.app.post('/register',data=json.dumps(raw_body), content_type='application/json')
		self.assertEquals(result.status_code, 200)
		json_obj = json.loads(result.data)
		self.assertEquals(json_obj['success'], False)

		#create user
		raw_body['email'] = 'test@test.test'
		result = self.app.post('/register',data=json.dumps(raw_body), content_type='application/json')
		self.assertEquals(result.status_code, 200)
		json_obj = json.loads(result.data)
		self.assertEquals(json_obj['success'], True)

		#check user is created in db
		user = User.get(User.username == 'test')
		self.assertEquals(user.username, 'test')
		#check password is not plain text password
		self.assertNotEquals(user.password, '1234')
		self.assertEquals(user.email, 'test@test.test')

		#TEST AUTH
		raw_body = {}
		result = self.app.post('/auth',data=json.dumps(raw_body), content_type='application/json')
		self.assertEquals(result.status_code, 200)
		json_obj = json.loads(result.data)
		self.assertEquals(json_obj['success'], False)

		raw_body['username'] = 'test'
		result = self.app.post('/auth',data=json.dumps(raw_body), content_type='application/json')
		self.assertEquals(result.status_code, 200)
		json_obj = json.loads(result.data)
		self.assertEquals(json_obj['success'], False)

		raw_body['password'] = '1234'
		result = self.app.post('/auth',data=json.dumps(raw_body), content_type='application/json')
		self.assertEquals(result.status_code, 200)
		json_obj = json.loads(result.data)
		self.assertEquals(json_obj['success'], True)
		user = User.get(User.username == 'test')
		self.assertNotEquals(user.auth_token, '')

		#test add list of exo
		exo1 = dict(id=1, distance=100, duration=3600)
		exo2 = dict(id=2, distance=50, duration=1800)
		#exo without id wont be add
		exo3 = dict(distance=20, duration=1800)
		exo4 = dict(id=4, distance=10, duration=900)
		#add token dans le header
		raw_body =  {}
		raw_body['exercises'] = [exo1, exo2,exo3, exo4]
		#no auth
		result = self.app.post('/exercises',data=json.dumps(raw_body), content_type='application/json')
		json_obj = json.loads(result.data)
		self.assertEquals(json_obj['success'], False)
		result = self.app.post('/exercises',data=json.dumps(raw_body), content_type='application/json',headers={'Authorization': user.auth_token})
		print raw_body
		#json_obj = json.loads(result.data)
		#print json_obj
		#self.assertEquals(json_obj['success'], True)
		#check exercises are in db
		exo1_obj = Activity.get(Activity.synchro_id == 1) 
		self.assertEquals(exo1_obj.distance, 100)
		self.assertEquals(exo1_obj.duration, 3600)
		exo2_obj = Activity.get(Activity.synchro_id == 2)
		self.assertEquals(exo2_obj.distance, 50)
		self.assertEquals(exo2_obj.duration, 1800)
		exo4_obj = Activity.get(Activity.synchro_id == 4)	
		self.assertEquals(exo4_obj.distance, 10)
		self.assertEquals(exo4_obj.duration, 900)

if __name__ == '__main__':
  unittest.main()
