import os, gridfs, pika, json
from flask import Flas, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server)

fs = gridfs.GridFS(mongo.db)

connection = pike.BlockConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@server.route("/login", methods=["POST"])
def login():
  token, err = access.login(request)
  
  if not err:
    return token
  
  return err

@server.route("/upload", methods=["POST"])
def upload():
  access, err = validate.token(request)

  access = json.loads(access) # obtaining the payload after decoding the token
  
  if access["adming"]:
    if len(reqeust.files) != 1: # allowing only one file at a time
      return "exactly 1 file required", 400
    
    for _, file in request.files.items():
      err = util.upload(file, fs, channel, access)
      if err:
        return err
    
    return "success!", 200
  
  return "not authorzied", 401

@server.route("/download", methods=["GET"])
def download():
  pass

if __name__ == "main":
  server.run(host="0.0.0.0", port=8080)
