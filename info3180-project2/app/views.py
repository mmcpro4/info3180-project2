
from app import app, db
from flask import render_template, request, redirect, url_for, flash, jsonify, json, send_from_directory, make_response, abort
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.sql import text
from app.models import User, Wish, wishes
from bs4 import BeautifulSoup
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename
from sqlalchemy.sql import exists
from random import randint
import requests
import urlparse
import datetime
import send 
import time
import os
import random

@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/application')
def Application():
    return app.send_static_file('index.html')



select = """SELECT wish.pid, wish.name, wish.description, wish.url, wish.thumbnail FROM wish JOIN wishes ON wishes.pid = wish.pid WHERE wishes.uid = uid"""    

def timeinfo():
    return time.strftime("%d %b %Y")
    
@app.route("/api/users/register", methods=["POST"])
def signup():
    if not request.form:
        abort(400)
    name = request.form['name']
    email = request.form['email']
    pword = request.form['pword']
    age = request.form['age']
    sex = request.form['gender']
    made_on = timeinfo()
    if db.session.query(User).filter_by(email = email).first() is not None and db.session.query(User).filter_by(pword = pword) is not None:
        return jsonify(error=True, info={}, message="This email and password cannot be used for signing up")
    while True:
        uid = randint(450000,470000)
        if not db.session.query(exists().where(User.uid == str(uid))).scalar():
            break    
    user = User(uid,name,age,sex,email,pword,made_on)
    db.session.add(user)
    db.session.commit()
    info = {'uid': user.uid, 'email': user.email,'name': user.name, 'age': user.age, 'sex': user.sex, 'made_on': user.made_on, 'uri': user.url}
    return jsonify(error=None, info={'info': info}, message="Everything was fine")
    
@app.route("/api/users/<int:uid>/swishlist", methods=["GET","POST"])
def swishlist(uid): 
    user = db.session.query(User).filter_by(uid=uid).first()
    if request.method == "POST":
        lst = []
        if not request.json:
            flash(str(user)+" Sorry but something is went wrong, our bad")
            abort(400)
        if user:
            if 'emails' in request.json:
                lst.append(request.json['email1'])
                lst.append(request.json['email2'])
                lst.append(request.json['email3'])
            if not lst:
                flash(str(user)+" Sorry but something is went wrong, our bad")
                abort(400)
            from_name = user.name
            from_addr = user.email
            Topic = "The best Wishlist"
            userpage = app.config["LINK"] 
            message = "This was my wish list check it out and tell me what you think later! " + "" + userpage
            for i in lst:
                send(i,user.name,user.email,Topic,message)
            info = {'persons': lst}
            response = jsonify({"error":None,"info":info,"message":"Success"})
            return response
        else:
            flash(str(user)+" Sorry but we couldnt find you in our emails that were entered")
            abort(404)
    elif request.method == "GET":
        if user:
            wishlst = []
            wishes = db.session.get_bind().execute(select, id=user.id)
            if wishes:
                for i in wishes:
                    wish = {'pid': i["pid"], 'name': i["name"], 'description': i["description"], 'url': i["url"], 'thumbnail_url': i["thumbnail"]}
                    wishlst.append(wish)
                errors = None
                message = "Success"
                info = {"wishes": wishlst, "user": user.name}
            else: 
                errors = True
                message = "Something went wrong we couldnt find the wishes you were looking for"
                info = {"wishes": wishlst, "user": user.name}
            return jsonify(error=errors, info=info, message=message)
        else:
            flash(str(user)+" Sorry but we couldn't find you in our database")
            abort(404)



@app.route("/api/users/login", methods=["POST"])
def login():
    if not request.json:
        flash("Something went wrong on our end. Please give us a moment")
        abort(400)
    if 'email' not in request.json and 'pword' not in request.json:
        abort(400) 
    email = request.json['email']
    pword = request.json['pword']
    if db.session.query(User).filter_by(email = email).first() is None and db.session.query(User).filter_by(email = email).first() is None :
        flash("Something went wrong on our end please give us a moment we cannot find that email in our database")
        abort(400)
    else:
        uid=db.session.getbind().execute("""SELECT uid FROM Users WHERE email={}""".format(str(email)))
        return jsonify(error=None, info={'user': uid}, message="Everything was fine")
        

       
        

@app.route("/api/users/<int:uid>/wishlist/<int:pid>", methods=["DELETE"])
def delete_item(uid, pid):
    user = db.session.query(User).filter_by(id=uid).first()
    wish = db.session.query(Wish).filter_by(pid=pid).first()
    if user and wish :
        wish = db.session.query(Wish).filter_by(pid=pid).first()
        if wish:
            db.session.delete(wish)
            db.session.commit()
            info = {'info': wish.pid, 'title': wish.name}
    else:
        flash("Something went wrong on our side please give us a moment")
        abort(404)
    return jsonify(error=None,info={'info': info}, message="Everything went fine")    
            

@app.route('/api/thumbnails', methods=['GET'])
def thumbnails():
    if not request.json :
        flash("Something went wrong on our side please give us a moment")
        abort(400) 
    info = request.json['url']
    if info:
        errors = None
        message = "OK"
    else:
        errors = True
        message = "Something went wrong"
    return jsonify(error=errors, info={'info': info}, message=message)
    
@app.route("/api/users/<int:uid>/wishlist", methods=["GET","POST"])
def wishlist(uid):
    user = db.session.query(User).filter_by(uid=uid).first()
    
    if request.method == "POST": 
        if not request.json:
            flash("Something went wrong on our side please give us a moment")
            abort(400) 
        exp = ('name' not in request.json and 'thumbnail_url' not in request.json and 'description' not in request.json and 'url' not in request.json)
        if exp:
            flash("Something went wrong on our side please give us a moment")
            abort(400)
        while True:
            pid = randint(450000,470000)
            if not db.session.query(exists().where(Wish.pid == str(pid))).scalar():
                break    
        name = request.json['name']
        description = request.json['description']
        url = request.json['url']
        thumbnail = request.json['thumbnaill']
        if user:
            wish = Wish(pid,name,description,url,thumbnail)
            db.session.add(wish)
            db.session.commit()
            err = None
            info = {'pid': wish.pid, 'name': wish.name, 'description': wish.description, 'url': wish.url, 'thumbnail': wish.thumbnail}
        else:
            flash("Something went wrong on our side please give us a moment")
            abort(404)
        return jsonify(error=None, data={'info': info}, message="Everything is fine")
    elif request.method == "GET": 
        if user:
            wishlst = []
            
            #FIGURE THIS OUT
            query = text("""SELECT wish.item_id, wish.title, wish.description, wish.url, wish.thumbnail FROM wish INNER JOIN users_wishes ON users_wishes.wish_id = wish.item_id WHERE users_wishes.user_id = :id""")
            wishes = db.session.get_bind().execute(query, id=user.id)
            if wishes:
                for i in wishes:
                    wish = {'pid': wish["pid"], 'name': wish["name"], 'description': wish["description"], 'url': wish["url"], 'thumbnail': wish["thumbnail"]}
                    wishlst.append(wish)
                errors = None
                message = "Success"
                info = {"wishes": wishlst}
            else: 
                errors = True
                message = "No wishes found"
                info = {"wishes": wishlst}
        else:
            flash("Something went wrong on our side please give us a moment")
            abort(404)
        return jsonify(error=errors, info=info, message=message)
        


@app.after_request
def add_header(response):   
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="5000")
