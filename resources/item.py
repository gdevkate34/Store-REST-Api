import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price',
						type=float,
						required = True,
						help="This field cannot be blank !")

	parser.add_argument('store_id',
						type=int,
						required = True,
						help="This field cannot be blank !")


	@jwt_required()
	#get methos to return particular item
	def get(self,name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		else:
			return {'message':'Item not found!'},404


	
	
	#post method to add an item to the list
	def post(self,name):
		
		if ItemModel.find_by_name(name):
			return {'message':"An item with the name '{}'already exists !".format(name)},404
		data = Item.parser.parse_args()
		item = ItemModel(name,**data)
		try:
			item.save_to_db()
		except:
			return {'message':'An error occurred inserting the item !'},500
		return item.json(),201

		

	#delete method to delete an item from the itemslist
	def delete(self,name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete()	
			return {'message':'Item deleted !'},201
		return {'message':'Item doesnt exist! '}

	#method to update item to item list
	def put(self,name):
		data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)
		
		if item is None:
			try:
				item = ItemModel(name,**data)
				item.save_to_db()
			except:
				return {'message':'An error occurred updating the item'},500
		else:
			try:
				item.price = data['price']
				item.store_id = data['store_id']
				item.save_to_db()
			except:
				return {'message':'An error occurred updating the item'},500
		return item.json()

	
#item list resource to get all the items stored
class ItemList(Resource):
	def get(self):

		return {'items':[item.json() for item in ItemModel.query.all()]}
