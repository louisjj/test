import unittest
import json
from app import app
from models.models import *

class Test(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True

	def test_test(self):
		result = self.app.get('/test')
		self.assertEquals(result.status_code, 200)
		json_obj = json.loads(result.data)
		self.assertEquals(json_obj['message'], "hello")

	def test_register(self):
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

		raw_body = {}
		result = self.app.post('/register',data=json.dumps(raw_body), content_type='application/json')
		self.assertEquals(result.status_code, 200)
		json_obj = json.loads(result.data)
		self.assertEquals(json_obj['success'], False)

		raw_body['username'] = 'test'
		raw_body['password'] = 'wrong_password'
                result = self.app.post('/register',data=json.dumps(raw_body), content_type='application/json')
		self.assertEquals(result.status_code, 200)
		json_obj = json.loads(result.data)
		self.assertEquals(json_obj['success'], False)

		raw_body['password'] = '1234'
                result = self.app.post('/register',data=json.dumps(raw_body), content_type='application/json')
		self.assertEquals(result.status_code, 200)
		json_obj = json.loads(result.data)
		self.assertEquals(json_obj['success'], True)

		
if __name__ == '__main__':
  unittest.main()
