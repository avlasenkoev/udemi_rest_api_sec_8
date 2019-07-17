from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from  flask_jwt_extended import create_access_token, create_refresh_token


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help='username is requires')
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help='password is requires')


class UserRegister(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        if UserModel.get_by_username(data['username']):
            return {'message': 'An user already exists'}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User created successfully'}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.get_by_id(user_id)
        if not user:
            return {'message': 'An user does not exists'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.get_by_id(user_id)
        if not user:
            return {'message': 'An user does not exists'}, 404
        user.delete_from_db()
        return {'message': 'User deleted successfully'}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()

        # find user in the database
        user = UserModel.get_by_username(data['username'])

        # check password
        if user and safe_str_cmp(user.password, data['password']):
            accsess_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                    'access_token': accsess_token,
                    'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials'}, 401