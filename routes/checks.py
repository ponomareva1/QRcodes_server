from flask import request, jsonify
from flask_restful import marshal, fields

from main import auth, checks, invalid_input
from routes import checks_route


check_fields = {
    'id': fields.Integer,
    'date': fields.DateTime(dt_format='iso8601'),
    'shop': fields.String,
    'sum': fields.Float
}


@checks_route.route('/checks/getRecent', methods=['GET'])
@auth.login_required
def get_recent_checks():
    num = request.args.get('num')
    try:
        num = 15 if not num else int(num)
    except ValueError:
        return invalid_input("Parameter 'num' must be an integer")
    if not num > 0:
        return invalid_input("Parameter 'num' must be larger than 0.")

    checks_list = list()
    for check in checks[-num:]:
        tmp = marshal(vars(check), check_fields)
        checks_list.append(tmp)

    return jsonify({'checks': checks_list}), 200
