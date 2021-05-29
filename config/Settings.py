import os
class Settings:
    secret = "76AE79F316FF4E9C888874925692F"
    host=os.environ['HOST']
    database=os.environ['DATABASE']
    user=os.environ['USERNAME']
    password=os.environ['PASSWORD']
