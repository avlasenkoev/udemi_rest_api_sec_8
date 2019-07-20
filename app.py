import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'test_key'  # app.config['JWT_SECRET_KEY']
api = Api(app)


jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_black_list(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    # send message to user when token will expired
    return jsonify({
        'description': 'The token has expired',
        'error': 'token expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'The token invalid. Verification failed',
        'error': error
    }), 401


@jwt.unauthorized_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Need authorization for access to this endpoint',
        'error': error
    }), 401


@jwt.needs_fresh_token_loader
def invalid_token_callback():
    return jsonify({
        'description': 'Need to refresh your token',
        'error': 'not fresh token'
    }), 401


@jwt.revoked_token_loader
def invalid_token_callback():
    return jsonify({
        'description': 'You need to login again, token was revoked',
        'error': 'revoke error'
    }), 401


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')


if __name__ == '__main__':
    from db import db
    db.init_app(app)


    @app.before_first_request
    def create_table():
        db.create_all()

    app.run(port=5000, debug=True)
