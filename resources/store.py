from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.store import StoreModel


class Store(Resource):

    @jwt_required
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'An store {0} not found'.format(name)}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'An store {0} already exists'.format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred inserting the store'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': StoreModel.get_all_objects_from_db()}
