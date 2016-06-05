from flask import Flask, request, jsonify
from models.models import *
import bcrypt
import jwt

HOST = '0.0.0.0'
DEBUG = True
PORT = 8002

# TODO: envoyer un tableau d'objet json
# faire une vraie synchro
# et pas utiliser l'api comme un CRUD

#secret key json web token
secret_key = "AZMNo@Dc01cFdpMKJ45hAsdig3525AoPuASD12ugr70s4D5C"

app = Flask(__name__)

@app.route('/test')
def hello():
    return jsonify(message="hello")

# enregistrer un client
@app.route('/register', methods=['POST'])
def register():
    #parse le json dans le body de la requete, envoie erreur 400 badrequest si le json est foireux
    try:
        json_data = request.get_json()
        try:
            username = json_data["username"]
        except KeyError:
            return error_response("Username is missing")
        try:
            password = json_data["password"]
        except KeyError:
            return error_response("Password is missing")
        try:
            email = json_data["email"]
        except KeyError:
            return error_response("Email is missing")
    except TypeError:
        return error_response("Request must be json")
    
    try:
        #creer l'user dans la db,
        #encode utf-8 sinon pb de stockage du hash dans la db
        with db.transaction():
            user = User.create(
            username = username,
            password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()),
            email = email
            )
        return jsonify(success=True,message="User created")
    except IntegrityError as e:
        if 'username' in e.args[1]:
            return error_response("This username is not available")        
        elif 'mail' in e.args[1]:
            return error_response("This email is not available")

#recuperer un token d'authentification
@app.route('/auth', methods=['POST'])
def auth():
    try:
        json_data = request.get_json()
        try:
            username = json_data["username"]
        except KeyError:
            return error_response("Username is missing")
        try:
            password = json_data["password"]
        except KeyError:
            return error_response("Password is missing")
    except TypeError:
        return error_response("Request must be json")

    #get db user
    try:
        user = User.get(User.username == username)
        if user.password == bcrypt.hashpw(password.encode("utf-8"), user.password.encode("utf-8")).decode():
            token = jwt.encode({"username" : user.username}, secret_key, algorithm='HS256')
            user.auth_token = token
            user.save()
            return jsonify(success=True, token=token)
        else:
            return error_response("Access denied")
    except:
        return error_response("Access denied")

#ajouter un exercice 
@app.route('/exercises', methods=['POST'])
def add_exercise():
    
    encoded_token = request.headers.get('Authorization')
    try:
        decoded_token = jwt.decode(encoded_token, secret_key, alrogithm='HS256')
    #token ne peut etre decode ou est vide
    except (jwt.DecodeError, AttributeError):
        return error_response("Access denied")
    
    try:
        json_data = request.get_json()
        try:
            synchro_id = json_data["id"]
        except KeyError:
            return error_response("Id is missing")
        try:
            distance = json_data["distance"]
        except KeyError:
            distance = 0
        try:
            duration = json_data["duration"]
        except KeyError:
            duration = 0
        try:
            max_speed = json_data["max_speed"]
        except KeyError:
            max_speed = 0
        try:
            avg_speed = json_data["avg_speed"]
        except KeyError:
            avg_speed = 0
        try:
            weather = json_data["weather"]
        except KeyError:
            weather = 0
    except TypeError:
        return error_response("Request must be json")
    
    try:
        user = User.get(User.username == decoded_token["username"])
    except:
        return error_response("Acess denied")
    exercise = Activity.create(
            synchro_id=synchro_id,
            user=user,
            distance=distance,
            duration=duration,
            max_speed=max_speed,
            avg_speed=avg_speed,
            weather=weather
            )
    exercise.save()
    return jsonify(success=True, message="Exercise created")

@app.route('/exercises', methods=['GET'])
def get_exercises():
    encoded_token = request.headers.get('Authorization')
    try:
        decoded_token = jwt.decode(encoded_token, secret_key, algorithm='HS256')
    except (jwt.DecodeError, AttributeError):
        return error_response("Access denied")
    try:
        user = User.get(User.username == decoded_token["username"])
    except:
        return error_response("Access denied")

    exercises = Activity.select().where(Activity.user == user)
    res_exercises = []
    for exo in exercises:
        res_exercises.append(exo.json())
    return jsonify(success=True, exercises=res_exercises)


@app.route('/exercise/<int:exercise_id>', methods=['POST'])
def edit_exercise(exercise_id):
    encoded_token = request.headers.get('Authorization')
    try:
        decoded_token = jwt.decode(encoded_token, secret_key, algorithm='HS256')
    except (jwt.DecodeError, AttributeError):
        return error_response("Access denied token")
    try:
        user = User.get(User.username == decoded_token["username"])
    except:
        return error_response("Access denied user")

    exercises = Activity.select().where(Activity.user == user, Activity.id == exercise_id)
    exo = exercises[0]
    #on recuperer un tableau d'object, pas l'objet directement donc faut bloucer dessus, voir si y'a pas une methodep our recuperer un seul res
    try:
        json_data = request.get_json()
        try:
            distance = json_data["distance"]
            exo.distance = distance
        except KeyError:
            distance = 0
        try:
            duration = json_data["duration"]
            exo.duration = duration
        except KeyError:
            duration = 0
        try:
            max_speed = json_data["max_speed"]
            exo.max_speed = max_speed
        except KeyError:
            max_speed = 0
        try:
            avg_speed = json_data["avg_speed"]
            exo.avg_speed = avg_speed
        except KeyError:
            avg_speed = 0
        try:
            weather = json_data["weather"]
            exo.weather = weather
        except KeyError:
            weather = 0
    except TypeError:
        return error_response("Request must be json")

    exo.save()
    return jsonify(success=True, message="Exercise updated")


def error_response(message):
    return jsonify(success=False, message=message)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
