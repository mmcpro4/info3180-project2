from . import db
from werkzeug.security import generate_password_hash, check_password_hash


    
# User
class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(80))
    age = db.Column(db.Integer)
    sex = db.Column(db.String(1))
    email = db.Column(db.String(255), unique=True)
    pword = db.Column(db.String(255))
    made_on = db.Column(db.String(80))
    wishs = db.relationship('Wish', secondary=wishes, backref=db.backref('userprofiles', lazy='dynamic'))
    
    def __init__(self, uid, name, age, sex, email, pword, made_on):
        self.uid = uid
        self.name = name
        self.age = age
        self.gender = sex
        self.email = email
        self.pword = generate_password_hash(pword)
        self.made_on = made_on
        
    def cpassword(self, password):
        return check_password_hash(self.password, password)
    
    def is_authenticated(self):
        return True

    def get_id(self):
        try:
            return unicode(self.uid)  # python 2 support
        except NameError:
            return str(self.uid)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.name)



class Wish(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    url = db.Column(db.String(255))
    thumbnail = db.Column(db.String(255))

    def __init__(self,pid, name, description, url, thumbnail):
        self.pid= pid
        self.name = name
        self.description = description
        self.url = url
        self.thumbnail = thumbnail
    
    def get_id(self):
        try:
            return unicode(self.pid)  # python 2 support
        except NameError:
            return str(self.pid)  # python 3 support
            
    def __repr__(self):
        return '<Item %r>' % (self.title)


wishes = db.Table('wishes',
        db.Column('uid', db.Integer, db.ForeignKey('user.uid')), 
        db.Column('wid', db.Integer, db.ForeignKey('wish.pid')))
    