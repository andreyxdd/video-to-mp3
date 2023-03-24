import pika, json

def upload(file, fss, channel, access):
  try:
    fid = fs.put(file) # file id
  except Exception as err:
    return "internal server error", 500
  
  message = {
    "video_fid": str(fid),
    "mp3_fid": None,
    "username": access["username"], # unique
  }
  
  try:
    channel.basic_publish(
      exchange="", # default
      routing_key="video", # default
      body=json.dumps(message), # stringify dict
      properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE # handling msh synchronization with kubernetes pod restarts
      ),
    )
  except:
    fs.delete(fid)
    return "internal server error", 500
