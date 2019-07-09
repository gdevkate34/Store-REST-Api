from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
	def get(self,name):
		store = StoreModel.find_by_name(name)
		if store:
			return store.json()
		return {'message':'Store doesnt Exist!'}

	def post(self,name):
		store = StoreModel.find_by_name(name)
		if store:
			return {'message':"Store named '{}' already Exist! ".format(name)}
		store = StoreModel(name)
		try:
			store.save_to_db()
		except:
			return {'message':"Error occured while creating store !"},500

		return store.json(),201

	def delete(self,name):
		store = Store.find_by_name(name)
		if store:
			store.delete_from_db()
		else:
			return {'message':"Store doesnt exist in Database! "},404



class StoreList(Resource):
	def get(self):
		return {[store.json() for store in StoreModel.query.all()]}
