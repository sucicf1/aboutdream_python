from flask import Flask, request, Response, jsonify, abort, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"]= 'Ivan'
app.config["UPLOAD_FOLDER"] = "./images"
app.config["ALLOWED_EXTENSIONS"] = set(["png", "jpg", "jpeg", "gif"])
app.config["FILENAME_LENGTH"] = 20

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
db = SQLAlchemy(app)