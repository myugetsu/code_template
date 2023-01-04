from app import db
from app.api import bp
from flask import jsonify, request, abort
from app.model.user import User
from app.utils.datatables import Datatable
from app.api.auth import token_auth
import time


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    pass


# @bp.route('/users', methods=['GET'])
# @token_auth.login_required
# def get_users():
  # displayable_columns = ['username', 'email']
  # user_data = Datatable(User, 'api.get_users').getRecords(
  #     displayable_columns, request)
  # r = user_data
  # r.status_code = 201
  # return r

    # @bp.route('/users', methods=['POST'])
    # def create_user():
    #     pass

    # @bp.route('/users/<int:id>', methods=['PUT'])
    # @token_auth.login_required
    # def update_user(id):
    #     pass

    # @bp.route('/users/<int:id>', methods=['DELETE'])
    # @token_auth.login_required
    # def delete_user(id):
    #     pass
