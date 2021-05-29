import functools,re
from flask import jsonify,request,Flask,g,redirect
from config.Settings import Settings
import jwt

def login_required(func):
    @functools.wraps(func)
    def secure_login(*args, **kwargs):
        auth=True
        auth_token=request.cookies.get("jwt")
       # print(auth_token)
        if auth_token==None:
            auth=False
        if auth_token:
            try:
                payload = jwt.decode(auth_token,Settings.secret,algorithms=['HS256'])
                #print(payload)
                g.userid=payload['userid']#update info in flask application context's g which lasts for one req/res cyycle
                g.username=payload['username']
            except jwt.exceptions.InvalidSignatureError as err:
                print(err)
                auth=False #Failed check

        if auth==False:
            #return jsonify({"Message":"Not Authorized!"}),403 #return response
            return redirect("http://127.0.0.1:5000/login")
        return func(*args, **kwargs)

    return secure_login

