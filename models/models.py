from peewee import *
import json

db = MySQLDatabase('app_test', user='root', password='')

class TimestampField(Field):
    db_field = 'timestamp'

class BaseModel(Model):
    class Meta:
	database = db

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField(unique=True)
    join_date = TimestampField()
    auth_token = CharField()
    valid_token  = CharField()
    is_active = BooleanField(default=1)

    def json(self):
        json_obj = {}
        json_obj['username'] = self.username
        return json.dumps(json_obj)

class Activity(BaseModel):
    synchro_id = CharField(unique=True) 
    type_activity = CharField(default='run')
    user = ForeignKeyField(User)
    distance = DecimalField()
    duration = DecimalField()
    max_speed = DecimalField()
    avg_speed = DecimalField()
    avg_bpm = DecimalField()
    avg_spm = DecimalField()
    mood = CharField(default='cool')
    weather = CharField(default='cloudy')
    date = TimestampField()

    def json(self):
        json_obj = {}
        json_obj['id'] = str(self.synchro_id)
        json_obj['type'] = str(self.type_activity)
        json_obj['mood'] = str(self.mood)
        json_obj['distance'] = str(self.distance)
        json_obj['duration'] = str(self.duration)
        json_obj['max_speed'] = str(self.max_speed)
        json_obj['avg_speed'] = str(self.avg_speed)
        json_obj['avg_bpm'] = str(self.avg_bpm)
        json_obj['avg_spm'] = str(self.avg_spm)
        json_obj['weather'] = str(self.weather)
        #json_obj['date'] = self.date
        return json_obj
