from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_migrate import Migrate

import uuid
import threading

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    discord = db.Column(db.Integer, unique=True)

    def get(self, user_id):
        return User.query.get(user_id)

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token_id = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Float, nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, nullable=False)
    recipient_id = db.Column(db.Integer, nullable=False)
    token_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    comment = db.Column(db.String(1024))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    supply = db.Column(db.Float, nullable=False, nullable=False)



#API FUNCTIONS

def create_user(username, password, discord=None):
    if discord is None: 
        new_user = User(username=username, password=password)
    else:
        new_user = User(username=username, password=password, discord=discord)
    db.session.add(new_user)
    db.session.commit()
    return 'User created successfully!'

def get_user_by_address(address):
    return db.session.query(User).filter(User.address == address).all()

def get_user_by_discord(discord_id):
    return db.session.query(User).filter(User.discord == discord_id).all()

def get_token_by_name(name):
    return db.session.query(Token).filter(Token.name == name).all()

def get_token_by_symbol(symbol):
    return db.session.query(Token).filter(Token.symbol == symbol).all()

def get_wallet(user, token):
    return db.session.query(Wallet).filter(Wallet.user_id == user.id and Wallet.token_id == token.id).all()

def get_balance(user, token):
    return get_wallet(user, token).balance

@app.route("/create_user", methods=['POST'])
def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    discord = request.form.get('discord')
    if not discord: discord = None
    return create_user(username, password, discord)

@app.route("/create_token", methods=['POST'])
def create_token():
    name = request.form.get('name')
    amount = request.form.get('amount')
    recipient_id = request.form.get('recipient_id')
    symbol = request.form.get('symbol')
    recipient = db.session.query(User).filter(User.id == recipient_id).all()
    if recipient is None:
        return "Recipient doesn't exists", 404
    new_token = Token(name=name, symbol=symbol, amount=amount)
    db.session.add(new_token)
    db.session.commit()


@app.route("/send", methods=['POST'])
def send():
    recipient_id = request.form.get('recipient_id')
    token_id = request.form.get('token_id')
    amount = request.form.get('amount')

    recipient = db.session.query(User).filter(User.id == recipient_id).all()
    if recipient is None:
        return "recipient doesn't exists", 404
    
@app.route("/create_wallet", methods=['POST'])
def create_wallet():
    user_id = request.form.get('user_id')
    token_id = request.form.get('token_id')

    user = db.session.query(User).filter(User.id == user_id).all()
    if user is None:
        return "user doesn't exists", 404
    token = db.session.query(Token).filter(Token.id == token_id).all()
    if token is None:
        return "token doesn't exists", 404
    new_wallet = Wallet(user_id=user_id, token_id=token_id, balance=0)
    db.session.add(new_wallet)
    db.session.commit()
    return f'Wallet on {token.name} created successfully'

if __name__ == '__main__':
    app.run(debug=True)