from flask import jsonify
from datetime import datetime
from app import moment
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
  # t = moment('2017-09-28T21:45:23Z').format('L')
    return jsonify({'timestamp': moment.create(datetime.utcnow()).format("L")})
