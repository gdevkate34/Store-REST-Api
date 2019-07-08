from flask import Flask,request
from flask_restful import Resource, Api
from flask_jwt import JWT,jwt_required
from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store,StoreList


app = Flask(__name__)

app.secret_key = 'shiv' #secret key for JWT tokenization
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'	
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
api=Api(app)
items = []
jwt = JWT(app,authenticate,identity) #create JWT TOKEN


#create tables in database created just before first http request
@app.before_first_request
def create_tables():
	db.create_all()


#add each resource created ,to api 
api.add_resource(Store,'/store')
api.add_resource(StoreList,'/stores')
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')

if __name__=='__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000,debug=True)

