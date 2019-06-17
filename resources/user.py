from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='username is requires')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='password is requires')

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        if UserModel.get_by_username(data['username']):
            return {'message': 'A user already exists'}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User created successfully'}, 201

    @classmethod
    def delete(cls):
        data = cls.parser.parse_args()
        user = UserModel.get_by_username(data['username'])
        if not user:
            return {'message': 'An user does not exists'}, 404

        user.delete_from_db()
        return {'message': 'User deleted successfully'}, 200
