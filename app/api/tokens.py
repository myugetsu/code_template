from flask import jsonify, g, request
from app import db
from app.api import bp
from app.api.auth import basic_auth
from app.api.auth import token_auth
from app.utils.auth_token import generate_token


@bp.route("/tokens", methods=["POST"])
@basic_auth.login_required
#  the database to store tokens
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    results = {"token": token}
    response = jsonify(results)
    response.status_code = 200
    return response


@bp.route("/tokens", methods=["DELETE"])
@token_auth.login_required
# using a saved token from the database
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return "", 204
