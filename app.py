from settings import *
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath, exists
from messages import *
from users import *
from followers import *
import random
import string
from sqlalchemy import and_

@app.route("/timeline", methods=["GET", "POST"])
def get_messages():
    if request.args.get('followee', 'false', type=str) == 'true':
        user = User.verify_auth_token(request.json.get("token"))
        if not user:
            return Response("User not authenticated", 
                            403, mimetype="application/json")
        follower_id = user.id
    else:
        follower_id = False
    if request.args.get('asc', 'true', type=str) == 'false':
        asc = False
    else:
        asc = True
    
    page = request.args.get('page', 0, type=int)
    start_date = request.args.get('start_date', 0, type=int)
    end_date = request.args.get('end_date', 0, type=int)
        
    return jsonify({"Messages": Message.get_messages(follower_id,
                                asc, page, start_date, end_date)})

@app.route('/image/<_name>', methods=["GET"])
def display_image(_name):
    return send_file(app.config["UPLOAD_FOLDER"] + '/' +_name)

@app.route("/messages", methods=["POST"])
def add_message():
    user = User.verify_auth_token(request.form["token"])
    if not user:
        return Response("User not authenticated", 403, mimetype="application/json")
    image_name = save_image()
    Message.add_message(request.form["text"], image_name, user.id)
    response = Response("Added message", 201, mimetype="application/json")
    return response

@app.route("/messages/delete/<int:_id>", methods=["POST"])
def delete_message(_id):
    user = User.verify_auth_token(request.json.get("token"))
    message = Message.query.filter_by(id = _id)
    if not message.scalar():
        return Response("Message not found", 404, mimetype="application/json")
    if (not user) or user.id != message.first().user_id:
        return Response("Authentication error", 403, mimetype="application/json")
    message.delete()
    db.session.commit()
    response = Response("Message deleted", 200, mimetype="application/json")
    return response

@app.route("/follow/add", methods=["POST"])
def add_follow():
    user = User.verify_auth_token(request.json.get("token"))
    if not user:
        return Response("User not authenticated", 403, mimetype="application/json")
    ff = Follower.add(user.id, request.json.get("followee_id"))
    response = Response("Added followee", 201, mimetype="application/json")
    return response

@app.route("/follow/delete/<int:_id>", methods=["POST"])
def delete_follow(_id):
    user = User.verify_auth_token(request.json.get("token"))
    if not user:
        return Response("User not authenticated", 400, mimetype="application/json")
    ff = Follower.query.filter(and_(Follower.follower_id == user.id, Follower.followee_id == _id))
    if not ff.scalar():
        return Response("Error: the user isn't followed", 400, mimetype="application/json")
    ff.delete()
    db.session.commit()
    response = Response("User isn't anymore followed", 200, mimetype="application/json")
    return response

@app.route("/users/new", methods=["POST"])
def new_user():
    username = request.json.get("username")
    password = request.json.get("password")
    if username is None or password is None:
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        abort(400)
    user = User.add_user(username, password)
    return jsonify({"username": user.username}, 201)

@app.route("/users/token", methods=["POST"])
def get_auth_token():
    username = request.json.get("username")
    password = request.json.get("password")
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        abort(400)
    token = user.generate_auth_token()
    return jsonify({"token": token.decode("ascii")})


def allowed_file(filename, allowed_ext):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_ext


def save_image():
    image_name = ""
    ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])
    if request.method == "POST":
        if 'file' not in request.files:
            return image_name
        
        file = request.files["file"]
        if file and allowed_file(file.filename, app.config["ALLOWED_EXTENSIONS"]):
            ext = file.filename.rsplit(".", 1)[1].lower()
            if len(secure_filename(file.filename)) < app.config["FILENAME_LENGTH"]: 
                image_name = secure_filename(file.filename)
            else:
                letters = string.ascii_letters
                image_name = ''.join(random.choice(letters) for i in range(
                                int(app.config["FILENAME_LENGTH"]) - 1 - len(ext)))
                image_name = secure_filename(image_name + '.' + ext)
            while exists(join(app.config["UPLOAD_FOLDER"], image_name)):
                letters = string.ascii_letters
                image_name = ''.join(random.choice(letters) for i in range(
                                int(app.config["FILENAME_LENGTH"]) - 1 - len(ext)))
                image_name = secure_filename(image_name + '.' + ext)
            file.save(join(app.config["UPLOAD_FOLDER"], image_name))
    return image_name